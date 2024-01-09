import z3
import random
import numpy as np

import fuzzing.utils.fuzzMatrix as mt

from config import *

class NonValidMatrix(object):
    def __init__(self, num_input, num_constraint, num_pubinput):
        """Use generation-based Fuzzing to generate non-valid matrix by using random number

        NonValidMatrix, int, int -> None"""
        self.num_input = num_input
        self.num_constraint = num_constraint
        self.num_pubinput = num_pubinput

        self.A = []
        self.B = []
        self.C = []

        self.Z = [1]

    def randomWitness(self):
        """Generate random number as witness
          
        NonValidMatrix -> None"""
        # Create random witness
        for i in range(self.num_input - 1):
            num = random.randint(RANDOM_WITNESS_MIN, RANDOM_WITNESS_MAX)
            self.Z.append(num)

    def randomMatrix(self):
        """Generate random number as matrix
          
        NonValidMatrix -> None"""
        def randval():
            chance = random.randint(0, 10)
            if (chance > 6):
                num = random.randint(RANDOM_MATRIX_MIN, RANDOM_MATRIX_MAX)
            else:
                num = 0

            return num

        for _ in range(self.num_constraint):
            constraintA = []
            for _ in range(self.num_input):
                num = randval()
                constraintA.append(num)
            
            constraintB = []
            for _ in range(self.num_input):
                num = randval()
                constraintB.append(num)

            constraintC = []
            for _ in range(self.num_input):
                num = randval()
                constraintC.append(num)

            self.A.append(constraintA)
            self.B.append(constraintB)
            self.C.append(constraintC)
    
    def returnMatrix(self):
        """Return matrix as the matrix class structure
        
        ValidMatrix -> Matrix"""
        num_variables = self.num_input
        num_constraint = self.num_constraint
        witness = self.Z
        A = self.A
        B = self.B
        C = self.C
        matrix = mt.Matrix(num_variables, num_constraint, witness, A, B, C)

        return matrix

class ValidMatrix(object):
    def __init__(self, num_input, num_constraint, num_pubinput):
        """Use generation-based Fuzzing to generate valid matrix by using random witness with solver matrix
          
        ValidMatrix, int, int -> None"""
        self.num_input = num_input
        self.num_constraint = num_constraint
        self.num_pubinput = num_pubinput
          
        self.A = []
        self.B = []
        self.C = []
        self.Z = [1]

        self.Avar = []
        self.Bvar = []
        self.Cvar = []

    def randomWitness(self):
        """Generate random number as witness
          
        ValidMatrix -> None"""
        # Create random witness
        for i in range(self.num_input - 1):
            num = random.randint(0, 100)
            self.Z.append(num)

    def matrixVariables(self):
        """Create all variables in the R1CS variables
          
        ValidMatrix -> None"""
        # Create variables for A, B, and C
        for i in range(self.num_input):
            name = "a" + str(i)
            locals()[name] = z3.Int(name)
            self.Avar.append(locals()[name])

            name = "b" + str(i)
            locals()[name] = z3.Int(name)
            self.Bvar.append(locals()[name])

            name = "c" + str(i)
            locals()[name] = z3.Int(name)
            self.Cvar.append(locals()[name])

    def solveMatrix(self):
        """Fill out all number in the R1CS matrix
          
        ValidMatrix -> None"""
        s = z3.Solver()
          
        for _ in range(self.num_constraint):
            anotzero = z3.IntVal("0")
            bnotzero = z3.IntVal("0")
            cnotzero = z3.IntVal("0")
               
            aeq = z3.IntVal("0")
            beq = z3.IntVal("0")
            ceq = z3.IntVal("0")
               
            acsame = False

            for i in range(self.num_input):
                ai = self.Avar[i]
                bi = self.Bvar[i]
                ci = self.Cvar[i]
                z = self.Z[i]
                    
                s.add(ai >= 0, bi >= 0, ci >= 0)

                aeq += ai * z
                beq += bi * z
                ceq += ci * z
               
                anotzero += ai
                bnotzero += bi
                cnotzero += ci
                    
                acsame = z3.Or(ai != ci, acsame)
                    
            s.add(z3.simplify(aeq * beq - ceq == 0))
               
            # start extra conditions
            s.add(z3.simplify(anotzero) != 0)
            s.add(z3.simplify(bnotzero) != 0)
            s.add(z3.simplify(cnotzero) != 0)
               
            s.add(z3.simplify(acsame))
            s.add(z3.Not(z3.And(beq == 1, self.Bvar[0] == 1)))
            # end extra conditions

            check = s.check()
            if (check == z3.unsat):
                raise ValueError("No solution")
               
            model = s.model()

            Acs = []
            Bcs = []
            Ccs = []
               
            # Add solution
            solution = False

            for i in range(self.num_input):
                Acs.append(model[self.Avar[i]].as_long())
                Bcs.append(model[self.Bvar[i]].as_long())
                Ccs.append(model[self.Cvar[i]].as_long())

                solution = z3.Or(self.Avar[i] != model[self.Avar[i]], \
                                 self.Bvar[i] != model[self.Bvar[i]], \
                                 self.Cvar[i] != model[self.Cvar[i]], \
                                 solution)

            self.A.append(Acs)
            self.B.append(Bcs)
            self.C.append(Ccs)

            # Avoid same solution
            s.add(z3.simplify(solution))

    def returnMatrix(self):
        """Return matrix as the matrix class structure
        
        ValidMatrix -> Matrix"""
        num_variables = self.num_input
        num_constraint = self.num_constraint
        num_pubinput = self.num_pubinput
        witness = self.Z
        A = self.A
        B = self.B
        C = self.C
        matrix = mt.Matrix(num_variables, num_constraint, num_pubinput, witness, A, B, C)

        return matrix
