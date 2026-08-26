def add(a, b):
    """Return the sum of two numbers.

    Args:
        a: First addend, expected to be an int or float.
        b: Second addend, expected to be an int or float.

    Returns:
        The numeric sum of ``a`` and ``b``.

    Raises:
        TypeError: If either ``a`` or ``b`` is not an int or float, or if either is a bool.
    """
    # Reject bools explicitly because bool is subclass of int
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("Both arguments must be int or float, not bool")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be int or float")
    return a + b
