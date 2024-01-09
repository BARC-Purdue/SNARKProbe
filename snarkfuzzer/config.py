import os

ABSPATH = os.path.dirname(os.path.abspath(__file__))

f = open(os.path.join(ABSPATH, "config.txt"))
content = f.readlines()
f.close()
config = {}
for line in content:
    if (line[0] == "#"):
        continue
    line = line.split("#")[0].strip("\n ")
    if (line == ""):
        continue
    key, value = line.split("=")
    config[key.strip(" ").upper()] = value.strip(" ")

##################################################
#                                                #
#         Tool Overall Global Variables          #
#                                                #
##################################################

# Library parameters
LIBRARY = config["LIBRARY"]
PROTOCOL = config["PROTOCOL"]
VERIFIERTYPE = "STRONG_IC"
ECCLIBRARY = config["ECCLIBRARY"]
ECCLIBRARY_PATH = os.path.join(ABSPATH, "depends", ECCLIBRARY)
ELLIPTICCURVE = config["ELLIPTICCURVE"]
MONTGOMERY_OUTPUT = config["MONTGOMERY_OUTPUT"].upper() == "ON"
MONTGOMERY_REDUCE = os.path.join(ABSPATH, "utils", "montgomery_reduce", LIBRARY.lower())

if (config["LIBRARY_PATH"].upper() == "DEFAULT"):
    if (LIBRARY.upper() == "LIBSNARK"):
        LIBRARY_PATH = os.path.join(ABSPATH, "depends", "libsnark-for-mfuzz", "depends", "libsnark")
    elif (LIBRARY.upper() == "BELLMAN"):
        LIBRARY_PATH = os.path.join(os.path.expanduser("~"), ".cargo", "registry", "src", "github.com-1ecc6299db9ec823", "bellman-0.1.0")
    elif (LIBRARY.upper() == "ARKWORKS"):
        LIBRARY_PATH = os.path.join(ABSPATH, "depends", "groth16", "src")
else:
    LIBRARY_PATH = config["LIBRARY_PATH"]

if (config["COMPILE_PATH"].upper() == "DEFAULT"):
    if (LIBRARY.upper() == "LIBSNARK"):
        COMPILE_PATH = os.path.join(ABSPATH, "depends", "libsnark-for-mfuzz")
    elif (LIBRARY.upper() == "BELLMAN"):
        COMPILE_PATH = os.path.join(ABSPATH, "depends", "bellman-examples")
    elif (LIBRARY.upper() == "ARKWORKS"):
        COMPILE_PATH = os.path.join(ABSPATH, "depends", "groth16")
else:
    COMPILE_PATH = config["COMPILE_PATH"]

##################################################
#                                                #
#        Fuzzing Related Global Variables        #
#                                                #
##################################################

FUZZING_PATH = os.path.join(ABSPATH, "fuzzing")

# Path of log file
#FUZZ_LOG = os.path.join(FUZZING_PATH, "output.log")

# Proportion for each type of fuzzing
GEN_INVALID = int(config["GEN_INVALID"])
GEN_VALID = int(config["GEN_VALID"])
MUT_INVALID = int(config["MUT_INVALID"])
MUT_VALID = int(config["MUT_VALID"])

# Generation valid fuzzing parameters
NUM_INPUT_MIN = int(config["NUM_INPUT_MIN"])
NUM_INPUT_MAX = int(config["NUM_INPUT_MAX"])
NUM_CONSTRAINT_MIN = int(config["NUM_CONSTRAINT_MIN"])
NUM_CONSTRAINT_MAX = int(config["NUM_CONSTRAINT_MAX"])

RANDOM_WITNESS_MIN = int(config["RANDOM_WITNESS_MIN"])
RANDOM_WITNESS_MAX = int(config["RANDOM_WITNESS_MAX"])

# Generation invalid fuzzing parameters
RANDOM_MATRIX_MIN = int(config["RANDOM_MATRIX_MIN"])
RANDOM_MATRIX_MAX = int(config["RANDOM_MATRIX_MAX"])

# Mutation valid fuzzing parameters
MULTIPLY_MIN = int(config["MULTIPLY_MIN"])
MULTIPLY_MAX = int(config["MULTIPLY_MAX"])

# Mutation fuzzing seed parameters
SEED_INPUT = os.path.join(FUZZING_PATH, "seed")

# Fuzzing output parameters
DIR_OUTPUT = os.path.join(FUZZING_PATH, "output")
FUZZING_OUTPUT = os.path.join(FUZZING_PATH, "output", "fuzzmatrix")
PROG_OUTPUT = os.path.join(FUZZING_PATH, "output", "fuzzprog", "code")
BINARY_OUTPUT = os.path.join(FUZZING_PATH, "output", "fuzzprog", "binary")

##################################################
#                                                #
#        Scheme Related Global Variables         #
#                                                #
##################################################

SCHEME_PATH = os.path.join(ABSPATH, "scheme")

# Branch scheme path
SCHEME_BRANCH_PATH = os.path.join(SCHEME_PATH, "branch", LIBRARY.lower() + "_" + PROTOCOL.lower() + ".txt")

# Value scheme path
SCHEME_VALUE_PATH = os.path.join(SCHEME_PATH, "value", LIBRARY.lower() + "_" + PROTOCOL.lower() + ".txt")

##################################################
#                                                #
#      Value Model Related Global Variables      #
#                                                #
##################################################

VALUE_MODEL_PATH = os.path.join(ABSPATH, "model", "value")

RAW_DATA = True

# Extractor Path
VALUE_EXTRACTOR_ABS_PATH = os.path.join(VALUE_MODEL_PATH, "extractor")
VALUE_EXTRACTOR_LOG = os.path.join(VALUE_EXTRACTOR_ABS_PATH, "log")

# Path of log file
VALUE_MODEL_LOG = os.path.join(VALUE_MODEL_PATH, "log")

# Output directory for extracted values
if (RAW_DATA):
    VALUE_DATA_ROOT_PATH = os.path.join(VALUE_MODEL_PATH, "data")
    VALUE_DATA_PATH = os.path.join(VALUE_MODEL_PATH, "data", "refined")
    VALUE_DATA_RAW_PATH = os.path.join(VALUE_MODEL_PATH, "data", "raw")
else:
    VALUE_DATA_PATH = os.path.join(VALUE_MODEL_PATH, "data")

# Value model result log file
VALUE_WATCH_LOG = os.path.join(ABSPATH, "value_model_watch.txt")

##################################################
#                                                #
#     Branch Model Related Global Variables      #
#                                                #
##################################################

BRANCH_MODEL_PATH = os.path.join(ABSPATH, "model", "branch")

# Path of log file
BRANCH_MODEL_LOG = os.path.join(BRANCH_MODEL_PATH, "log")

# Branch model result log file
BRANCH_STAT_LOG = os.path.join(ABSPATH, "branch_model_stat.txt")
BRANCH_LIST_LOG = os.path.join(ABSPATH, "branch_model_list.txt")

##################################################
#                                                #
#        Monitor Related Global Variables        #
#                                                #
##################################################

MONITOR_PATH = os.path.join(ABSPATH, "model", "monitor")

MONITOR_LOG = os.path.join(MONITOR_PATH, "log")

VALGRIND_PATH = "/usr/bin/vgdb"

##################################################
#                                                #
#             Parameters Validation              #
#                                                #
##################################################

# Protocol Validation
protocol_validation = {"LIBSNARK": ["PGHR13", "GROTH16"], \
                       "BELLMAN": ["GROTH16"], \
                       "ARKWORKS": ["GROTH16"]   }
if (LIBRARY.upper() not in protocol_validation):
    raise TypeError("Does not support library " + LIBRARY)
if (PROTOCOL.upper() not in protocol_validation[LIBRARY.upper()]):
    raise TypeError("Does not support protocol " + PROTOCOL + " for library " + LIBRARY)

# ECC Validation
ecc_validation = {"CIRCL": ["BLS12-381"], \
                  "PY_ECC": ["BN128", "BLS12-381"]}
if (ECCLIBRARY.upper() not in ecc_validation):
    raise TypeError("Does not support ECC library " + ECCLIBRARY)
if (ELLIPTICCURVE.upper() not in ecc_validation[ECCLIBRARY.upper()]):
    raise TypeError("Does not support elliptic curve " + ELLIPTICCURVE + " for ECC library " + ECCLIBRARY)