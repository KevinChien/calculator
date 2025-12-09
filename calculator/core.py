"""簡化的核心計算模組：只支援整數/浮點數與基本四則運算 (+ - * /) 和括號。

此模組使用 AST 解析以避免使用不安全的 eval。為了最大相容性，僅處理 `ast.BinOp`、
`ast.UnaryOp` 與 `ast.Constant`（數字）。
"""
import ast
import operator

__all__ = ["evaluate"]

# 只允許的二元運算
_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

# 一元運算（正/負號）
_UNARY_OPS = {ast.UAdd: lambda x: x, ast.USub: operator.neg}


def evaluate(expr: str):
    """評估只含基本四則運算與括號的表達式並回傳數值。

    例： evaluate('1+2*3') -> 7
    """
    if not isinstance(expr, str):
        raise TypeError("expression must be a string")

    node = ast.parse(expr, mode="eval")
    return _eval(node.body)


def _eval(node):
    # 二元運算
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _BINARY_OPS:
            return _BINARY_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")

    # 一元運算
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    # 數字常數（Python 3.8+ 使用 ast.Constant）
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # 如果執行到這裡，代表節點類型不被允許
    raise ValueError(f"Unsupported expression element: {type(node)}")
