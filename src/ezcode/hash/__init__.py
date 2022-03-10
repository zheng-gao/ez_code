

def get_hash(*args):
    if type(args[0]) is list or type(args[0]) is tuple:
        args = args[0]
    primes = [53, 57]  # configurable: hash(x1, x2, x3, ...) = (((p1 + x1) * p2 + x2) * p3 + x3) ...
    hash_value = 0
    for index, number in enumerate(args):
        prime = primes[index % len(primes)]
        hash_value = number + prime * hash_value
    return hash_value

