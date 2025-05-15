#matrixes

import numpy as np
import random
def matrixes(length, mode, disorder_params, seed=None):  # default optional
    if seed is not None:
        random.seed(seed)
    MD = 3 * length
    A = np.zeros((MD, MD))

    # HOMO or LUMO setup
    if mode == "HOMO":
        ES = 9.0
        tS = 0.02
        tSp = disorder_params.get("tsp_disorder", tS)
        EGkC = 8.0
        EAkT = 8.3
        tGG = 0.1
    elif mode == "LUMO":
        ES = 0.0
        tS = 0.0
        tSp = disorder_params.get("tsp_disorder", tS)
        EGkC = -4.5
        EAkT = -4.9
        tGG = 0.020
    else:
        raise ValueError("Mode must be 'HOMO' or 'LUMO'")

    h = 4.135667517  # eV·fs
    hbar = h / (2 * np.pi)
    eVperhbar = (2 * np.pi) / h

    # Matrix population
    for k1 in range(MD):
        for k2 in range(k1, MD):
            if k1 == k2:
                if k1 % 3 == 0 or k1 % 3 == 2:
                    A[k1, k2] = ES * (1 + disorder_params.get("es_disorder", 0) * random.gauss(0, 1))
                elif k1 % 3 == 1:
                    A[k1, k2] = EGkC * (1 + disorder_params.get("eg_disorder", 0) * random.gauss(0, 1))
            elif k1 % 3 == 1 and k2 % 3 == 1 and abs(k1 - k2) == 3:
                tGG_dis = tGG * (1 + disorder_params.get("tg_disorder", 0) * random.gauss(0, 1))
                A[k1, k2] = tGG_dis
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

    # Symmetrize
    for k1 in range(MD):
        for k2 in range(k1):
            A[k1, k2] = A[k2, k1]

    return A, MD, eVperhbar
