import os

from config import *

LOG_PATH = os.path.join(ABSPATH, "extractor", "log")
if (not os.path.exists(LOG_PATH)):
    os.mkdir(LOG_PATH)

GETLINE_GDB = os.path.join(ABSPATH, "extractor", "log", "getline.gdb")
GETR1CS_GDB = os.path.join(ABSPATH, "extractor", "log", "getr1cs.gdb")
GETPRIAUX_GDB = os.path.join(ABSPATH, "extractor", "log", "getpriaux.gdb")
GETPUBLIC_GDB = os.path.join(ABSPATH, "extractor", "log", "getpublic.gdb")

CONSTRAINT_LOG = os.path.join(ABSPATH, "extractor", "log", "constraints.log")
PRIAUXVAR_LOG = os.path.join(ABSPATH, "extractor", "log", "priauxvar.log")
PUBLICVAR_LOG = os.path.join(ABSPATH, "extractor", "log", "publicvar.log")
CONSTRAINT_PRE = os.path.join(ABSPATH, "extractor", "log", "constraints_pre.txt")