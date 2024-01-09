import os
import shutil
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

# Remove all binary files and log files

# Home directory
path = os.path.join(parentdir, "constraints.txt")
if os.path.exists(path):
    os.remove(path)

path = os.path.join(parentdir, "priauxvar.txt")
if os.path.exists(path):
    os.remove(path)

path = os.path.join(parentdir, "publicvar.txt")
if os.path.exists(path):
    os.remove(path)

path = os.path.join(parentdir, "log.txt")
if os.path.exists(path):
    os.remove(path)
    
path = os.path.join(parentdir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
# utils
path = os.path.join(parentdir, "utils/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
# solver
path = os.path.join(parentdir, "solver/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
# extractor
path = os.path.join(parentdir, "extractor/log")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(parentdir, "extractor/libsnark/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
# domain
path = os.path.join(parentdir, "domain/random/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# gadget
path = os.path.join(parentdir, "gadget/__pycache__")
print(path)
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(parentdir, "gadget/gadgetlib1/__pycache__")
print(path)
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(parentdir, "gadget/gadgetlib2/__pycache__")
print(path)
if os.path.exists(path):
    shutil.rmtree(path)