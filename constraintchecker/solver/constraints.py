import ast

class Constraint(object):
    def __init__(self, source):
        """Constraint conatins variable for R1CS constraint
        
        Constraint, str, int, int, int, list"""
        self.source = source

        self.public_input = -1
        self.private_input = -1
        self.num_val = -1#1 + public_input + private_input
        self.num_constraints = -1

        self.constraint = []
        
        self.read = False

    def __str__(self):
        """Return the string of class represnetation
        
        Constraint -> str"""
        if (not self.read):
            return None
            
        line1 = "Number of public input: " + str(self.public_input) + "\n"
        line2 = "Number of private input: " + str(self.private_input) + "\n"
        line3 = "Number of variables: " + str(self.num_val) + "\n"
        line4 = "Number of constraint: " + str(self.num_constraints) + "\n"
        line5 = "Using the show() method to show the matrix\n"

        return line1 + line2 + line3 + line4 + line5

    def __repr__(self):
        """Return the string of class represnetation
        
        Constraint -> str"""
        return str(self)

    def readConstraint(self):
        """Read constraint from files and return class
        
        Constraint -> Constraint"""
        self.read = True
        
        f = open(self.source)
        content = f.readlines()
        f.close()
        
        public_input = int(content[0].strip("\n"))
        private_input = int(content[1].strip("\n"))
        num_constraints = int(content[2].strip("\n"))
        res = ast.literal_eval(content[3].strip("\n"))
        constraint = res
        
        self.public_input = public_input
        self.private_input = private_input
        self.num_constraints = num_constraints
        self.constraint = constraint
        self.num_val = 1 + public_input + private_input
        
        return self

    def show(self):
        """Display R1CS matrix in python list format
        
        Constraint -> None"""
        for matrix in self.constraint:
            for line in matrix:
                print(list(line))
            print()