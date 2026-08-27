import numbers

def add(a, b):
    """Return the sum of two numbers.

    Args:
        a: First addend, expected to be a real number (int, float, Decimal, Fraction, etc.).
        b: Second addend, expected to be a real number.

    Returns:
        The numeric sum of ``a`` and ``b``.

    Raises:
        TypeError: If either ``a`` or ``b`` is not a real number, or if either is a bool.
    """
    # Reject bools explicitly because bool is subclass of int
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("bool is not allowed as an argument")
    # Ensure both are real numbers (int, float, Decimal, Fraction, etc.)
    if not isinstance(a, numbers.Real) or not isinstance(b, numbers.Real):
        raise TypeError("Both arguments must be real numbers")
    return a + b
