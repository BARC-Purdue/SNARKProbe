import ast
import numpy as np

class Matrix(object):
    def __init__(self, *args):
        """Matrix class to store number of variable, constraint, and witness
        
        Matrix, *args -> None"""
        self.num_variables = -1
        self.num_constraint = -1
        self.num_pubinput = -1
        self.witness = []
        self.r1csmatrix = []

        if (len(args) == 1):
            filename = args[0]
            self.readFromFile(filename)
        
        elif (len(args) == 5):
            num_variables, num_constraint, num_pubinput, witness, matrixabc = args
            A, B, C = matrixabc
            self.readFromInput(num_variables, num_constraint, num_pubinput, witness, A, B, C)

        elif (len(args) == 7):
            num_variables, num_constraint, num_pubinput, witness, A, B, C = args
            self.readFromInput(num_variables, num_constraint, num_pubinput, witness, A, B, C)
    
    def __eq__(self, other):
        """Compare if two matrix are equal
        
        Matrix, Matrix -> bool"""
        return self.num_variables == other.num_variables and \
               self.num_constraint == other.num_constraint and \
               self.witness == other.witness and \
               self.r1csmatrix == other.r1csmatrix
            
    def readFromFile(self, filename):
        """Read matrix data from file
        
        Matrix, str -> None"""
        f = open(filename)
        content = f.read()
        f.close()
            
        info = ast.literal_eval(content)
            
        self.num_variables = info[0]
        self.num_constraint = info[1]
        self.num_pubinput = info[2]
        self.witness = info[3]
        self.r1csmatrix = info[4]

    def readFromInput(self, num_variables, num_constraint, num_pubinput, witness, A, B, C):
        """Read matrix data from user provided variables
        
        Matrix, int, int, list, list, list -> None"""
        self.num_variables = num_variables
        self.num_constraint = num_constraint
        self.num_pubinput = num_pubinput
        self.witness = witness
        self.r1csmatrix = [A, B, C]

    def writeToFile(self, dst):
        """Write matrix data to dst file
        
        Matrix, str -> None"""
        f = open(dst, "w")
        f.write(str([self.num_variables, self.num_constraint, self.num_pubinput, self.witness, self.r1csmatrix]))
        f.close()
        
    def verify(self):
        """Use numpy to calculate if R1CS matrix is valid
          
        Matrix -> None"""
        Anp = np.array(self.r1csmatrix[0])
        Bnp = np.array(self.r1csmatrix[1])
        Cnp = np.array(self.r1csmatrix[2])
        Znp = np.array(np.transpose((self.witness)))

        AZ = np.matmul(Anp, Znp)
        BZ = np.matmul(Bnp, Znp)
        CZ = np.matmul(Cnp, Znp)

        verify = np.multiply(AZ, BZ) - CZ
          
        return np.sum(verify) == 0

    def printMatrix(self):
        """Print list as matrix format
        
        Matrix -> None"""
        def printX(X):
            for x in X:
                print(x)

        printX(self.r1csmatrix[0])
        print()
        printX(self.r1csmatrix[1])
        print()
        printX(self.r1csmatrix[2])