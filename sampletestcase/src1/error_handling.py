# error_handling.py
def divide_with_error_handling(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
