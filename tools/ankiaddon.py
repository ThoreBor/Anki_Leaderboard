import zipfile
import os
from pathlib import Path
import shutil

root = Path(__file__).parents[1]

# create output folder
if not os.path.exists(f"{root}/releases"):
   os.makedirs(f"{root}/releases")

# remove pycache
shutil.rmtree(f"{root}/forms/pyqt5UI/__pycache__", ignore_errors=True)
shutil.rmtree(f"{root}/forms/pyqt6UI/__pycache__", ignore_errors=True)
shutil.rmtree(f"{root}/src/__pycache__", ignore_errors=True)

# create .ankiaddon

data = [
   "-c",
   f"{root}/releases/AnkiLeaderboard.ankiaddon",
   f"{root}/__init__.py",
   f"{root}/config.json",
   f"{root}/manifest.json",
   f"{root}/License.txt",
   f"{root}/designer",
   f"{root}/forms",
   f"{root}/src",
   ]

zipfile.main(data)