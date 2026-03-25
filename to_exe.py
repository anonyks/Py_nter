import subprocess
import sys

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "Pynter",
    "--icon", "pynter/icon.ico",
    "--add-data", "pynter/icon.ico;pynter",
    "--add-data", "pynter/credit.png;pynter",
    "pynter.py",
]

subprocess.run(cmd, check=True)
