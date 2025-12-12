# DNA Transport Simulation

Quantum transport simulation for DNA and molecular systems.

## Features

- **Sequence Mode**: Traditional DNA sequence input (A, T, G, C)
- **Structure Mode**: Read molecular structures from CIF, XYZ, or PDB files
- Multiple transport models (WIRE, FISHBONE, LADDER, EXTENDED_LADDER, SPECIALE)
- HOMO/LUMO transport calculations
- Disorder models for realistic simulations

## Quick Start

### Using DNA Sequence (Traditional)
```bash
cd python
python main.py --sequence AAAAA --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0 --export
```

### Using Structure Files (New!)
```bash
cd python

# Carbon chain (XYZ)
python main.py --structure example_chain.xyz --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0

# Benzene (CIF)
python main.py --structure example_benzene.cif --mode LUMO --model LADDER --symmetry symmetric --disorder 0

# DNA base pair (PDB)
python main.py --structure example_dna.pdb --mode HOMO --model WIRE --symmetry symmetric --disorder 0
```

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started quickly with examples
- **[STRUCTURE_FILE_GUIDE.md](STRUCTURE_FILE_GUIDE.md)** - Comprehensive guide to structure files
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - What changed and how it works

## Supported File Formats

- **CIF** (Crystallographic Information File) - Crystal structures
- **XYZ** (Chemical File Format) - Simple molecular coordinates  
- **PDB** (Protein Data Bank) - Biomolecular structures
- **Sequence** - DNA sequence strings (A, T, G, C)

## Example Files Included

- `example_chain.xyz` - 10-atom carbon chain
- `example_benzene.cif` - Benzene molecule
- `example_dna.pdb` - DNA base pair

