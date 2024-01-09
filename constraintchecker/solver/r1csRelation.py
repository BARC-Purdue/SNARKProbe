import z3
import numpy as np
import json

import solver.constraints as cs
import solver.optimization as opt

from config import *

class R1CSRelation(object):
    def __init__(self, source):
        """Get all equations relation from r1cs martix
        
        Relation, str -> None"""
        self.source = source
        self.constraintClass = None

        self.allocate = []
        self.variables = []
        self.private_var = []
        self.public_var = []

        self.public_value = []
        self.private_value = []

        self.equations = []

        self.setup()

    def __str__(self):
        """Return the string representation of class
        
        Relation -> str"""
        line1 = "Private Variables: " + str(self.private_var)[1:-1] + "\n"
        line2 = "Public Variables: " + str(self.public_var)[1:-1] + "\n"
        line3 = "Public Variables value: " + str(self.public_value)[1:-1] + "\n"
        line4 = "Using the show() method to list the equations\n"

        return line1 + line2 + line3 + line4

    def __repr__(self):
        """Return the string representation of class
        
        Relation -> str"""
        return str(self)
    
    def setup(self):
        """Convert the constraint file to matrix, create variables, and read public variables value
        
        Relation -> None"""
        # Build the constraint matrix from ConstraintBuild class
        cprint.info("Pre-Check if R1CS matrix is valid", 2)
        
        cb = cs.Constraint(CONSTRAINT_FILE)
        constraint = cb.readConstraint()
        
        self.constraintClass = constraint
        
        # Create private variables and public variables
        self.createVars()

        # Read public variables from PUBLICVAR_FILE file
        f = open(PUBLICVAR_FILE)
        nums = f.readlines()
        f.close()

        for num in nums:
            self.public_value.append(int(num.strip("\n'")))
        
        if (len(self.public_value) != len(self.public_var)):
            cprint.error("Number of public variable and public value are not equal")
            raise ValueError("Number of public variable and public value are not equal")
        
        # Read private variables from PRIAUXVAR_FILE file
        f = open(PRIAUXVAR_FILE)
        nums = f.readlines()
        f.close()

        for num in nums:
            self.private_value.append(int(num.strip("\n'")))
        
        if (len(self.private_value) != len(self.private_var)):
            cprint.error("Number of auxiliary inputs is different with number of private variables in R1CS")
            raise IndexError("Number of auxiliary inputs is different with number of private variables in R1CS")
        
    def addAllocate(self, allocate):
        """Add allocate list to to the solver
        
        Relation, list -> None"""
        self.allocate.clear()
        
        for var in allocate:
            self.allocate.append(var)
        
    def readR1CS(self):
        """Read the R1CS matrix, get the number of variables, and create variables
        
        Relation -> None"""
        self.constraints = np.load(self.source)
        f = open(self.source)
        content = f.read()
        f.close()

        self.public_input, self.constraints = json.loads(str(content))
        npsize = np.array(self.constraints)

        self.num_constraints = npsize.shape[1]
        self.num_val = npsize.shape[2]
        
    def createVars(self):
        """Create n variables (based on the R1CS matrix size) for SMT solver

        Relation -> list"""
        constant_variable = [z3.IntVal(1)]
        public_variables = []
        private_variables = []

        for num in range(1, self.constraintClass.public_input + 1):
            name = "pub_" + str(num)
            public_variables.append(z3.Int(name))

        for num in range(1, self.constraintClass.private_input + 1):
            name = "sym_" + str(num)
            private_variables.append(z3.Int(name))

        variables = constant_variable + public_variables + private_variables
        
        self.public_var = public_variables
        self.private_var = private_variables
        self.variables = variables

    def createEquation(self, A, B, C):
        """Convert the R1CS matrix to math equations set for one constraint
        
        Relation -> instance(z3py)"""
        clauseA = 0
        for i in range(self.constraintClass.num_val):
            if (A[i] != 0):
                clauseA = clauseA + A[i] * self.variables[i]

        clauseB = 0
        for i in range(self.constraintClass.num_val):
            if (B[i] != 0):
                clauseB = clauseB + B[i] * self.variables[i]
        
        clauseC = 0
        for i in range(self.constraintClass.num_val):
            if (C[i] != 0):
                clauseC = clauseC + C[i] * self.variables[i]

        if (isinstance(clauseA * clauseB, int) or z3.simplify(clauseA * clauseB).children() == []):
            left = (clauseA * clauseB) % MOD
        else:
            left = (clauseA * clauseB) % MOD

        if (isinstance(clauseC, int) or z3.simplify(clauseC).children() == []):
            right = clauseC
        else:
            right = clauseC % MOD
        
        return z3.simplify(left == right)
        
        # if (isinstance(clauseC, int) or z3.simplify(clauseC).children() == []):
        #     return z3.simplify((clauseA * clauseB) % MOD == clauseC)
        # else:
        #     return z3.simplify((clauseA * clauseB) % MOD == clauseC % MOD)
    
    def getRelation(self):
        """Convert the R1CS matrix to math equations set
        
        Relation -> None"""
        for cons in range(0, self.constraintClass.num_constraints):
            rowA = self.constraintClass.constraint[0][cons]
            rowB = self.constraintClass.constraint[1][cons]
            rowC = self.constraintClass.constraint[2][cons]
            eq = self.createEquation(rowA, rowB, rowC)
            self.equations.append(eq)
    
    def getEquations(self):
        """Return the equation set
        
        Relation -> list"""
        return self.equations

    def show(self):
        for e in self.getEquations():
            print(str(e).replace("\n", "").replace(" ", ""))
            print()

## if __name__ == "__main__":
##     # test case
##     cb = cs.ConstraintBuild("constraints.txt")
##     cb.buildConstraint()
##     constraint = cb.returnConstraint()
## 
##     r = Relation(constraint)
##     r.getRelation()
## 
##     print(r)
##     r.show()