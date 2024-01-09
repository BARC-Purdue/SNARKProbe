import ast
import numpy as np

class Matrix(object):
    def __init__(self, *args):
        """Matrix class to store number of variable, constraint, and witness
        
        Matrix, *args -> None"""
        self.num_variables = -1
        self.num_constraint = -1
        self.witness = []
        self.r1csmatrix = []

        if (len(args) == 1):
            filename = args[0]
            self.readFromFile(filename)
        
        elif (len(args) == 4):
            num_variables, num_constraint, witness, matrixabc = args
            A, B, C = matrixabc
            self.readFromInput(num_variables, num_constraint, witness, A, B, C)

        elif (len(args) == 6):
            num_variables, num_constraint, witness, A, B, C = args
            self.readFromInput(num_variables, num_constraint, witness, A, B, C)
            
    def readFromFile(self, filename):
        """Read matrix data from file
        
        Matrix, str -> None"""
        f = open(filename)
        content = f.read()
        f.close()
            
        info = ast.literal_eval(content)
            
        self.num_variables = info[0]
        self.num_constraint = info[1]
        self.witness = info[2]
        self.r1csmatrix = info[3]

    def readFromInput(self, num_variables, num_constraint, witness, A, B, C):
        """Read matrix data from user provided variables
        
        Matrix, int, int, list, list, list -> None"""
        self.num_variables = num_variables
        self.num_constraint = num_constraint
        self.witness = witness
        self.r1csmatrix = [A, B, C]

    def writeToFile(self, dst):
        """Write matrix data to dst file
        
        Matrix, str -> None"""
        f = open(dst, "w")
        f.write(str([self.num_variables, self.num_constraint, self.witness, self.r1csmatrix]))
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
        def printX(X):
            for x in X:
                print(x)

        printX(self.r1csmatrix[0])
        print()
        printX(self.r1csmatrix[1])
        print()
        printX(self.r1csmatrix[2])