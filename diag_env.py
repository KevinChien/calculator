import sys
import subprocess
import json
import platform

info = {}
info['python_version'] = sys.version
info['executable'] = sys.executable
info['platform'] = platform.platform()

try:
    # pip show pyinstaller
    p = subprocess.run([sys.executable, '-m', 'pip', 'show', 'pyinstaller'], capture_output=True, text=True)
    info['pyinstaller_show'] = p.stdout.strip() if p.stdout.strip() else p.stderr.strip()
except Exception as e:
    info['pyinstaller_show'] = repr(e)

try:
    p2 = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], capture_output=True, text=True)
    info['pip_list'] = json.loads(p2.stdout) if p2.stdout.strip() else []
except Exception as e:
    info['pip_list'] = repr(e)

with open('diag_env_output.txt', 'w', encoding='utf-8') as f:
    json.dump(info, f, indent=2, ensure_ascii=False)

print('WROTE diag_env_output.txt')
