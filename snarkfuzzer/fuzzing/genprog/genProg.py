import z3
import os

import fuzzing.utils.fuzzMatrix as mt
import utils.modelsource as ms

from config import *

if (LIBRARY.upper() == "BELLMAN"):
    import fuzzing.genprog.bellman.bellmanProg as prog
elif (LIBRARY.upper() == "LIBSNARK"):
    import fuzzing.genprog.libsnark.libsnarkProg as prog
elif (LIBRARY.upper() == "ARKWORKS"):
    import fuzzing.genprog.arkworks.arkworksProg as prog
else:
    raise Exception

class ProGenerator(object):
    def __init__(self, name):
        self.name = name
        
        self.num_variables = []
        self.num_constraint = []
        self.num_pubinput = -1
        self.witness = []
        self.r1csmatrix = []
      
        self.variables = []
        self.constraints = []
        self.witnessvalue = {}  
        
    def readMatrixFromFile(self):
        """Rad the matrix information from provided file
        
        ProGenerator -> None"""
        matrix = mt.Matrix(os.path.join(FUZZING_OUTPUT, self.name + ".txt"))
        self.num_variables = matrix.num_variables
        self.num_constraint = matrix.num_constraint
        self.num_pubinput = matrix.num_pubinput
        self.witness = matrix.witness
        self.r1csmatrix = matrix.r1csmatrix

    # def readMatrixFromClass(self, matrixClass : mt.Matrix):
    #     """Rad the matrix information from RandomMatrix class
        
    #     ProGenerator, RandomMatrix -> None"""
    #     self.num_variables = matrixClass.num_variables
    #     self.num_constraint = matrixClass.num_constraint
    #     self.num_pubinput = matrixClass.num_pubinput
    #     self.witness = matrixClass.witness
    #     self.r1csmatrix = matrixClass.r1csmatrix

    def setvariables(self):
        """Create variables in the R1CS matrix
        
        RandomMatrix -> None"""
        self.variables.append(z3.IntVal(1))
        
        for i in range(1, self.num_variables):
            self.variables.append(z3.Int("sym_" + str(i - 1)))
        
        for i in range(1, self.num_variables):
            var = self.variables[i]
            val = self.witness[i]
            self.witnessvalue[var] = val
    
    def getRelation(self):
        """Convert the R1CS matrix to math equations set
        
        RandomMatrix -> None"""
        def createEquation(A, B, C):
            """Convert the R1CS matrix to math equations set for one constraint
            
            RandomMatrix -> tuple of instance(z3py)"""
            clauseA = z3.IntVal("0")
            for i in range(self.num_variables):
                if (A[i] != 0):
                    clauseA = clauseA + A[i] * self.variables[i]

            clauseB = z3.IntVal("0")
            for i in range(self.num_variables):
                if (B[i] != 0):
                    clauseB = clauseB + B[i] * self.variables[i]
            
            clauseC = z3.IntVal("0")
            for i in range(self.num_variables):
                if (C[i] != 0):
                    clauseC = clauseC + C[i] * self.variables[i]
            
            return z3.simplify(clauseA), z3.simplify(clauseB), z3.simplify(clauseC)

        for cons in range(0, self.num_constraint):
            gate = createEquation(self.r1csmatrix[0][cons], self.r1csmatrix[1][cons], self.r1csmatrix[2][cons])
            self.constraints.append(gate)
            
    def generateProg(self):
        """Generate libsnark program file
        
        RandomMatrix, str -> None"""
        if (LIBRARY.upper() == "BELLMAN"):
            pg = prog.BellmanGenerator(self.name, self)
            lines, varnames = pg.generateProg()

            pc = prog.BellmanCompiler(self.name)
            filepath = pc.compile()

        elif (LIBRARY.upper() == "LIBSNARK"):
            pg = prog.LibsnarkGenerator(self.name, self)
            lines, varnames = pg.generateProg()
            
            pc = prog.LibsnarkCompiler(self.name)
            filepath = pc.compile()

        elif (LIBRARY.upper() == "ARKWORKS"):
            pg = prog.ArkworksGenerator(self.name, self)
            lines, varnames = pg.generateProg()
            
            pc = prog.ArkworksCompiler(self.name)
            filepath = pc.compile()
        else:
            raise Exception

        fileparams = [ms.FileParam(filepath, lines[0], varnames[0]),
                      ms.FileParam(filepath, lines[1], varnames[1]),
                      ms.FileParam(filepath, lines[2], varnames[2])]
        
        return fileparams

        

