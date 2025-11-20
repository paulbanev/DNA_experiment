"""Disorder Model Definitions

This module defines disorder models that simulate experimental variations
in DNA transport parameters. Disorder models specify which parameters
(onsite energies or hopping integrals) are perturbed and by how much.

Disorder Types:
    0: No disorder (clean system)
    1-3: Energy disorders only
    6-8: Hopping integral disorders only
    9-10: Complete disorder (all parameters)

Disorder is implemented as Gaussian multiplicative noise:
    Parameter_new = Parameter_0 * (1 + δ * N(0,1))
where δ is the disorder strength and N(0,1) is a standard normal random variable.
"""

import random

def get_disorder_model(disorder_type, seed=None):
    """Get disorder parameters for the specified disorder type.
    
    Returns a dictionary specifying which parameters should have disorder
    and their respective disorder strengths (standard deviations).
    
    Args:
        disorder_type (int): Disorder type from 0 to 10
            0: No disorder
            1: Base pair energy disorder (Eg)
            2: Sugar energy disorder (Es)
            3: Full energy disorder (Eg + Es)
            6: Base-base hopping disorder (tg)
            7: Sugar-base hopping disorder (tS)
            8: Full hopping disorder (tg + tS)
            9/10: Complete disorder (all parameters)
        seed (int, optional): Random seed for reproducibility
    
    Returns:
        dict: Dictionary with disorder parameters, e.g.:
            {'eg_disorder': 0.05, 'ts_disorder': 0.5}
            Empty dict {} if disorder_type == 0
    
    Disorder Strengths:
        - Energy parameters: 5% (δ = 0.05)
          Rationale: Onsite energies are relatively stable
        - Hopping integrals: 50% (δ = 0.5)
          Rationale: Hopping depends sensitively on spatial overlap
    
    Raises:
        ValueError: If disorder_type is not in range 0-10
    
    Notes:
        - Types 9 and 10 are identical (10 exists for batch experiments)
        - Disorder is applied in matrixes.py as: param * (1 + δ * N(0,1))
        - Each simulation run with disorder should use a different seed
    """
    if seed is not None:
        random.seed(seed)

    if disorder_type == 0:
        return {}

    if disorder_type == 1:
        return {"eg_disorder": 0.05}
    elif disorder_type == 2:
        return {"es_disorder": 0.05}#for now, both sides are disturbed, there is no ES choice, just ES+ES
    elif disorder_type == 3:
        return {"es_disorder": 0.05, "eg_disorder": 0.05}
    elif disorder_type == 6:
        return {"tg_disorder": 0.5}
    elif disorder_type == 7:
        return {"ts_disorder": 0.5}
    elif disorder_type == 8:
        return {"ts_disorder": 0.5, "tg_disorder": 0.5}
    elif disorder_type == 9:
        return {
            "es_disorder": 0.05,
            "eg_disorder": 0.05,
            "ts_disorder": 0.5,
            "tg_disorder": 0.5,
            "tsp_disorder": 0.5
        }
    elif disorder_type == 10:# This is the same as 9. It exists so that we can use the input "10" to run the 10-9-8-...3-2-1-0 experiment. meaning all possible types in the same run
        return {
            "es_disorder": 0.05,
            "eg_disorder": 0.05,
            "ts_disorder": 0.5,
            "tg_disorder": 0.5,
            "tsp_disorder": 0.5
        }
    else:
        raise ValueError("Unknown disorder type.")
