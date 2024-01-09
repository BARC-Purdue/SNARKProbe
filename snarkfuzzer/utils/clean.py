import os
import shutil
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

# Home directory
path = os.path.join(parentdir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(parentdir, "branch_model_list.txt")
if os.path.exists(path):
    os.remove(path)
    
path = os.path.join(parentdir, "branch_model_stat.txt")
if os.path.exists(path):
    os.remove(path)
    
path = os.path.join(parentdir, "value_model_watch.txt")
if os.path.exists(path):
    os.remove(path)

##################################################
#                                                #
#          Fuzzing Directory File Clean          #
#                                                #
##################################################

fuzzing_dir = os.path.join(parentdir, "fuzzing")

# home directory
path = os.path.join(fuzzing_dir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# utils directory
path = os.path.join(fuzzing_dir, "utils/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(fuzzing_dir, "utils/random/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(fuzzing_dir, "output.log")
if os.path.exists(path):
    os.remove(path)
    
# genprog directory
path = os.path.join(fuzzing_dir, "genprog/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(fuzzing_dir, "genprog/bellman/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(fuzzing_dir, "genprog/libsnark/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(fuzzing_dir, "genprog/arkworks/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# mfuzzer directory
path = os.path.join(fuzzing_dir, "mfuzzer/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(fuzzing_dir, "mfuzzer/generation/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(fuzzing_dir, "mfuzzer/mutation/__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(fuzzing_dir, "mfuzzer/mutation/mutfile")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(fuzzing_dir, "mfuzzer/mutation/seed_invalid")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(fuzzing_dir, "mfuzzer/mutation/seed_valid")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(fuzzing_dir, "mfuzzer/mutation/args.txt")
if os.path.exists(path):
    os.remove(path)

# output directory
path = os.path.join(fuzzing_dir, "output")
if os.path.exists(path):
    shutil.rmtree(path)
    
##################################################
#                                                #
#       Branch Model Directory File Clean        #
#                                                #
##################################################

branch_dir = os.path.join(parentdir, "model", "branch")

# home directory
path = os.path.join(branch_dir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(branch_dir, "log")
if os.path.exists(path):
    shutil.rmtree(path)

# bellman directory
path = os.path.join(branch_dir, "bellman", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# libsnark directory
path = os.path.join(branch_dir, "libsnark", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# arkworks directory
path = os.path.join(branch_dir, "arkworks", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
##################################################
#                                                #
#          Monitor Directory File Clean          #
#                                                #
##################################################

monitor_dir = os.path.join(parentdir, "model", "monitor")

# home directory
path = os.path.join(monitor_dir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(monitor_dir, "log")
if os.path.exists(path):
    shutil.rmtree(path)

##################################################
#                                                #
#        Value Model Directory File Clean        #
#                                                #
##################################################

value_dir = os.path.join(parentdir, "model", "value")

# home directory
path = os.path.join(value_dir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)
    
path = os.path.join(value_dir, "data")
if os.path.exists(path):
    shutil.rmtree(path)

# checker directory
path = os.path.join(value_dir, "checker", "__pycache__")

if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "checker", "pghr13", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "checker", "groth16", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# extractor directory
path = os.path.join(value_dir, "extractor", "log")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "extractor", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "extractor", "bellman", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "extractor", "libsnark", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "extractor", "arkworks", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# eccmath directory
path = os.path.join(value_dir, "eccmath", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "eccmath", "library", "bls12381", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(value_dir, "eccmath", "library", "bn128", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

##################################################
#                                                #
#           Utils Directory File Clean           #
#                                                #
##################################################

clean_dir = os.path.join(parentdir, "utils")

# home directory
path = os.path.join(clean_dir, "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# montgomery_reduce directory
# None

# ec_coordinate directory
path = os.path.join(clean_dir, "ec_coordinate", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

##################################################
#                                                #
#          Depends Directory File Clean          #
#                                                #
##################################################

depends_dir = os.path.join(parentdir, "depends")

# py_ecc directory
path = os.path.join(depends_dir, "py_ecc", "py_ecc", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(depends_dir, "py_ecc", "py_ecc", "bls", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(depends_dir, "py_ecc", "py_ecc", "fields", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(depends_dir, "py_ecc", "py_ecc", "secp256k1", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(depends_dir, "py_ecc", "py_ecc", "optimized_bn128", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(depends_dir, "py_ecc", "py_ecc", "bn128", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(depends_dir, "py_ecc", "py_ecc", "bls12_381", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

path = os.path.join(depends_dir, "py_ecc", "py_ecc", "optimized_bls12_381", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)

# circl directory
path = os.path.join(depends_dir, "circl", "__pycache__")
if os.path.exists(path):
    shutil.rmtree(path)