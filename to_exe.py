import subprocess
import sys
import os
import tempfile
import zipfile
import urllib.request

UPX_VERSION = "4.2.4"
UPX_URL = f"https://github.com/upx/upx/releases/download/v{UPX_VERSION}/upx-{UPX_VERSION}-win64.zip"
UPX_DIR = os.path.join(tempfile.gettempdir(), f"upx-{UPX_VERSION}-win64")
UPX_EXE = os.path.join(UPX_DIR, "upx.exe")

# download UPX if not already present
if not os.path.isfile(UPX_EXE):
    zip_path = os.path.join(tempfile.gettempdir(), "upx.zip")
    print(f"Downloading UPX {UPX_VERSION}...")
    urllib.request.urlretrieve(UPX_URL, zip_path)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(tempfile.gettempdir())
    print("UPX ready.")

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "Pynter",
    "--icon", "pynter/icon.ico",
    "--add-data", "pynter/icon.ico;pynter",
    "--add-data", "pynter/credit.png;pynter",
    "--upx-dir", UPX_DIR,
    "--upx-exclude", "vcruntime140.dll",
    "--upx-exclude", "ucrtbase.dll",
    "--upx-exclude", "python3.dll",
    "--exclude-module", "numpy",
    "--exclude-module", "pandas",
    "--exclude-module", "matplotlib",
    "--exclude-module", "scipy",
    "--exclude-module", "PIL",
    "--exclude-module", "playwright",
    "--exclude-module", "unittest",
    "--exclude-module", "pydoc",
    "--exclude-module", "doctest",
    "--exclude-module", "xmlrpc",
    "--exclude-module", "multiprocessing",
    "--exclude-module", "asyncio",
    "--exclude-module", "concurrent",
    "--exclude-module", "email",
    "--exclude-module", "html",
    "--exclude-module", "http",
    "--exclude-module", "xml",
    "--exclude-module", "logging",
    "--exclude-module", "csv",
    "--exclude-module", "ssl",
    "--exclude-module", "socket",
    "--exclude-module", "distutils",
    "--exclude-module", "lib2to3",
    "--exclude-module", "setuptools",
    "--exclude-module", "pkg_resources",
    "--exclude-module", "packaging",
    "pynter.py",
]

subprocess.run(cmd, check=True)
