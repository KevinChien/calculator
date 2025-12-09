"""核心計算模組：使用 AST 安全解析與評估數學表達式。

支援：+ - * / ** % // 括號、數字、與 math 中的常用函數（如 sqrt, sin, cos, log...）。
不使用 eval，僅允許安全的 AST 節點。
"""
import ast
import operator
import math

__all__ = ["evaluate"]

# 允許的數學函數（可擴充）
_MATH_NAMES = (
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "asinh",
    "acosh",
    "atanh",
    "sqrt",
    "log",
    "log10",
    "exp",
    "pow",
    "floor",
    "ceil",
    "fabs",
    "degrees",
    "radians",
    "hypot",
    "factorial",
)

# 建立允許的函數集合（只加入 math 中存在的），並加入一些內建函數
_ALLOWED_FUNCS = {name: getattr(math, name) for name in _MATH_NAMES if hasattr(math, name)}
_ALLOWED_FUNCS.update({"abs": abs, "max": max, "min": min})

# 常數
_CONSTS = {"pi": math.pi, "e": math.e}
if hasattr(math, "tau"):
    _CONSTS["tau"] = math.tau


# 二元運算對映
_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# 一元運算
_UNARY_OPS = {ast.UAdd: lambda x: x, ast.USub: operator.neg}


def evaluate(expr: str):
    """評估數學字串表達式並回傳數值。

    例子： evaluate('1+2*3') -> 7
    """
    if not isinstance(expr, str):
        raise TypeError("expression must be a string")

    node = ast.parse(expr, mode="eval")
    return _eval(node.body)


def _eval(node):
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _BINARY_OPS:
            return _BINARY_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Call):
        # 只允許簡單名稱呼叫，如 sqrt(4)
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        fname = node.func.id
        if fname not in _ALLOWED_FUNCS:
            raise ValueError(f"Function '{fname}' is not allowed")
        args = [_eval(a) for a in node.args]
        return _ALLOWED_FUNCS[fname](*args)

    if isinstance(node, ast.Name):
        if node.id in _CONSTS:
            return _CONSTS[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    # 拒絕其他 AST 節點
    raise ValueError(f"Unsupported expression element: {type(node)}")
