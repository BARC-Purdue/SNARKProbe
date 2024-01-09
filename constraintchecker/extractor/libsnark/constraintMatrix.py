import numpy as np

# class Constraint(object):
#     def __init__(self, source, public_input, private_input, num_constraints, constraint):
#         """Constraint conatins variable for R1CS constraint
        
#         Constraint, str, int, int, int, list"""
#         self.source = source

#         self.public_input = public_input
#         self.private_input = private_input
#         self.num_val = 1 + public_input + private_input
#         self.num_constraints = num_constraints

#         self.constraint = constraint

#     def __str__(self):
#         """Return the string of class represnetation
        
#         Constraint -> str"""
#         line1 = "Number of public input: " + str(self.public_input) + "\n"
#         line2 = "Number of private input: " + str(self.private_input) + "\n"
#         line3 = "Number of variables: " + str(self.num_val) + "\n"
#         line4 = "Number of constraint: " + str(self.num_constraints) + "\n"
#         line5 = "Using the show() method to show the matrix\n"

#         return line1 + line2 + line3 + line4 + line5

#     def __repr__(self):
#         """Return the string of class represnetation
        
#         Constraint -> str"""
#         return str(self)

#     def show(self):
#         """Display R1CS matrix in python list format
        
#         Constraint -> None"""
#         for matrix in self.constraint:
#             for line in matrix:
#                 print(list(line))
#             print()

class ConstraintBuild(object):
    def __init__(self, source):
        """ConstraintBuild read for libsnark library (currently not work for other zk-SNARKs libraries)
        
        ConstraintBuild, str, str -> None"""
        self.source = source

        self.public_input = -1
        self.private_input = -1
        self.num_constraints = -1

        self.constraintlist = []
        self.constraint = [[], [], []]
        self.constraint_size = ()

        self.setup()

    def setup(self):
        """Read constraint file and number of input and constraints and create log directory if necessary
        
        ConstraintBuild -> None"""
        self.constraintlist = self.readConstraints()

        self.public_input = self.constraintlist[0]
        self.private_input = self.constraintlist[1]
        self.num_constraints = self.constraintlist[2]

        self.num_val = 1 + self.public_input + self.private_input

    def readConstraints(self):
        """Read libsnark variable GDB log r1cs_constraint_system<FieldT> from pb.get_constraint_system()
        
        ConstraintBuild -> list"""
        constraintlist = []

        f = open(self.source)
        content = f.readlines()
        f.close()
        
        for line in content:
            constraintlist.append(int(line.strip("\n")))

        return constraintlist

    def buildConstraint(self):
        """Convert libsnark GDB log format to R1CS constraint matrix
        
        ConstraintBuild -> None"""
        i = 0
        i += 2
        i += 1

        for nc in range(0, self.num_constraints):
            for x in range(3):
                gateX = [0 for i in range(self.num_val)]
                num_sub = self.constraintlist[i]
                i += 1
                for nvar in range(0, num_sub):
                    place = self.constraintlist[i]
                    i += 1
                    value = self.constraintlist[i]
                    i += 1
                    gateX[place] = value
                
                self.constraint[x].append(gateX)
        
        self.constraint_size = np.array(self.constraint).shape

    # def returnConstraint(self):
    #     """Return R1CS constraint in Constraint class
        
    #     ConstraintBuild -> Constraint"""
    #     source = self.source
    #     public_input = self.public_input
    #     private_input = self.private_input
    #     num_constraints = self.num_constraints
    #     constraint = self.constraint

    #     return Constraint(source, public_input, private_input, num_constraints, constraint)

    def show(self):
        """Display R1CS matrix in python list format
        
        ConstraintBuild -> None"""
        for matrix in self.constraint:
            for line in matrix:
                print(list(line))
            print()

## if __name__ == "__main__":
##     # test case
##     cb = ConstraintBuild("constraints.txt")
##     cb.buildConstraint()
##     cb.show()
