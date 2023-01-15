import zipfile
import os
from os.path import dirname, join, realpath
import shutil
from version import version

# run from root

# remove pycache from forms
qt5 = join(dirname(realpath(__file__)), "forms/pyqt5UI/__pycache__")
qt6 = join(dirname(realpath(__file__)), "forms/pyqt6UI/__pycache__")
shutil.rmtree(qt5, ignore_errors=True)
shutil.rmtree(qt6, ignore_errors=True)

# find files
pyFiles = [file for file in os.listdir() if file.endswith('.py') and file != "ankiaddon.py"]
jsonFiles = [file for file in os.listdir() if file.endswith('.json') and file != "meta.json"]

# create .ankiaddon
data = ["-c", f"AnkiLeaderboard_{version}.ankiaddon", "License.txt", "designer", "forms"]
for i in pyFiles:
   data.append(i)
for i in jsonFiles:
   data.append(i)
zipfile.main(data)