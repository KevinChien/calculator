from calculator.core import evaluate


def test_basic_operations():
    assert evaluate("1+2*3") == 7
    assert evaluate("(2+3)*4") == 20


def test_functions_and_consts():
    assert round(evaluate("sqrt(16)"), 6) == 4.0
    assert abs(evaluate("pi") - 3.14159) < 1e-5
from calculator.core import evaluate


def test_basic_operations():
    assert evaluate("1+2*3") == 7
    assert evaluate("(2+3)*4") == 20


def test_functions_and_consts():
    assert round(evaluate("sqrt(16)"), 6) == 4.0
    assert abs(evaluate("pi") - 3.14159) < 1e-5
