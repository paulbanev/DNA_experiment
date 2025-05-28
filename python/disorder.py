# disorder.py
#here we map which polymer parameters( site energies or hopping intervals) will be disturbed by the disorder_type
# in general we disturb energies by 5% and intervals by 50%.
#here we get the apropriate percentile which we implement in matrixes.py to get the desired fluctuations around the bibliographical value. 
import random

def get_disorder_model(disorder_type, seed=None):
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
