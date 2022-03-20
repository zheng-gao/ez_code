def hash_encode(numbers: list) -> int:
    def _hash_encode_2(a: int, b: int) -> int:
        """
            https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
            Cantor pairing function: (a + b) * (a + b + 1) / 2 + a; where a, b >= 0
            Szudzik's function: a >= b ? a * a + a + b : a + b * b;  where a, b >= 0
        """
        A = 2 * a if a >= 0 else -2 * a - 1  # map x to positive integers
        B = 2 * b if b >= 0 else -2 * b - 1  # map y to positive integers
        C = (A * A + A + B) if A >= B else (B * B + A)  # Szudzik's method
        if (a >= 0 and b >= 0) or (a < 0 and b >= 0 and A >= B) or (a < 0 and b < 0 and A < B):
            return C // 2     # Map evens onto positives
        return (C + 1) // -2  # Map odds onto negative

    if not numbers:
        raise ValueError("Cannot hash empty list")
    hash_value = numbers[0]
    for i in range(1, len(numbers)):
        hash_value = _hash_encode_2(hash_value, numbers[i])
    return hash_value


def hash_decode(hash_code: int, size: int = 2) -> list:
    """
        :Return: the unique list of the given size that encodes to hash_code
    """
    def _sqrt(C) -> int:
        """
            Newton's method: x[n+1] = x[n] - f(x[n]) / f'(x[n])
            For square root, f(x) = x^2 - C ==> x[n+1] = (x[n] + C/x[n]) / 2
            :Return: the largest integer x for which x * x does not exceed n.
        """
        x_n = (C + 1) // 2  # use C/2 as the initial value, x_n is 0 if C is 0
        while True:
            x_n_plus_1 = (x_n + C // x_n) // 2
            if x_n_plus_1 >= x_n:  # ==> x_n_plus_1 * x_n_plus_1 >= C
                return x_n
            x_n = x_n_plus_1

    def _hash_decode_2(hash_code: int) -> list:
        C = -2 * hash_code - 1 if hash_code < 0 else 2 * hash_code  # Mapping onto positive integers
        s = _sqrt(C)
        A, B = (C - s * s, s) if C - s * s < s else (s, C - s * s - s)  # Reversing Pairing
        # Undoing map int to positive integers
        a = (A + 1) // -2 if A % 2 else A // 2  # True if A not divisible by 2
        b = (B + 1) // -2 if B % 2 else B // 2  # True if B not divisible by 2
        return a, b

    if size <= 0:
        raise ValueError(f"The size must be positive: {size}")
    number_stack = list()
    for i in range(size, 1, -1):
        hash_code, number = _hash_decode_2(hash_code)
        number_stack.append(number)
    number_stack.append(hash_code)
    return number_stack[::-1]

