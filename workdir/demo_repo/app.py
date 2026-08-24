def add(a, b):
    """Return the sum of two numbers.

    Only ``int`` and ``float`` types are supported. If either argument is not a number,
    a ``TypeError`` is raised.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be int or float")
    return a + b
