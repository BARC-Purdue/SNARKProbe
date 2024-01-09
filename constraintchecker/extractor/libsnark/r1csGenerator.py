import os

import extractor.libsnark.getLine as gl
import extractor.libsnark.montTrans as mt
import extractor.libsnark.varExtractor as ve

from config import *

class R1CSGenerator(object):
    def __init__(self, src):
        """R1CSGenerator, str -> None"""
        self.src = src
        self.dst_cs = CONSTRAINT_FILE
        self.dst_aux = PRIAUXVAR_FILE
        self.dst_pub = PUBLICVAR_FILE
        
        self.setup()

        self.line = self.getline()

        self.ve = ve.VarExtractor(self.src, self.line)
        self.mt = mt.MontTrans(self.dst_cs, self.dst_aux, self.dst_pub)

    def setup(self):
        """Check if source binary exists and raise error if doesn't exist

        R1CSGenerator -> None"""
        if (not os.path.exists(self.src)):        
            cprint.error("\tzk-SNARKs binary file does not exist: " + self.src)
            raise FileNotFoundError("zk-SNARKs binary file does not exists")
        
        cprint.info("Save constraint matrix to " + CONSTRAINT_FILE, 1)
        cprint.info("Save auxiliary variable(s) to " + PRIAUXVAR_FILE, 1)
        cprint.info("Save public variable(s) to " + PUBLICVAR_FILE, 1)

    def getline(self):
        """Using GetLine class to find the breakpoint line for source binary file
        
        R1CSGenerator -> int"""
        lineClass = gl.GetLine(self.src)
        lineClass.gdbscript()
        lineClass.runscript()
        
        line = lineClass.getline()
        
        cprint.info("Set GDB breakpoint at line " + str(line) + " to extract constraint variable", 1)
        
        return line

    def gdbScript(self):
        """Using VarExtractor class to get the original formatted GDB log
        
        R1CSGenerator -> None"""
        cprint.info("Extract constraint, public variable(s) value, and auxiliary variable(s) value", 2)
        
        self.ve.gdbscript()
        self.ve.runscript()
        self.ve.formatlog()

    def translate(self):
        """Convert the original formatted GDB log to integer format r1cs list and matrix
        
        R1CSGenerator -. None"""
        cprint.info("Convert montgomery representation into integer format", 2)
        
        self.mt.readlog()
        self.mt.translateAll()
        self.mt.r1csMatrix()
        self.mt.writer1cslst()

## if __name__ == "__main__":
##     # test case
##     src = "/media/fanyo/DATA/Research/zk-SNARKs/tool/depends/libsnark-tutorial/build/src/range"
##     dst = os.path.join(ABSPATH, "constraints.txt")
## 
##     r1cse = R1CSGenerator(src, dst)
##     r1cse.getr1cs()
