import sys
import os

import utils.ec_coordinate.field_elements as fields

from config import *

PY_ECC = os.path.join(ABSPATH, "depends", "py_ecc")

sys.path.append(PY_ECC)
import py_ecc
import py_ecc.utils as utils

def inverse(galois):
    if (isinstance(galois, py_ecc.fields.bn128_FQ)):
        return FQ_inverse(galois)
    elif (isinstance(galois, py_ecc.fields.bn128_FQ2)):
        return FQ2_inverse(galois)
    elif (isinstance(galois, py_ecc.fields.bls12_381_FQ)):
        #TODO: 
        return FQ_inverse(galois)
    elif (isinstance(galois, py_ecc.fields.bls12_381_FQ2)):
        #TODO: 
        return FQ2_inverse(galois)
    else:
        raise Exception

def FQ_inverse(fq):
    num = utils.prime_field_inv(int(fq), fq.field_modulus)
    return fields.FQ(num)

def FQ2_inverse(fq2):
    return fq2.inv()