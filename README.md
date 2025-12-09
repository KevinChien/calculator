# Python 計算機

一個簡單的可重用 Python 計算機示例，包含：

- `calculator.core`：安全評估數學表達式的核心模組（使用 `ast`，避免 `eval`）。
- `calculator.cli`：命令列互動介面（REPL）。
- `calculator.gui`：基於 Tkinter 的簡單 GUI。
- `tests/`：一些基本單元測試（使用 `pytest`）。


快速開始（PowerShell）：

```powershell
cd e:\workspace\src_code\smaple_project
python -m calculator.cli      # 啟動 CLI
python -m calculator.gui      # 啟動 GUI

# 安裝 pytest（如要執行測試）
pip install pytest
pytest -q
```

打包為執行檔（Windows）

```powershell
cd e:\workspace\src_code\smaple_project
# 安裝 pyinstaller
pip install pyinstaller

# 使用內建的 helper 腳本
.\build_exe.ps1 -Target gui   # 產生 GUI 單一檔案 exe
.\build_exe.ps1 -Target cli   # 產生 CLI exe
```

注意：若要建立可執行檔，請在目標環境安裝 `pyinstaller`，並確保 Python 與相依環境設定正確。

範例表達式： `1+2*3`, `(1+2)/3`, `200*2`。

注意：此簡化版本只支援基本四則運算（`+ - * /`）與括號，不支援三角、常數或其他 math 函數。
