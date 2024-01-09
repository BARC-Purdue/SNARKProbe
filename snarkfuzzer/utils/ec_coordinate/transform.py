import sys
import os

import utils.ec_coordinate.field_elements as fields
import utils.ec_coordinate.inverse as inv

from config import *

def to_affine(ec):
    x, y, z = ec

    if (isinstance(x, int) and isinstance(x, int)):
        ectype = "FQ"
    elif ((isinstance(x, list) and isinstance(x, list)) or \
          (isinstance(x, tuple) and isinstance(x, tuple))):
        ectype = "FQ2"
    else:
        raise Exception

    if (ectype == "FQ"):
        x_ff = fields.FQ(x)
        y_ff = fields.FQ(y)
        z_ff = fields.FQ(z)
    elif (ectype == "FQ2"):
        x_ff = fields.FQ2(list(x))
        y_ff = fields.FQ2(list(y))
        z_ff = fields.FQ2(list(z))
    else:
        raise Exception

    z_inv_ff = inv.inverse(z_ff)

    x_affine = x_ff * z_inv_ff ** 2
    y_affine = y_ff * z_inv_ff ** 3

    if (ectype == "FQ"):
        return int(x_affine), int(y_affine)
    elif (ectype == "FQ2"):
        x1_affine, x2_affine = x_affine.coeffs
        y1_affine, y2_affine = y_affine.coeffs

        return (x1_affine, x2_affine), (y1_affine, y2_affine)



