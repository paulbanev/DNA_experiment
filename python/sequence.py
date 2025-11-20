"""DNA Sequence Processing and Physical Parameter Extraction

This module handles DNA sequence validation and extracts physical parameters
(onsite energies and hopping integrals) based on the electronic mode (HOMO/LUMO)
and transport model (WIRE, FISHBONE, LADDER, etc.).

The energy values and hopping integrals are derived from literature sources,
primarily Marcus-like studies (MLS) for HOMO and various experimental/theoretical
work for LUMO.
"""


import re
from Bio.Seq import Seq

def sequence_properties(sequence: str, mode: str, model: str):
    """Extract physical parameters from DNA sequence.
    
    Maps each base to its onsite energy and each adjacent base pair to their
    hopping integral based on the specified electronic mode and transport model.
    
    Args:
        sequence (str): DNA sequence (one strand) using characters A, C, G, T, M
                       where M represents an A-C mismatch
        mode (str): Electronic mode - either 'HOMO' (hole transport) or
                   'LUMO' (electron transport)
        model (str): Transport model - 'WIRE', 'FISHBONE', 'LADDER',
                    'EXTENDED_LADDER', or 'SPECIALE'
    
    Returns:
        tuple: (Ebp, tbb) where:
            - Ebp (list): Onsite energies in eV for each base in sequence
            - tbb (list): Hopping integrals in eV between adjacent bases
                         (length = len(sequence) - 1)
    
    Raises:
        ValueError: If mode is not 'HOMO' or 'LUMO'
        ValueError: If model is not recognized
        ValueError: If invalid base pair combination found
    
    Notes:
        - Energy values differ between WIRE/FISHBONE and LADDER models
        - Hopping integrals are directional (5'→3' convention)
        - LUMO transport ignores sugar backbones (ES = 0, tS = 0)
    """
    if model in("FISHBONE", "WIRE"): 
         # here we need to input the Eb on a singular base level, aswell as the hopping integrals both the vertical and horisontal.
       # we must not forget the diagonal hopping integrals. We'll read them here and then if needed nullify in matrixes.py 
        if mode == "HOMO":#HOMO DATA BY MLS
            base_energy = {
                "A": 8.49,
                "T": 8.49,
                "G": 8.3,
                "C": 8.3,
                "M": 8.43    #m represents A-C missmatch on the bp level
            }
            coupling_data = {               #the interaction parameters between basepairs. 5'3' direction
                "AA": 0.038,  "TT": 0.038,
                "AT": -0.0050, "TA": -0.037,
                "AG": 0.037,  "GA": 0.142,
                "AC": -0.016, "CA": 0.028,
                "TG": 0.028,  "GT": -0.016,
                "CT": 0.037,  "TC": 0.142,
                "GG": 0.116,   "CC": 0.116,
                "GC": -0.01, "CG": 0.075,
                "GM": 0.13, "MG": 0.031,      #mG represents connection Am-G,and Gm represents G-Am on 5'-3' direction
                "MM": 0.036                   #mm represents connection Am-Am on 5'-3' diection
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

        #sequence = sequence.upper()

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
    elif model in ("LADDER", "EXTENDED_LADDER"):
       # here we need to input the Eb on a singular base level, aswell as the hopping integrals both the vertical and horisontal.
       # we must not forget the diagonal hopping integrals. We'll read them here and then if needed nullify in matrixes.py 
        if mode == "HOMO":
            base_energy = {
                "A": 8.3,
                "T": 8.3,
                "G": 8.0,
                "C": 8.0,
                "M": 8.43    #m represents A-C missmatch on the bp level
            }
            coupling_data = {               #the interaction parameters between basepairs. 5'3' direction
                "AA": 0.02,  "TT": 0.02,
                "AT": -0.035, "TA": -0.05,
                "AG": 0.03,  "GA": 0.11,
                "AC": -0.01, "CA": 0.01,
                "TG": 0.01,  "GT": -0.01,
                "CT": 0.03,  "TC": 0.11,
                "GG": 0.1,   "CC": 0.1,
                "GC": -0.01, "CG": 0.05,
                "GM": 0.13, "MG": 0.031,      #mG represents connection Am-G,and Gm represents G-Am on 5'-3' direction
                "MM": 0.036                   #mm represents connection Am-Am on 5'-3' diection
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

        #sequence = sequence.upper()

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
     # your code here
    elif model =="SPECIALE":
         # Onsite energies (base pair)
        if mode == "HOMO":
            base_energy = {
                "A": 8.3,
                "T": 8.3,
                "G": 8.0,
                "C": 8.0,
                "M": 8.43    #m represents A-C missmatch on the bp level
            }
            coupling_data = {               #the interaction parameters between basepairs. 5'3' direction
                "AA": 0.02,  "TT": 0.02,
                "AT": -0.035, "TA": -0.05,
                "AG": 0.03,  "GA": 0.11,
                "AC": -0.01, "CA": 0.01,
                "TG": 0.01,  "GT": -0.01,
                "CT": 0.03,  "TC": 0.11,
                "GG": 0.1,   "CC": 0.1,
                "GC": -0.01, "CG": 0.05,
                "GM": 0.13, "MG": 0.031,      #mG represents connection Am-G,and Gm represents G-Am on 5'-3' direction
                "MM": 0.036                   #mm represents connection Am-Am on 5'-3' diection
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

        #sequence = sequence.upper()

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
    # your code here
    else:
        raise ValueError(f"Invalid model: {model}")



def validate_sequence(seq):
    """Validate and normalize DNA sequence.
    
    Args:
        seq (str): Input DNA sequence (case-insensitive)
    
    Returns:
        str: Uppercase validated sequence
    
    Raises:
        ValueError: If sequence contains characters other than A, C, G, T, M
    """
    seq = seq.upper()
    if not re.fullmatch(r'[ACGTM]+', seq):
        raise ValueError("Invalid sequence: only A, C, G, T, M characters are allowed.")
    return seq

def get_reverse_complement(seq):
    """Get reverse complement of DNA sequence using BioPython.
    
    Args:
        seq (str): DNA sequence
    
    Returns:
        str: Reverse complement sequence (A↔T, G↔C, reversed)
    """
    return str(Seq(seq).reverse_complement())

def get_sequence_profile(seq):
    """Get basic statistics about DNA sequence composition.
    
    Args:
        seq (str): DNA sequence
    
    Returns:
        dict: Dictionary containing:
            - 'length': Total sequence length
            - 'A': Count of adenine bases
            - 'C': Count of cytosine bases
            - 'G': Count of guanine bases
            - 'T': Count of thymine bases
    """
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
