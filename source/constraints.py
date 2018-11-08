def all_different(x):
    """ Return True if all non-None values in x are different"""
    seen = set()
    return not any([i is not None and (i in seen or seen.add(i)) for i in x])