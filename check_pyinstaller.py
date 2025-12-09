import importlib
import json

info = {}
try:
    m = importlib.import_module('PyInstaller')
    info['file'] = getattr(m, '__file__', None)
    info['version'] = getattr(m, '__version__', None)
except Exception as e:
    info['error'] = str(e)

with open('pyinst_check.json', 'w', encoding='utf-8') as f:
    json.dump(info, f, indent=2, ensure_ascii=False)
print('WROTE pyinst_check.json')
