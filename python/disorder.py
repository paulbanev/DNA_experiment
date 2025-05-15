# disorder.py
import random

def get_disorder_model(disorder_type, length, seed=None):
    if seed is not None:
        random.seed(seed)

    if disorder_type == 0:
        return {}

    if disorder_type == 1:
        return {"eg_disorder": 0.05}
    elif disorder_type == 2:
        return {"es_disorder": 0.05}
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
    elif disorder_type == 10:
        return {
            "es_disorder": 0.05,
            "eg_disorder": 0.05,
            "ts_disorder": 0.5,
            "tg_disorder": 0.5,
            "tsp_disorder": 0.5
        }
    else:
        raise ValueError("Unknown disorder type.")
