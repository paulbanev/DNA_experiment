#matrixes
#Here the matrix describing our problem is created and filled. This is the basis upon which analysis.py runs

import numpy as np
import random
def matrixes(Ebp, tbb, disorder_params, sequence, mode, seed=None,  symmetry='symmetric'): 
    if seed is not None:
        random.seed(seed)
    length = len(sequence)
    MD = 3 * length
    A = np.zeros((MD, MD), dtype=np.float64)

    # HOMO or LUMO setup
    if mode == "HOMO":
        ES = 9.0
        tS = 0.02
        tSp = tS if symmetry == 'symmetric' else 0.16
    elif mode == "LUMO":
        ES = 0.0
        tS = 0.0
        tSp = tS if symmetry == 'symmetric' else 0.0
    else:
        raise ValueError("Mode must be 'HOMO' or 'LUMO'")

    # Matrix population
    # Here you can see the usage of the percentiles created in disorder.py
    # You can change the random generator from gaussian to something else if you want 
    for k1 in range(MD):
        for k2 in range(k1, MD):
            if k1 == k2:
                if k1 % 3 == 0 or k1 % 3 == 2:
                    A[k1, k2] = ES * (1 + disorder_params.get("es_disorder", 0) * random.gauss(0, 1))
                elif k1 % 3 == 1:
                   A[k1, k2] = Ebp[k1//3] * (1 + disorder_params.get("eg_disorder", 0) * random.gauss(0, 1))
            elif k1 % 3 == 1 and k2 % 3 == 1 and abs(k1 - k2) == 3:
                if (k1 // 3) < len(tbb):
                    tbb_dis = tbb[k1 // 3] * (1 + disorder_params.get("tg_disorder", 0) * random.gauss(0, 1))
                A[k1, k2] = tbb_dis
            elif abs(k1 - k2) == 1:
                if {k1 % 3, k2 % 3} == {0, 1}:
                    tS_dis = tS * (1 + disorder_params.get("ts_disorder", 0) * random.gauss(0, 1))
                    A[k1, k2] = tS_dis
                elif {k1 % 3, k2 % 3} == {1, 2}:
                    tSp_dis = tSp * (1 + disorder_params.get("tsp_disorder", 0) * random.gauss(0, 1))
                    A[k1, k2] = tSp_dis
                else:
                    A[k1, k2] = 0.0
            else:
                A[k1, k2] = 0.0

    # Symmetrize. Important to assure that it will be Hamiltonian
    for k1 in range(MD):
        for k2 in range(k1):
            A[k1, k2] = A[k2, k1]

    return A, MD
