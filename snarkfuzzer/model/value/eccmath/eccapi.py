from config import *

if (ELLIPTICCURVE.upper() == "BLS12-381"):
    if (ECCLIBRARY.upper() == "CIRCL"):
        import model.value.eccmath.library.bls12381.circl as ecc
    elif (ECCLIBRARY.upper() == "PY_ECC"):
        import model.value.eccmath.library.bls12381.py_ecc as ecc
elif (ELLIPTICCURVE.upper() == "BN128"):
    if (ECCLIBRARY.upper() == "PY_ECC"):
        import model.value.eccmath.library.bn128.py_ecc as ecc

FF = ecc.FF
G1 = ecc.G1
G2 = ecc.G2
GT = ecc.GT
Ideal = ecc.Ideal
pairing = ecc.pairing