import sys

from config import *

PY_ECC = os.path.join(ABSPATH, "depends", "py_ecc")

sys.path.append(PY_ECC)
import py_ecc.fields as fields

if (ELLIPTICCURVE.upper() == "BN128"):
    FQ = fields.bn128_FQ
    FQ2 = fields.bn128_FQ2
elif (ELLIPTICCURVE.upper() == "BLS12-381"):
    FQ = fields.bls12_381_FQ
    FQ2 = fields.bls12_381_FQ2
else:
    raise Exception