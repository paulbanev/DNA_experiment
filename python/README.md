# DNA Transport Simulation

A Python-based quantum transport simulation tool for modeling charge (hole or electron) transport through DNA sequences using tight-binding Hamiltonian methods.

## Overview

This project simulates electronic transport in DNA polymers using quantum mechanical tight-binding models. It supports multiple structural models (WIRE, FISHBONE, LADDER) and analyzes both HOMO (highest occupied molecular orbital) and LUMO (lowest unoccupied molecular orbital) electronic states.

The simulation computes key transport metrics including:
- **Eigenvalue spectrum** (energy levels)
- **Participation ratio** (delocalization)
- **Transfer rates** (charge mobility)
- **Density of States (DOS)**
- **Dipole moments** and frequency analysis
- **Weighted mean frequencies**

## Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Required packages:
- `numpy` - Numerical computations
- `biopython` - DNA sequence manipulation
- `matplotlib` - Visualization
- `pandas` - Data export
- `openpyxl` - Excel file generation

### Docker Setup (Optional)

Build and run using Docker:

```bash
docker build -f Dockerfile.dev -t dna-transport .
docker run -it -v $(pwd):/app dna-transport
```

## Quick Start

Basic example simulating a short DNA sequence:

```bash
python main.py --sequence ATGCAT --mode HOMO --model FISHBONE --disorder 0
```

This will:
1. Simulate HOMO transport through the sequence ATGCAT
2. Use the FISHBONE model (double helix with sugar backbones)
3. Run without disorder (clean system)
4. Generate plots in `results/` directory
5. Print summary statistics to console

## Usage

### Command-Line Arguments

```bash
python main.py [OPTIONS]
```

#### Required Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `--sequence` | string | One strand of your DNA sequence (e.g., `ATGCAT`)<br>Allowed characters: A, C, G, T, M (M = A-C mismatch) |
| `--mode` | choice | Electronic mode: `HOMO` or `LUMO` |
| `--model` | choice | Transport model: `WIRE`, `FISHBONE`, `LADDER`, `EXTENDED_LADDER`, `SPECIALE` |

#### Optional Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--symmetry` | choice | `symmetric` | Hopping symmetry:<br>`symmetric` (tSp=tS)<br>`asymmetric` (tSp=0.16) |
| `--disorder` | int | `0` | Disorder type (0–10, see table below) |
| `--seed` | int | `None` | Random seed for disorder (reproducibility) |
| `--export` | flag | `False` | Export results to Excel file |
| `--number_of_DOS_points` | int | `10` | Number of bins for DOS histogram |
| `--workers` | int | all CPUs | Number of parallel workers<br>`None` or `0` = use all CPUs<br>`1` = sequential (for debugging)<br>`N` = use N cores |

### Transport Models

| Model | Description | Status |
|-------|-------------|--------|
| `WIRE` | 1D chain (base pairs only) | ✅ Implemented |
| `FISHBONE` | Double helix with sugar backbones (3 sites per base pair) | ✅ Implemented |
| `LADDER` | Simplified ladder model | ⚠️ Incomplete |
| `EXTENDED_LADDER` | Extended ladder with diagonal couplings | ⚠️ Incomplete |
| `SPECIALE` | Custom polymer model | ⚠️ Incomplete |

### Disorder Types

Disorder simulates experimental variations in energy levels and hopping integrals:

| Type | Description | Energy Disorder | Hopping Disorder |
|------|-------------|-----------------|------------------|
| `0` | No disorder (clean system) | - | - |
| `1` | Base pair energy disorder | Eg: 5% | - |
| `2` | Sugar energy disorder | Es: 5% | - |
| `3` | Full energy disorder | Eg, Es: 5% | - |
| `6` | Base-base hopping disorder | - | tg: 50% |
| `7` | Sugar-base hopping disorder | - | tS: 50% |
| `8` | Full hopping disorder | - | tg, tS: 50% |
| `9` | Complete disorder | All: 5% | All: 50% |
| `10` | Complete disorder (alias) | All: 5% | All: 50% |

**Note:** When disorder > 0, the simulation runs 10 times with different random seeds to gather statistics.

### Example Commands

**HOMO transport in clean FISHBONE model:**
```bash
python main.py --sequence GCGCATAT --mode HOMO --model FISHBONE --disorder 0
```

**LUMO transport with energy disorder:**
```bash
python main.py --sequence ATCGATCG --mode LUMO --model WIRE --disorder 1 --seed 42
```

**HOMO transport with full disorder, export to Excel:**
```bash
python main.py --sequence GGCCTTAA --mode HOMO --model FISHBONE --disorder 9 --export
```

**Asymmetric hopping with custom DOS resolution:**
```bash
python main.py --sequence ATGCAT --mode HOMO --model FISHBONE --symmetry asymmetric --number_of_DOS_points 20
```

## Performance Optimization

### Multiprocessing Support

The simulation supports parallel execution to significantly reduce computation time when running multiple disorder realizations.

**How it works:**
- When `--disorder > 0`, the program runs 10 independent simulations
- By default, these run in parallel using all available CPU cores
- Each worker process handles one complete simulation
- Results are aggregated after all runs complete

**Performance benefit:**
- On an 8-core machine: **~7-8x faster** (with disorder)
- On a 4-core machine: **~3-4x faster** (with disorder)
- Sequential fallback available for debugging

**Usage examples:**

```bash
# Use all CPU cores (default, fastest)
python main.py --sequence GCGCATAT --mode HOMO --model FISHBONE --disorder 9

# Use 4 cores explicitly
python main.py --sequence GCGCATAT --mode HOMO --model FISHBONE --disorder 9 --workers 4

# Sequential execution (for debugging or comparison)
python main.py --sequence GCGCATAT --mode HOMO --model FISHBONE --disorder 9 --workers 1
```

**Notes:**
- For `disorder = 0` (single run), parallelization is not used
- Memory usage scales with number of workers
- Worker count auto-detects CPU cores if not specified


### Console Output

The program prints:
- Eigenvector matrix (quantum states)
- Degeneracy detection results
- Lambda values (time evolution coefficients)
- Summary statistics for all metrics (mean ± std)
- Mean transfer rates per site

### Generated Files

#### Plots (in `results/` directory):

1. **`eigenvalue_spectrum.png`** - Energy levels of the system
2. **`participation_ratio.png`** - Delocalization of each eigenstate
3. **`mean_probability.png`** - Time-averaged charge distribution
4. **`mean_transfer_rate.png`** - Transfer rates (log scale)
5. **`density_of_states.png`** - DOS histogram

#### Excel Export (optional):

When using `--export` flag:
- **`results/results.xlsx`** - Multi-sheet workbook with:
  - Separate sheets for each metric
  - All simulation runs
  - Mean and standard error calculations

## Scientific Background

For detailed physics and mathematical formulation, see [PHYSICS.md](PHYSICS.md).

### Key Concepts

**Tight-Binding Hamiltonian:** Models electrons/holes as hopping between discrete sites (base pairs) with onsite energies and nearest-neighbor couplings.

**HOMO vs LUMO:**
- **HOMO** (Highest Occupied Molecular Orbital): Hole transport, positive energies (8-9 eV)
- **LUMO** (Lowest Unoccupied Molecular Orbital): Electron transport, negative/zero energies (0 to -5 eV)

**Participation Ratio:** Measures how many sites contribute to an eigenstate. PR = 1 means fully localized, PR = N means fully delocalized.

**Transfer Rate:** Efficiency of charge moving to each site: rate = probability / arrival_time

## Project Structure

```
python/
├── main.py               # Entry point and CLI
├── analysis.py           # Core quantum computations
├── sequence.py           # DNA sequence processing
├── matrixes.py          # Hamiltonian construction
├── disorder.py          # Disorder model definitions
├── visualization.py     # Plot generation
├── export_results.py    # Excel export
├── utils.py             # Helper functions
├── requirements.txt     # Dependencies
└── Dockerfile.dev       # Docker configuration
```

## Physical Parameters

### Constants
- Planck constant: h = 4.135667517 eV·fs
- Bohr radius: a₀ = 0.52917721067 Å
- Base stacking distance: 3.4 Å
- Cross-strand distance: 10 Å

### Time Evolution
- Time points: L = 64 × 16385 ≈ 1M points
- Time range: 0 to 100,000 fs

## Limitations & Notes

1. **Incomplete Models:** LADDER, EXTENDED_LADDER, and SPECIALE models are not yet implemented
2. **Memory Usage:** Large time arrays (~1M points) may require significant RAM
3. **Validation:** No unit tests currently available
4. **Language:** Some variable names use Greek transliteration (legacy code)

## Contributing

When adding features:
1. Follow PEP 8 style guidelines
2. Add docstrings to all functions
3. Update this README and PHYSICS.md
4. Test with multiple sequences and disorder types

## References

Energy and hopping parameters are based on:
- HOMO parameters: Marcus-like studies (MLS data)
- LUMO parameters: Literature values for DNA electron transport
- Model architectures: Standard tight-binding approaches for DNA

## License

[Add your license here]

## Contact

[Add contact information here]
