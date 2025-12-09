from calculator.core import evaluate


def repl():
    print("Python 計算機 REPL。輸入 'exit' 或 'quit' 結束。")
    try:
        while True:
            s = input("> ")
            if not s:
                continue
            if s.strip().lower() in ("exit", "quit"):
                break
            try:
                r = evaluate(s)
                print(r)
            except Exception as e:
                print("錯誤：", e)
    except (KeyboardInterrupt, EOFError):
        print()  # 美化輸出


if __name__ == "__main__":
    repl()
