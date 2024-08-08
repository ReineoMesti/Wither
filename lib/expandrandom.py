import random as rand

unif = rand.uniform
randi = rand.randint
def coord_hash(mod, **kwarg):
    res = 1
    for key, val in kwarg.items():
        res *= (hash(key + '=' + str(val)) + 1)
        res %= mod
    return res

def polynominal_linear(term, lower, upper, integer=True):
    low_limit = lower / term
    up_limit = upper / term
    result = 0
    for i in range(term):
        result += rand.uniform(low_limit, up_limit)
    if integer:
        result = round(result)
    result = min(result, upper)
    result = max(result, lower)
    return result
def weighted_choice(options:dict, rengine = unif):
    'Choice by weighted chance'
    w_range = sum(options.values())
    lottery = rengine(0, w_range)
    for key, val in options.items():
        if w_range <= val:
            return key
        w_range -= val
    return key
