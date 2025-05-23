# sequence.py

import re
from Bio.Seq import Seq

def sequence_properties(sequence: str, mode: str):
    """Given a DNA sequence and mode (HOMO/LUMO), return Ebp and tbb arrays."""
    
    # Onsite energies (single base, not base pair)
    if mode == "HOMO":
        base_energy = {
            "A": 8.3,
            "T": 8.3,
            "G": 8.0,
            "C": 8.0
        }
        coupling_data = {
            "AA": 0.02,  "TT": 0.02,
            "AT": -0.035, "TA": -0.05,
            "AG": 0.03,  "GA": 0.11,
            "AC": -0.01, "CA": 0.01,
            "TG": 0.01,  "GT": -0.01,
            "CT": 0.03,  "TC": 0.11,
            "GG": 0.1,   "CC": 0.1,
            "GC": -0.01, "CG": 0.05,
        }
    elif mode == "LUMO":
        base_energy = {
            "A": -4.9,
            "T": -4.9,
            "G": 0.0,
            "C": -4.5
        }
        coupling_data = {
            "AA": -0.029, "TT": -0.029,
            "AT": 0.0005, "TA": 0.002,
            "AG": 0.003,  "GA": -0.001,
            "AC": 0.032,  "CA": 0.017,
            "TG": 0.017,  "GT": 0.032,
            "CT": 0.003,  "TC": -0.001,
            "GG": 0.020,  "CC": 0.020,
            "GC": -0.010, "CG": -0.008,
        }
    else:
        raise ValueError("Invalid mode. Use 'HOMO' or 'LUMO'.")

    sequence = sequence.upper()

    # Onsite energies
    Ebp = [base_energy[b] for b in sequence]

    # Hopping terms (between adjacent bases)
    tbb = []
    for i in range(len(sequence) - 1):
        pair = sequence[i] + sequence[i + 1]
        t = coupling_data.get(pair)
        if t is None:
            raise ValueError(f"Invalid basepair combination: {pair}")
        tbb.append(t)

    return Ebp, tbb


def validate_sequence(seq):
    seq = seq.upper()
    if not re.fullmatch(r'[ACGT]+', seq):
        raise ValueError("Invalid sequence: only A, C, G, T characters are allowed.")
    return seq

def get_reverse_complement(seq):
    return str(Seq(seq).reverse_complement())

def get_sequence_profile(seq):
    """Optional: return frequency or position info, etc."""
    return {
        'length': len(seq),
        'A': seq.count('A'),
        'C': seq.count('C'),
        'G': seq.count('G'),
        'T': seq.count('T'),
    }


#def one_hot_encode(seq):
    """Convert to one-hot encoding if needed for ML or matrix ops."""
 ##  return [mapping[base] for base in seq]
