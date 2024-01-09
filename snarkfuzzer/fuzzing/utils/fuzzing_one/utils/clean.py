import os
import shutil
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

# Remove all binary files and log files

# utils directory
path = os.path.join(parentdir, "utils/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# Home directory
path = os.path.join(parentdir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
# fuzzing directory
path = os.path.join(parentdir, "fuzzing/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(parentdir, "fuzzing/generation/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(parentdir, "fuzzing/mutation/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(parentdir, "fuzzing/mutation/mutfile")
if os.path.exists(path):
    shutil.rmtree(path)

# fuzzmatrix directory
path = os.path.join(parentdir, "fuzzmatrix")
if os.path.exists(path):
    shutil.rmtree(path)
    
# genprog directory
path = os.path.join(parentdir, "genprog/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)