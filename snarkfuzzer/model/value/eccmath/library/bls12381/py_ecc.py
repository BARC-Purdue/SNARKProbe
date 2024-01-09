import copy

from config import *

import sys
sys.path.append(ECCLIBRARY_PATH)
import py_ecc.bls12_381 as bls12_381
import py_ecc.utils as utils

class FF(object):
    def __init__(self, num):
        self.num = num
        
    def __str__(self):
        return str(self.num)
    
    def __repr__(self):
        return str(self)
    
    def __add__(self, other):
        if (isinstance(other, int)):
            return FF(self.num + other)
        elif (isinstance(other, FF)):
            return FF(self.num + other.num)
        else:
            raise Exception
    
    def __mul__(self, other):
        if (isinstance(other, int)):
            return FF(self.num * other)
        elif (isinstance(other, FF)):
            return FF(self.num * other.num)
        elif (isinstance(other, G1) or isinstance(other, G2)):
            return other * self
        else:
            raise Exception
    
    def __pow__(self, other):
        if (isinstance(other, int)):
            return FF(self.num ** other)
        elif (isinstance(other, FF)):
            return FF(self.num ** other.num)
        else:
            raise Exception
        
    def __eq__(self, other):
        if (isinstance(other, int)):
            return self.num == other
        elif (isinstance(other, FF)):
            return self.num == other.num
        else:
            return False
        
    def __ne__(self, other):
        if (isinstance(other, int)):
            return self.num != other
        elif (isinstance(other, FF)):
            return self.num != other.num
        else:
            return False

    def inverse(self):
        inv = utils.prime_field_inv(self.num, bls12_381.curve_order)
        return FF(inv)
        
class G1(object):
    def __init__(self, x, y, z = 1):
        if (int(z) != 1):
            raise Exception
        
        self.g1 = (bls12_381.FQ(int(x)), bls12_381.FQ(int(y)))
        
    def __str__(self):
        return str(self.g1)
    
    def __repr__(self):
        return str(self)
        
    def __add__(self, other):
        if (isinstance(other, G1)):
            g1 = bls12_381.add(self.g1, other.g1)
            if (g1 == None):
                return Ideal()
            return G1(*g1)
        elif (other == 0):
            return copy.deepcopy(self)
        else:
            raise Exception
        
    def __mul__(self, other):
        if (isinstance(other, int)):
            g1 = bls12_381.multiply(self.g1, other)
        elif (isinstance(other, FF)):
            g1 = bls12_381.multiply(self.g1, other.num)
        else:
            raise Exception

        if (g1 == None):
            return Ideal()
        return G1(*g1)

    def __neg__(self):
        return G1(*bls12_381.neg(self.g1))
    
    def __eq__(self, other):
        if (isinstance(other, G1)):
            return self.g1 == other.g1
        else:
            return False
    
    def __ne__(self, other):
        if (isinstance(other, G1)):
            return self.g1 != other.g1
        else:
            return True
    
class G2(object):
    def __init__(self, x, y, z = (1, 0)):
        if (z != (1, 0)):
            raise Exception
        
        if (not isinstance(x, tuple) and (not isinstance(y, tuple))):
            x = x.coeffs
            y = y.coeffs
        
        self.g2 = (bls12_381.FQ2(list(x)), bls12_381.FQ2(list(y)))
        
    def __str__(self):
        return str(self.g2)
    
    def __repr__(self):
        return str(self)
        
    def __add__(self, other):
        if (isinstance(other, G2)):
            g2 = bls12_381.add(self.g2, other.g2)
            if (g2 == None):
                return Ideal()
            return G2(*g2)
        elif (other == 0):
            return copy.deepcopy(self)
        else:
            raise Exception
        
    def __mul__(self, other):
        if (isinstance(other, int)):
            g2 = bls12_381.multiply(self.g2, other)
        elif (isinstance(other, FF)):
            g2 = bls12_381.multiply(self.g2, other.num)
        else:
            raise Exception

        if (g2 == None):
            return Ideal()
        return G2(*g2)
    
    def __eq__(self, other):
        if (isinstance(other, G2)):
            return self.g2 == other.g2
        else:
            return False
    
    def __ne__(self, other):
        if (isinstance(other, G2)):
            return self.g2 != other.g2
        else:
            return True

class GT(object):
    def __init__(self, coeffs):        
        self.gt = bls12_381.FQ12(coeffs)

    def __str__(self):
        return str(self.gt)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        if (isinstance(other, GT)):
            return GT((self.gt + other.gt).coeffs)
        else:
            raise Exception

    def __mul__(self, other):
        if (isinstance(other, GT)):
            return GT((self.gt * other.gt).coeffs)
        else:
            raise Exception

    def __sub__(self, other):
        if (isinstance(other, GT)):
            return GT((self.gt - other.gt).coeffs)
        else:
            raise Exception

    def __div__(self, other):
        if (isinstance(other, GT)):
            return GT((self.gt / other.gt).coeffs)
        else:
            raise Exception

    def __pow__(self, other):
        if (isinstance(other, int)):
            return GT((self.gt ** other).coeffs)
        elif (isinstance(other, FF)):
            return GT((self.gt ** other.num).coeffs)
        else:
            raise Exception

    def __eq__(self, other):
        return self.gt == other.gt

    def __ne__(self, other):
        return self.gt != other.gt

class Ideal(object):
    def __init__(self):
        self.g = None

    def __str__(self):
        return "0"
    
    def __repr__(self):
        return "0"
    
    def __add__(self, other):
        if (isinstance(other, G1) or isinstance(other, G2)):
            return copy.deepcopy(other)
        elif (isinstance(other, Ideal) or other == 0):
            return Ideal()
        else:
            raise Exception
    
    def __eq__(self, other):
        if (isinstance(other, Ideal) or other == 0):
            return True
        else:
            return False
    
    def __ne__(self, other):
        return not(self == other)

def pairing(point1, point2):
    if (isinstance(point1, G1) and isinstance(point2, G2)):
        pair = bls12_381.pairing(point2.g2, point1.g1)
    elif (isinstance(point1, G2) and isinstance(point2, G1)):
        pair = bls12_381.pairing(point1.g2, point2.g1)
    else:
        raise Exception
    
    return GT(pair.coeffs)