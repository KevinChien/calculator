import tkinter as tk
from tkinter import messagebox
import traceback
from calculator.core import evaluate


def _make_button(root, text, row, col, cmd, colspan=1):
    btn = tk.Button(root, text=text, command=lambda: cmd(text), font=("Consolas", 14))
    btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1)


def main():
    root = tk.Tk()
    root.title("計算機")

    expr = tk.StringVar()
    entry = tk.Entry(root, textvariable=expr, font=("Consolas", 20), justify="right")
    entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=3, pady=3)

    def on_click(txt):
        if txt == "C":
            expr.set("")
        elif txt == "⌫":
            s = expr.get()
            expr.set(s[:-1])
        elif txt == "=":
            try:
                res = evaluate(expr.get())
                expr.set(str(res))
            except Exception as e:
                # show detailed error to the user and log it for debugging
                tb = traceback.format_exc()
                try:
                    messagebox.showerror("Evaluation error", tb)
                except Exception:
                    # if messagebox fails (rare), fallback to setting the entry text
                    expr.set("Error")
                # write a small error log to current working directory
                try:
                    with open("error_log.txt", "a", encoding="utf-8") as f:
                        f.write(tb + "\n")
                except Exception:
                    pass
        elif txt == "^":
            expr.set(expr.get() + "**")
        elif txt in ("sin","cos","tan","sqrt","log","pi","e"):
            if txt in ("pi","e"):
                expr.set(expr.get() + txt)
            else:
                expr.set(expr.get() + txt + "(")
        else:
            expr.set(expr.get() + txt)

    # 鍵盤支援：Enter 評估, Esc 清除, Backspace 自然運作
    def on_key(event):
        if event.keysym == "Return":
            on_click("=")
        elif event.keysym == "Escape":
            on_click("C")

    entry.bind("<Key>", on_key)

    buttons = [
        ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
        ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
        ("0", 4, 0), (".", 4, 1), ("(", 4, 2), (")", 4, 3),
        ("C", 5, 0), ("⌫", 5, 1), ("^", 5, 2), ("=", 5, 3),
    ]

    # row 6: function keys
    func_buttons = [("sin", 6, 0), ("cos", 6, 1), ("tan", 6, 2), ("sqrt", 6, 3),
                    ("log", 7, 0), ("pi", 7, 1), ("e", 7, 2),]

    for b in buttons:
        if len(b) == 3:
            text, r, c = b
            _make_button(root, text, r, c, on_click)
        else:
            text, r, c, cs = b
            _make_button(root, text, r, c, on_click, colspan=cs)

    for i in range(8):
        root.grid_rowconfigure(i, weight=1)
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)

    for b in func_buttons:
        text, r, c = b
        _make_button(root, text, r, c, on_click)

    root.mainloop()


if __name__ == "__main__":
    main()
