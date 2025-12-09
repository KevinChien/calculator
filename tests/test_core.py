from calculator.core import evaluate


def test_basic_add_mul():
    assert evaluate("1+2*3") == 7
    assert evaluate("(2+3)*4") == 20


def test_more_operations():
    assert evaluate("200*2") == 400
    assert evaluate("123*3") == 369
    assert evaluate("10/4") == 2.5
