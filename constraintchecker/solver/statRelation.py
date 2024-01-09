import z3

class StatRelation(object):
    def __init__(self):
        self.private_var = []
        self.public_var = []
        self.variables = []
        
        self.equations = []

    def addStatement(self, statement):
        """Add statement to the solver
        
        StatRelation, list -> None"""
        if (isinstance(statement, z3.z3.BoolRef)):
            statement = [statement]
            
        for st in statement:
            self.equations.append(st)

    def addVariables(self, private_var, public_var):
        """Add public and private variables to the solver
        
        StatRelation, list, list -> None"""
        if (isinstance(private_var, z3.z3.ArithRef)):
            private_var = [private_var]
        for priv in private_var:
            self.private_var.append(priv)
            self.variables.append(priv)

        if (isinstance(public_var, z3.z3.ArithRef)):
            public_var = [public_var]
        for pubv in public_var:
            self.public_var.append(pubv)
            self.variables.append(pubv)