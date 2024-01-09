#from config import *
ECCLIBRARY_PATH = "/media/fanyo/snark/snarktool/model/depends/circl"
import sys
sys.path.append(ECCLIBRARY_PATH)

import circl_api as bls12_381

class FF(object):
    def __init__(self, num):
        self.num = num
        
    def __str__(self):
        return str(int(self.num))
    
    def __repr__(self):
        return str(self)
    
    def __add__(self, other):
        num = bls12_381.add_ff(self.num, other.num)

        return FF(num)
    
    def __mul__(self, other):
        if (isinstance(other, FF)):
            num = bls12_381.mul_ff(self.num, other.num)

            return FF(num)
        else:
            return other * self
    
    def __pow__(self, other):
        return FF(self.num ** other.num)
        
    def __eq__(self, other):
        return self.num == other.num
    
    def __ne__(self, other):
        return self.num != other.num
        
class G1(object):
    def __init__(self, x, y, z = 1):
        if (int(z) != 1):
            raise Exception
        
        self.g1 = (x, y)
        
    def __str__(self):
        return str(self.g1)
    
    def __repr__(self):
        return str(self)
        
    def __add__(self, other):
        g1 = bls12_381.add_g1(self.g1, other.g1)

        return G1(*g1)
        
    def __mul__(self, other):
        g1 = bls12_381.mul_g1(self.g1, other.num)
        
        return G1(*g1)
    
    def __eq__(self, other):
        return self.g1 == other.g1
    
    def __ne__(self, other):
        return self.g1 != other.g1
    
class G2(object):
    def __init__(self, x, y, z = (1, 0)):
        if (z != (1, 0)):
            raise Exception
        
        self.g2 = (x, y)
        
    def __str__(self):
        return str(self.g2)
    
    def __repr__(self):
        return str(self)
        
    def __add__(self, other):
        g2 = bls12_381.add_g2(self.g2, other.g2)

        return G2(*g2)
        
    def __mul__(self, other):
        g2 = bls12_381.mul_g2(self.g2, other.num)

        return G2(*g2)
    
    def __eq__(self, other):
        return self.g2 == other.g2
    
    def __ne__(self, other):
        return self.g2 != other.g2
