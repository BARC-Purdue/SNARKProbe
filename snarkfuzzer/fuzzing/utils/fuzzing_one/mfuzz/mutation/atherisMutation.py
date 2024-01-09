import atheris
import os
import sys
import ast

with atheris.instrument_imports():
    import sys
    import zlib

def matrix2list(matrix):
    """Convert marix to single list
    
    list of list of list -> list"""
    numlst = []
    
    for X in matrix:
        for row in X:
            for num in row:
                numlst.append(num)
    
    return numlst

def list2matrix(numlst, num_constraint, num_variables):
    """Convert single list to marix
    
    list, int, int -> list of list of list"""
    matrix = []
    
    rowlst = []
    for i in range(0, len(numlst), num_variables):
        rowlst.append(numlst[i:i + num_variables])
    
    matrix = []
    for i in range(0, len(rowlst), num_constraint):
        matrix.append(rowlst[i:i + num_constraint])
        
    return matrix

def list2byte(numlst, bit_length):
    """Convert single list to bytes string
    
    list -> bytes"""
    byteset = b''
    for n in numlst:
        intbyte = n.to_bytes(bit_length, 'little')
        byteset += intbyte
        
    return byteset

def byte2list(bb, bit_length):
    """Convert bytes string to single list
    
    bytes -> list"""
    nlist = []
    
    for i in range(0, len(bb), bit_length):
        b = bb[i:i+bit_length]
        num = int.from_bytes(b, "little")
        nlist.append(num)
    
    return nlist

class AtherisMutation(object):
    def __init__(self, src, total):
        """Use atheris to get a new matrix by using mutation fuzzing with seed
        
        AtherisMutation, str"""
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        
        self.src = src
        self.dst = os.path.join(self.abspath, "mutfile")
        
        self.num_variables = -1
        self.num_constraint = -1
        self.r1csmatrix = []
        self.witness = []
        
        self.deep = 0
        self.deepMax = 10
        self.count = 0
        self.total = total
        self.fuzzingset = []
        
        self.bit_length = -1
        self.numlist = []
        self.bytelist = b""
        
        self.setup()
        
    def setup(self):
        """Create directory to store matrix file if necessary and read matrix
        
        AtherisMutation -> None"""
        self.dst = os.path.join(self.abspath, "mutfile")
        if not os.path.exists(self.dst):
            os.mkdir(self.dst)
        
        self.readSeed()
        
    def readSeed(self):
        """Read R1CS matrix from seed file
        
        AtherisMutation -> None"""
        f = open(self.src)
        content = f.read()
        f.close()
            
        info = ast.literal_eval(content)
            
        self.num_variables = info[0]
        self.num_constraint = info[1]
        self.witness = info[2]
        self.r1csmatrix = info[3]
        
        self.bit_length = max(max(max(self.r1csmatrix))).bit_length()
    
    def preconvert(self):
        """Convert the matrix to bytes string
        
        AtherisMutation -> None"""
        numlist = matrix2list(self.r1csmatrix)
        self.numlist = numlist
        self.bytelist = list2byte(numlist, self.bit_length)
    
    def atherisFuzzing(self):
        """Using atheris mutation fuzzing
        
        AtherisMutation -> None"""
        def CustomMutator(data, max_size, seed): 
            """Mutation function for atheris
            
            bytes, int, type -> bytes"""
            try:
                decompressed = zlib.decompress(data)
            except zlib.error:
                decompressed = self.bytelist
            else:
                decompressed = atheris.Mutate(decompressed, len(decompressed))
                
            return zlib.compress(decompressed)

        @atheris.instrument_func
        def InputFunction(data):
            """Input function for atheris
            
            bytes -> None"""
            try:
                decompressed = zlib.decompress(data)
            except zlib.error:
                return
            
            try:
                if (len(decompressed) != len(self.bytelist)):
                    return
                
                newbytelist = byte2list(decompressed, self.bit_length)
                
                if (newbytelist == self.numlist or newbytelist in self.fuzzingset):
                    return
                
                self.deep += 1
                
                if (self.deep == self.deepMax):
                    self.fuzzingset.append(newbytelist)
                    self.writeMatrix(newbytelist, self.count)
                    
                    self.count += 1
                    self.deep = 0
                    
                if (self.count == self.total):
                    raise RuntimeError("Reach the maximum deep of fuzzing")
                
            except UnicodeDecodeError:
                pass
        
        try:
            atheris.Setup(sys.argv, InputFunction, custom_mutator=CustomMutator)
            atheris.Fuzz()
        except:
            pass

    def writeMatrix(self, fuzzbytelist, i = 0):
        """ Write the matrix as Matrix class into file
        
        AtherisMutation, bytes[, int] -> None"""
        srcbase = os.path.basename(self.src)
        
        dst_name = srcbase.split(".")[0] + "_mutation_invalid_" + str(i) + ".txt"
        
        dst = os.path.join(self.dst, dst_name)
        
        r1csmatrix = list2matrix(fuzzbytelist, self.num_constraint, self.num_variables)
        
        f = open(dst, "w")
        f.write(str([self.num_variables, self.num_constraint, self.witness, r1csmatrix]))
        f.close()
        
def main():
    """Main function to call the atheris mutation fuzzing
    
    None -> int"""
    abspath = os.path.dirname(os.path.abspath(__file__))
    argspath = os.path.join(abspath, "args.txt")
    
    f = open(argspath)
    content = f.readlines()
    f.close()
    
    src = content[0].strip("\n")
    total = int(content[1].strip("\n"))
    
    mf = AtherisMutation(src, total)
    mf.preconvert()
    mf.atherisFuzzing()
    
    return 1

if __name__ == "__main__":
    main()