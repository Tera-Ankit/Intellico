# calculator.py
def add(a, b):
    """Returns the sum of a and b."""
    return a + b

def subtract(a, b):
    """Returns the result of subtracting b from a."""
    return a - b

def multiply(a, b):
    """Returns the product of a and b."""
    return a * b

def divide(a, b):
    """Returns the result of dividing a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

