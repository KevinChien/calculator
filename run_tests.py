"""簡單的測試執行器，用於在沒有 pytest 的環境下執行基本測試。
這會逐一 import tests 中的模組並執行以 `test_` 開頭的函式。
"""
import importlib
import pkgutil
import sys
import os
import runpy


def run_tests():
    failures = 0
    tests_dir = os.path.join(os.path.dirname(__file__), "tests")
    if not os.path.isdir(tests_dir):
        print("No tests directory found")
        sys.exit(0)
    for fname in os.listdir(tests_dir):
        if not fname.endswith(".py"):
            continue
        path = os.path.join(tests_dir, fname)
        # run the test file to get its globals
        g = runpy.run_path(path)
        modname = f"tests.{fname[:-3]}"
        for k, v in g.items():
            if k.startswith("test_") and callable(v):
                try:
                    v()
                    print(f"PASS: {modname}.{k}")
                except AssertionError as e:
                    print(f"FAIL: {modname}.{k} -> {e}")
                    failures += 1
                except Exception as e:
                    print(f"ERROR: {modname}.{k} -> {e}")
                    failures += 1
    if failures:
        print(f"{failures} failures")
        sys.exit(1)
    print("All tests passed")


if __name__ == "__main__":
    run_tests()
