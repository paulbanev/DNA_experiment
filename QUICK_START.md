# Quick Start Guide: Using Structure Files

## Overview

Your DNA transport simulation now accepts **structure files** in addition to DNA sequences!

```
Before:  DNA sequence (AAAAA) → Hardcoded parameters → Simulation
Now:     Structure file (CIF/XYZ/PDB) → Extracted parameters → Simulation
```

## Quick Examples

### 1. Test with Carbon Chain (XYZ)
```bash
cd python
python main.py --structure example_chain.xyz --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0
```

### 2. Test with Benzene (CIF)
```bash
cd python
python main.py --structure example_benzene.cif --mode LUMO --model LADDER --symmetry symmetric --disorder 0
```

### 3. Test with DNA (PDB)
```bash
cd python
python main.py --structure example_dna.pdb --mode HOMO --model WIRE --symmetry symmetric --disorder 0
```

### 4. Old method still works!
```bash
cd python
python main.py --sequence AAAAA --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0
```

## File Format Decision Tree

```
What file do you have?
│
├── Crystal structure from database → Use .CIF file
│   Example: Download from Crystallography Open Database
│
├── Simple molecular coordinates → Use .XYZ file
│   Example: Create your own carbon chain
│
├── Protein/DNA from PDB → Use .PDB file
│   Example: Download from Protein Data Bank
│
└── DNA sequence string → Use --sequence argument
    Example: AAAAA, ATGCATGC
```

## Example Files Included

| File | Format | Description | Atoms |
|------|--------|-------------|-------|
| `example_chain.xyz` | XYZ | 10-atom carbon chain | 10 C |
| `example_benzene.cif` | CIF | Benzene molecule with lattice | 6 C, 6 H |
| `example_dna.pdb` | PDB | Adenine-Thymine base pair | 8 C, 3 N, 1 O |

## Understanding the Output

When you run with a structure file, you'll see:
```
Reading structure from: example_chain.xyz
Extracted 10 sites from structure file
```

The program:
1. ✅ Reads atomic positions from the file
2. ✅ Identifies chain atoms (C, N, O, S)
3. ✅ Sorts them along the chain direction
4. ✅ Computes on-site energies from element types
5. ✅ Calculates hopping from distances
6. ✅ Runs the simulation as normal

## Troubleshooting

### "No such file or directory"
- Check that you're in the `python` directory
- Use full path: `--structure C:\Users\...\myfile.cif`

### "Unsupported file format"
- Make sure your file ends with `.cif`, `.xyz`, or `.pdb`
- Check the file isn't corrupted

### "No chain atoms found"
- Your structure needs C, N, O, or S atoms
- Edit `structure_reader.py` line 176 to include other elements

## Want to Create Your Own XYZ File?

```xyz
5
My custom carbon chain
C    0.0    0.0    0.0
C    1.5    0.0    0.0
C    3.0    0.0    0.0
C    4.5    0.0    0.0
C    6.0    0.0    0.0
```

Save as `my_chain.xyz` and run:
```bash
python main.py --structure my_chain.xyz --mode HOMO --model FISHBONE --symmetry symmetric --disorder 0
```

## Where to Get CIF/PDB Files

- **CIF**: [Crystallography Open Database](http://www.crystallography.net/cod/)
- **PDB**: [Protein Data Bank](https://www.rcsb.org/)
- **CIF**: [Cambridge Structural Database](https://www.ccdc.cam.ac.uk/)

## Next Steps

1. ✅ Try the example files
2. Download a CIF file from a database
3. Create your own XYZ file
4. Customize parameters in `structure_reader.py`
5. Compare results with sequence mode

---

**Need more details?** See `STRUCTURE_FILE_GUIDE.md` for comprehensive documentation.
