import random as rand
def linear_uneven(term, lower, upper, integer=True):
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
