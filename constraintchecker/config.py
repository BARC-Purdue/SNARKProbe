import os

from utils.colorlog import *

ABSPATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ABSPATH, "config.txt")

f = open(CONFIG_PATH)
lines = f.readlines()
f.close()

config_dict = {}
for line in lines:
    if (line == "\n"):
        continue
    key, value = line.split(" = ")
    config_dict[key] = value.strip("\n")

# EXTRACTION
if (config_dict["EXTRACTION"] == "OFF"):
    EXTRACTION = False
elif (config_dict["EXTRACTION"] == "ON"):
    EXTRACTION = True
else:
    raise KeyError("EXTRACTION option " + config_dict["EXTRACTION"] + " is not valid; choose from ON/OFF")

# BINARY_FILE_PATH
# BINARY_FILE_PATH = config_dict["BINARY_FILE_PATH"]

# LIBRARY_CHOICE
LIBRARY_CHOICE = config_dict["LIBRARY_CHOICE"]

# CURVE_CHOICE
CURVE_CHOICE = config_dict["CURVE_CHOICE"]

# DOMAIN_FUZZING
if (config_dict["DOMAIN_FUZZING"] == "OFF"):
    DOMAIN_FUZZING = False
elif (config_dict["DOMAIN_FUZZING"] == "ON"):
    DOMAIN_FUZZING = True
else:
    raise KeyError("DOMAIN_FUZZING option " + config_dict["DOMAIN_FUZZING"] + " is not valid; choose from ON/OFF")
    
# DOMAIN_FUZZING_TOOL
DOMAIN_FUZZING_TOOL = config_dict["DOMAIN_FUZZING_TOOL"]

# DOMAIN_TEST_SIZE
DOMAIN_TEST_SIZE = config_dict["DOMAIN_TEST_SIZE"]

# OPT_TIME
OPT_TIME = float(config_dict["OPT_TIME"])

# QF_BV
if (config_dict["QF_BV"] == "OFF"):
    QF_BV = False
elif (config_dict["QF_BV"] == "ON"):
    QF_BV = True
else:
    raise KeyError("QF_BV option " + config_dict["QF_BV"] + " is not valid; choose from ON/OFF")

# LOGFILE
if (config_dict["LOGFILE"] != "OFF"):
    LOGFILE = config_dict["LOGFILE"]
else:
    LOGFILE = None

# CONSTRAINT_FILE
CONSTRAINT_FILE = os.path.join(ABSPATH, "constraints.txt")

# PRIAUXVAR_FILE
PRIAUXVAR_FILE = os.path.join(ABSPATH, "priauxvar.txt")

# PUBLICVAR_FILE
PUBLICVAR_FILE = os.path.join(ABSPATH, "publicvar.txt")

# LOGGING_DATE
LOGGING_DATE = False

# MOD
if (CURVE_CHOICE.upper() == "BN128"):
    MOD = 21888242871839275222246405745257275088548364400416034343698204186575808495617
elif (CURVE_CHOICE.upper() == "ALT_BN128"):
    MOD = 21888242871839275222246405745257275088548364400416034343698204186575808495617
else:
    raise KeyError("Does not support elliptic curve: " + CURVE_CHOICE)

# logging
cprint = PrintColor(LOGFILE)