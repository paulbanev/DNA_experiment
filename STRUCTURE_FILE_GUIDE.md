# Structure File Support for DNA Transport Simulations

This document explains how to use structure files (CIF, XYZ, PDB) instead of DNA sequences for transport simulations.

## Overview

The DNA transport simulation app now supports two input modes:

1. **Sequence Mode** (original): Input a DNA sequence string (e.g., `AAAAA`)
2. **Structure Mode** (new): Input a molecular structure file (CIF, XYZ, or PDB)

## Supported File Formats

### 1. CIF (Crystallographic Information File)
- Standard format for crystal structures
- Contains lattice parameters and atomic coordinates
- Example: `example_benzene.cif`

### 2. XYZ (Chemical File Format)
- Simple format with Cartesian coordinates
- First line: number of atoms
- Second line: comment/metadata
- Following lines: element symbol and x, y, z coordinates
- Example: `example_chain.xyz`

### 3. PDB (Protein Data Bank)
- Standard format for biomolecular structures
- Contains detailed atomic information
- Commonly used for proteins and DNA

## How It Works

When you provide a structure file, the program:

1. **Parses the file** using the appropriate reader (CIF/XYZ/PDB)
2. **Extracts atomic positions** and identifies chain atoms (C, N, O, S)
3. **Sorts atoms** along the specified chain direction (x, y, or z)
4. **Computes on-site energies** based on element types:
   - Carbon (C): -8.0 eV
   - Nitrogen (N): -9.5 eV
   - Oxygen (O): -10.5 eV
   - Sulfur (S): -7.5 eV
5. **Calculates hopping integrals** using distance-based model:
   ```
   t = t₀ × exp(-β × (r - r₀))
   ```
   where:
   - t₀ = 0.1 eV (hopping at equilibrium)
   - r₀ = 1.4 Å (typical C-C bond length)
   - β = 3.0 Å⁻¹ (decay parameter)

## Usage Examples

### Using DNA Sequence (Original Method)
```bash
python main.py --sequence AAAAA --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0
```

### Using Structure File (New Method)

#### Example 1: Carbon chain from XYZ file
```bash
python main.py --structure example_chain.xyz --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0 --chain-direction z
```

#### Example 2: Benzene from CIF file
```bash
python main.py --structure example_benzene.cif --mode LUMO --model LADDER --symmetry symmetric --disorder 0 --chain-direction x
```

#### Example 3: Your own CIF file
```bash
python main.py --structure /path/to/your/structure.cif --mode HOMO --model WIRE --symmetry symmetric --disorder 0 --chain-direction y
```

## Command-Line Arguments

### Input Arguments (Mutually Exclusive)
- `--sequence`: DNA sequence string (e.g., `AAAAA`)
- `--structure`: Path to structure file (CIF, XYZ, or PDB)

### Other Arguments
- `--mode`: Electronic mode (`HOMO` or `LUMO`)
- `--model`: Transport model (`WIRE`, `FISHBONE`, `LADDER`, `EXTENDED_LADDER`, `SPECIALE`)
- `--symmetry`: Hopping symmetry (`symmetric` or `asymmetric`)
- `--disorder`: Disorder type (0-10)
- `--chain-direction`: Primary chain direction for structure files (`x`, `y`, or `z`, default: `z`)
- `--number_of_DOS_points`: Number of density of states points (default: 10)
- `--export`: Export results to Excel
- `--seed`: Random seed for disorder

## Creating Your Own Structure Files

### XYZ File Format
```
<number of atoms>
<comment line>
<element> <x> <y> <z>
<element> <x> <y> <z>
...
```

Example (`my_chain.xyz`):
```
5
Simple carbon chain
C    0.0    0.0    0.0
C    1.4    0.0    0.0
C    2.8    0.0    0.0
C    4.2    0.0    0.0
C    5.6    0.0    0.0
```

### CIF File Format
CIF files are more complex and typically obtained from crystallographic databases like:
- [Crystallography Open Database (COD)](http://www.crystallography.net/cod/)
- [Cambridge Structural Database (CSD)](https://www.ccdc.cam.ac.uk/structures/)
- [Protein Data Bank (PDB)](https://www.rcsb.org/)

## Testing the Structure Reader

You can test the structure reader independently:

```bash
# Test with XYZ file
python structure_reader.py example_chain.xyz

# Test with CIF file
python structure_reader.py example_benzene.cif

# Test with your own file
python structure_reader.py /path/to/your/structure.cif
```

This will display:
- Number of atoms read
- Element types present
- Lattice vectors (for CIF files)
- Number of sites and hoppings extracted
- Energy and hopping parameter ranges

## Advanced: Customizing the Model

The structure-to-parameters conversion is defined in `structure_reader.py`. You can customize:

1. **Element energies** (line ~189): Modify `element_energies` dictionary
2. **Hopping model** (line ~206): Change `t0`, `r0`, `beta` parameters
3. **Chain atom selection** (line ~176): Filter different elements
4. **Distance calculations** (line ~199): Implement different hopping models

## Comparison: Sequence vs Structure

| Feature | Sequence Mode | Structure Mode |
|---------|---------------|----------------|
| **Input** | DNA sequence string | Structure file (CIF/XYZ/PDB) |
| **Parameters** | Pre-defined for DNA bases | Calculated from atomic positions |
| **Flexibility** | Limited to DNA | Any molecular system |
| **Accuracy** | Empirical parameters | Distance-based approximation |
| **Use Case** | DNA transport | General molecular transport |

## Troubleshooting

### Error: "Unsupported file format"
- Make sure your file has the correct extension (`.cif`, `.xyz`, or `.pdb`)
- Check that the file exists at the specified path

### Error: "No chain atoms found in structure"
- The structure must contain at least one of: C, N, O, S atoms
- Modify the `chain_atoms` filter in `structure_reader.py` if needed

### Warning: Unrealistic hopping values
- This can happen if atoms are too far apart or too close together
- Check your structure file for errors
- Adjust the hopping model parameters if needed

## Future Enhancements

Potential improvements:
- Support for 2D and 3D transport (not just 1D chains)
- Machine learning based parameter extraction
- Integration with DFT calculations
- Automatic bond detection and connectivity analysis
- Support for more file formats (POSCAR, MOL2, etc.)

## References

- **CIF Format**: [International Union of Crystallography](https://www.iucr.org/resources/cif)
- **XYZ Format**: [Open Babel Documentation](http://openbabel.org/wiki/XYZ)
- **PDB Format**: [wwPDB Documentation](https://www.wwpdb.org/documentation/file-format)
