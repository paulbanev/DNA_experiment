# structure_reader.py
"""
Module for reading molecular structures from various file formats (CIF, XYZ, PDB, etc.)
and extracting parameters for transport simulations.
"""

import re
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Atom:
    """Represents an atom in 3D space."""
    element: str
    x: float
    y: float
    z: float
    label: Optional[str] = None

@dataclass
class Structure:
    """Represents a molecular/crystal structure."""
    atoms: List[Atom]
    lattice_vectors: Optional[np.ndarray] = None  # For periodic systems
    metadata: Dict = None

class CIFReader:
    """Parser for Crystallographic Information Files (CIF)."""
    
    @staticmethod
    def read(filepath: str) -> Structure:
        """Read a CIF file and extract atomic positions."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"CIF file not found: {filepath}")
        
        atoms = []
        lattice_params = {}
        metadata = {}
        
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Parse lattice parameters
        for line in lines:
            if '_cell_length_a' in line:
                lattice_params['a'] = float(line.split()[1].split('(')[0])
            elif '_cell_length_b' in line:
                lattice_params['b'] = float(line.split()[1].split('(')[0])
            elif '_cell_length_c' in line:
                lattice_params['c'] = float(line.split()[1].split('(')[0])
            elif '_cell_angle_alpha' in line:
                lattice_params['alpha'] = float(line.split()[1].split('(')[0])
            elif '_cell_angle_beta' in line:
                lattice_params['beta'] = float(line.split()[1].split('(')[0])
            elif '_cell_angle_gamma' in line:
                lattice_params['gamma'] = float(line.split()[1].split('(')[0])
        
        # Find atomic coordinates section
        in_atom_section = False
        for i, line in enumerate(lines):
            if '_atom_site_fract_x' in line or '_atom_site_Cartn_x' in line:
                in_atom_section = True
                # Find where the data starts
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('_'):
                    j += 1
                # Read atomic data
                for k in range(j, len(lines)):
                    parts = lines[k].strip().split()
                    if not parts or parts[0].startswith('_') or parts[0].startswith('#'):
                        break
                    if len(parts) >= 5:
                        label = parts[0]
                        element = parts[1] if not parts[1].isdigit() else parts[0]
                        # Remove numbers from element symbol
                        element = re.sub(r'[0-9]+', '', element)
                        try:
                            x = float(parts[2].split('(')[0])
                            y = float(parts[3].split('(')[0])
                            z = float(parts[4].split('(')[0])
                            atoms.append(Atom(element, x, y, z, label))
                        except (ValueError, IndexError):
                            continue
                break
        
        lattice_vectors = None
        if lattice_params:
            lattice_vectors = CIFReader._compute_lattice_vectors(lattice_params)
            metadata['lattice_params'] = lattice_params
        
        return Structure(atoms, lattice_vectors, metadata)
    
    @staticmethod
    def _compute_lattice_vectors(params: Dict) -> np.ndarray:
        """Convert lattice parameters to lattice vectors."""
        a, b, c = params['a'], params['b'], params['c']
        alpha = np.radians(params['alpha'])
        beta = np.radians(params['beta'])
        gamma = np.radians(params['gamma'])
        
        # Compute lattice vectors
        v1 = np.array([a, 0, 0])
        v2 = np.array([b * np.cos(gamma), b * np.sin(gamma), 0])
        cx = c * np.cos(beta)
        cy = c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma)) / np.sin(gamma)
        cz = np.sqrt(c**2 - cx**2 - cy**2)
        v3 = np.array([cx, cy, cz])
        
        return np.array([v1, v2, v3])


class XYZReader:
    """Parser for XYZ molecular structure files."""
    
    @staticmethod
    def read(filepath: str) -> Structure:
        """Read an XYZ file and extract atomic positions."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"XYZ file not found: {filepath}")
        
        atoms = []
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # First line: number of atoms
        try:
            n_atoms = int(lines[0].strip())
        except (ValueError, IndexError):
            raise ValueError("Invalid XYZ file format: first line should be number of atoms")
        
        # Second line: comment (metadata)
        metadata = {'comment': lines[1].strip() if len(lines) > 1 else ''}
        
        # Rest: atomic coordinates
        for i in range(2, min(2 + n_atoms, len(lines))):
            parts = lines[i].strip().split()
            if len(parts) >= 4:
                element = parts[0]
                try:
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    atoms.append(Atom(element, x, y, z))
                except ValueError:
                    continue
        
        return Structure(atoms, metadata=metadata)


class PDBReader:
    """Parser for Protein Data Bank (PDB) files."""
    
    @staticmethod
    def read(filepath: str) -> Structure:
        """Read a PDB file and extract atomic positions."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"PDB file not found: {filepath}")
        
        atoms = []
        metadata = {}
        
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('ATOM') or line.startswith('HETATM'):
                    # PDB format: columns are fixed-width
                    element = line[76:78].strip() or line[12:14].strip()
                    element = re.sub(r'[0-9]+', '', element)
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    label = line[12:16].strip()
                    atoms.append(Atom(element, x, y, z, label))
                elif line.startswith('TITLE'):
                    metadata['title'] = line[10:].strip()
        
        return Structure(atoms, metadata=metadata)


class StructureReader:
    """Main interface for reading various structure file formats."""
    
    READERS = {
        '.cif': CIFReader,
        '.xyz': XYZReader,
        '.pdb': PDBReader,
    }
    
    @staticmethod
    def read(filepath: str) -> Structure:
        """Automatically detect format and read structure file."""
        filepath = Path(filepath)
        extension = filepath.suffix.lower()
        
        if extension not in StructureReader.READERS:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported formats: {', '.join(StructureReader.READERS.keys())}"
            )
        
        reader_class = StructureReader.READERS[extension]
        return reader_class.read(str(filepath))


def structure_to_sequence(structure: Structure, chain_direction: str = 'z') -> Tuple[List[float], List[float]]:
    """
    Convert a structure to energy and hopping parameters.
    
    This is a simplified model that:
    1. Identifies atoms along a chain (e.g., carbon backbone)
    2. Computes on-site energies based on local environment
    3. Estimates hopping integrals from interatomic distances
    
    Args:
        structure: Structure object containing atomic positions
        chain_direction: Primary chain direction ('x', 'y', or 'z')
    
    Returns:
        Ebp: List of on-site energies
        tbb: List of hopping integrals between adjacent sites
    """
    # Sort atoms along the specified direction
    direction_map = {'x': 0, 'y': 1, 'z': 2}
    axis = direction_map[chain_direction.lower()]
    
    # Filter relevant atoms (e.g., carbon backbone for organic molecules)
    chain_atoms = [atom for atom in structure.atoms if atom.element in ['C', 'N', 'O', 'S']]
    
    if not chain_atoms:
        raise ValueError("No chain atoms found in structure")
    
    # Sort by position along chain direction
    chain_atoms.sort(key=lambda atom: [atom.x, atom.y, atom.z][axis])
    
    # Compute on-site energies (simplified model based on element)
    element_energies = {
        'C': -8.0,  # sp2 carbon (approximate HOMO level)
        'N': -9.5,
        'O': -10.5,
        'S': -7.5,
    }
    
    Ebp = [element_energies.get(atom.element, -8.0) for atom in chain_atoms]
    
    # Compute hopping integrals based on distance
    tbb = []
    for i in range(len(chain_atoms) - 1):
        atom1 = chain_atoms[i]
        atom2 = chain_atoms[i + 1]
        
        # Calculate distance
        dx = atom2.x - atom1.x
        dy = atom2.y - atom1.y
        dz = atom2.z - atom1.z
        distance = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # Hopping integral decays exponentially with distance
        # t = t0 * exp(-beta * (r - r0))
        t0 = 0.1  # eV (typical hopping at equilibrium)
        r0 = 1.4  # Angstroms (typical C-C bond length)
        beta = 3.0  # Decay parameter
        
        t = t0 * np.exp(-beta * (distance - r0))
        tbb.append(t)
    
    return Ebp, tbb


def structure_properties(filepath: str, mode: str = 'HOMO', chain_direction: str = 'z') -> Tuple[List[float], List[float]]:
    """
    Read a structure file and extract transport properties.
    
    Args:
        filepath: Path to structure file (CIF, XYZ, PDB)
        mode: 'HOMO' or 'LUMO' (affects sign/scaling of energies)
        chain_direction: Primary chain direction for 1D transport
    
    Returns:
        Ebp: List of on-site energies
        tbb: List of hopping integrals
    """
    structure = StructureReader.read(filepath)
    Ebp, tbb = structure_to_sequence(structure, chain_direction)
    
    # Adjust energies for LUMO vs HOMO
    if mode == 'LUMO':
        Ebp = [-E for E in Ebp]  # Approximate LUMO as negative HOMO
    
    return Ebp, tbb


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        structure = StructureReader.read(filepath)
        print(f"Read {len(structure.atoms)} atoms from {filepath}")
        print(f"Elements: {set(atom.element for atom in structure.atoms)}")
        
        if structure.lattice_vectors is not None:
            print(f"Lattice vectors:\n{structure.lattice_vectors}")
        
        # Try to extract sequence
        try:
            Ebp, tbb = structure_to_sequence(structure)
            print(f"\nExtracted {len(Ebp)} sites with {len(tbb)} hoppings")
            print(f"Energy range: {min(Ebp):.3f} to {max(Ebp):.3f} eV")
            print(f"Hopping range: {min(tbb):.3f} to {max(tbb):.3f} eV")
        except Exception as e:
            print(f"Error extracting sequence: {e}")
    else:
        print("Usage: python structure_reader.py <structure_file>")
