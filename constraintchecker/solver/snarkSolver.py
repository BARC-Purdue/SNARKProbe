import subprocess
import os
import z3

import solver.z3Solver as z3p
import solver.statRelation as sr
import solver.r1csRelation as rr
import solver.gadgetRelation as gr
import solver.optimization as opt

from config import *

class SNARKSolver(object):
    def __init__(self):
        """A SMT solver to compare if two equations are equal
        
        SNARKSolver, str -> None"""
        cprint.info("Use SMT Solver to compare if R1CS matrix equals to statement function")
    
        self.statrelation = None
        self.r1csrelation = None
        self.gadgetrelation = None

        self.statvarrange = {}
        self.r1csvarrange = {}
        
        self.input_sizes = 0

        self.setup()
    
    def setup(self):
        """Build the Constraint and Relation and check R1CS constraint
        
        SNARKSolver -> None"""
        # Build statement relation class
        cprint.info("Build the equation(s) in statement function", 1)
        
        self.statrelation = sr.StatRelation()

        # Build r1cs relation class
        cprint.info("Build the equation(s) in R1CS matrix", 1)
        
        self.r1csrelation = rr.R1CSRelation(CONSTRAINT_FILE)
        self.r1csrelation.getRelation()

        # Build gadget relation class
        
        cprint.info("Build the gadget relation(s) if necessary", 1)
        self.gadgetrelation = gr.GadgetRelation()

        # Build r1cs variables range
        cprint.info("Build the range of all variances", 1)
        
        for var in self.r1csrelation.variables[1:]:
            self.r1csvarrange[var] = z3.And(var >= 0, var < MOD)

        # Optimize variables range
        cprint.info("Optimize variances in equation(s) to reduce the SMt Solver time complexity", 1)
        
        count = self.optrange()
        
        # check if r1cs has valid solution
        cprint.info("Pre-Check if R1CS matrix and statement function are valid", 1)
        
        check = self.r1csvalid()
        
        if (check != z3.sat):
            cprint.error("R1CS constraints do not have valid solution in auxiliary and primary inputs")
            raise ValueError("R1CS constraints do not have valid solution in auxiliary and primary inputs")

    def optrange(self):
        """Optimize the range of the variables in R1CS constraints 
        
        SNARKSolver -> int"""
        count = 0

        for equation in self.r1csrelation.equations:
            improved, var, range = opt.optrange(equation)
            count += improved

            if (improved):
                self.r1csvarrange[var] = range
        
        return count
    
    def r1csvalid(self):
        """Check if the auxiliary and primary inputs are valid (sat) in R1CS constraints
        
        SNARKSolver -> z3.z3.BoolRef"""
        cprint.info("Check if R1CS matrix and statement function have common solution", 2)
        
        s = z3p.Solver()
        s.add(self.r1csrelation, self.r1csvarrange, self.gadgetrelation, domain = False)

        # link public input with public value
        for i in range(self.r1csrelation.constraintClass.public_input):
            s.add(self.r1csrelation.public_var[i] == self.r1csrelation.public_value[i])

        # link private input with private value
        for i in range(self.r1csrelation.constraintClass.private_input):
            s.add(self.r1csrelation.private_var[i] == self.r1csrelation.private_value[i])

        check = s.check()
        
        return check

    def addAllocate(self, allocate):
        """Add allocate list to to the solver
        
        SNARKSolver, list -> None"""
        self.r1csrelation.addAllocate(allocate)
        
    def set_input_sizes(self, size):
        """Set input size in the solver
        
        SNARKSolver, int -> None"""
        self.input_sizes = size
    
    #def addVariables(self, private_var, public_var):
    def addVariables(self, variables):
        """Add public and private variables to the solver
        
        SNARKSolver, list, list -> None"""
        public_var = variables[:self.input_sizes]
        private_var = variables[self.input_sizes:]
        
        self.statrelation.addVariables(private_var, public_var)
        
        for var in self.statrelation.variables:
            if (var == None):
                continue
            if (type(var) == z3.z3.BoolRef):
                continue
            if (var not in self.statvarrange.keys()):
                self.statvarrange[var] = z3.And(var >= 0, var < MOD)
        
        if (len(self.statrelation.private_var) > len(self.r1csrelation.private_var)):
            cprint.error("Number of private variable(s) in R1CS and statement are not euqal")
            raise IndexError("Number of private variable(s) in R1CS and statement are not euqal")
        
        if (len(self.statrelation.public_var) != len(self.r1csrelation.public_var)):
            cprint.error("Number of public variable(s) in R1CS and statement are not equal")
            raise IndexError("Number of public variable(s) in R1CS and statement are not equal")
        
        # self.statrelation.addVariables(private_var, public_var)

        # for var in self.statrelation.variables:
        #     if (var not in self.statvarrange.keys()):
        #         self.statvarrange[var] = z3.And(var >= 0, var < MOD)

        # # Check if number of variables are equal
        # if (len(self.statrelation.private_var) > len(self.r1csrelation.private_var)):
        #     cprint.error("Statement has more private variables than R1CS")
        #     raise IndexError("Statement has more private variables than R1CS")

        # if (len(self.statrelation.public_var) != len(self.r1csrelation.public_var)):
        #     cprint.error("Number of public variables in R1CS and statement are not equal")
        #     raise IndexError("Number of public variables in R1CS and statement are not equal")
        
    def addStatement(self, statement):
        """Add statement to the solver
        
        SNARKSolver, list -> None"""
        self.statrelation.addStatement(statement)
    
    def addRange(self, var, range):
        """Add range for statement variables
        
        SNARKSolver, z3.z3.ArithRef, z3.z3.BoolRef -> None"""
        if (var not in self.statrelation.variables):
            cprint.error("Statement equation does not has vaiable " + str(var))
            raise KeyError("Statement equation does not has vaiable " + str(var))
        
        o = z3p.Optimize()
        
        o.add(self.statvarrange[var])
        o.add(range)

        minval, maxval = o.minmax(var)
        
        self.statvarrange[var] = z3.And(var >= minval, var <= maxval)

    def addGadget(self, name):
        """Add gadget rule to the solver
        
        SNARKSolver, str -> None"""
        self.gadgetrelation.addGadget(name, self.r1csrelation)

    def matchComparison(self):
        """Compare if r1cs equations and statement equations are same
        
        SNARKSolver -> tuple of z3.z3.CheckSatResult"""
        cprint.info("Compare if Statement function is equal to the function in R1CS matrix")
        
        satcheck = []
        
        # ===== Pre Check =====        
        # pre-test to see if private and public variables value in r1cs satisfy statement equations
        s = z3p.Solver()

        s.add(self.statrelation, self.statvarrange, domain = False)
        s.add(self.r1csrelation, self.r1csvarrange, self.gadgetrelation, domain = False)

        # Link input (private) variables
        for num_pv in range(len(self.statrelation.private_var)):
            if (self.statrelation.private_var[num_pv] == None):
                continue
            s.add(self.statrelation.private_var[num_pv] == self.r1csrelation.private_var[num_pv])

        # Link public variables
        for num_pv in range(len(self.statrelation.public_var)):
            s.add(self.statrelation.public_var[num_pv] == self.r1csrelation.public_var[num_pv])

        # link public input with public value
        for i in range(self.r1csrelation.constraintClass.public_input):
            s.add(self.r1csrelation.public_var[i] == self.r1csrelation.public_value[i])

        # link private input with private value
        for i in range(self.r1csrelation.constraintClass.private_input):
            s.add(self.r1csrelation.private_var[i] == self.r1csrelation.private_value[i])

        check = s.check()
        
        if (check == z3.unsat):
            cprint.error("Statement function and function in R1CS matrix are not valid")
            raise ValueError("Statement function and function in R1CS matrix are not valid")

        # ===== CHECK POINT 1 =====
        if (self.r1csrelation.constraintClass.public_input > 0):
        # Create solver to compare statement and r1cs equations by public variables
            cprint.info("Create a SMT Solver to compare the statement function and R1CS matrix by public variables", 1)
            
            s = z3p.Solver()

            s.add(self.statrelation, self.statvarrange, domain = False)
            s.add(self.r1csrelation, self.r1csvarrange, self.gadgetrelation, domain = False)

            # link private variables (private variables are equal)
            for num_pv in range(len(self.statrelation.private_var)):
                if (self.statrelation.private_var[num_pv] == None):
                    continue
                s.add(self.statrelation.private_var[num_pv] == self.r1csrelation.private_var[num_pv])

            # link public variables (private variables are not equal)
            for num_pv in range(len(self.statrelation.public_var)):
                s.add(self.statrelation.public_var[num_pv] != self.r1csrelation.public_var[num_pv])

            check = s.check()

            satcheck.append(check)
            #if (check != z3.unsat):
            #    return check
        
        else:
            cprint.warning("Skip the comparison with public variable since the number of public input is 0", 1)
            
            satcheck.append(None)

        # ===== CHECK POINT 2 =====
        # Create solver to compare statement and r1cs equations by boolean variables
        cprint.info("Create a SMT Solver to compare the statement function and R1CS matrix by Boolean variables", 1)
        
        s = z3p.Solver()

        bstat = z3.Bool("bstat")
        br1cs = z3.Bool("br1cs")

        estat = bstat == z3.And(self.statrelation.equations)
        er1cs = br1cs == z3.And(self.r1csrelation.equations)

        # Add statement and r1cs equation
        if (len(self.statrelation.equations) != 1 or len(opt.get_vars(self.statrelation.equations[0])) != 1):
            s.add(self.statrelation, self.statvarrange)
        s.add(self.r1csrelation, self.r1csvarrange, self.gadgetrelation)

        # Add statement and r1cs boolean output
        s.add(estat)
        s.add(er1cs)

        # Link private variables
        for num_pv in range(len(self.statrelation.private_var)):
            if (self.statrelation.private_var[num_pv] == None):
                continue
            s.add(self.statrelation.private_var[num_pv] == self.r1csrelation.private_var[num_pv])

        # Link public variables
        for num_pv in range(len(self.statrelation.public_var)):
            s.add(self.statrelation.public_var[num_pv] == self.r1csrelation.public_var[num_pv])

        # Link boolean output (not equal)
        s.add(bstat != br1cs)

        check = s.check()
        
        satcheck.append(check)
        
        return satcheck

    def domainComparison(self):
        """Compare statement equations domain and r1cs equations domain ar same
        
        SNARKSolver -> z3.z3.CheckSatResult"""
        cprint.info("Compare if Statement function and R1CS matrix have same domain")
        
        # Compare statement equations domain and r1cs equations domain
        for i in range(len(self.statrelation.private_var)):
            stat_var = self.statrelation.private_var[i]
            r1cs_var = self.r1csrelation.private_var[i]
            
            if (stat_var == None):
                continue
            if (type(stat_var) == z3.z3.BoolRef):
                cprint.info("Skip domain comparison for Boolean variable", 1)
                continue
            
            # Domain of statement private variable
            cprint.info("Get the domain of statement function for variable no. " + str(i), 1)
            optmax = opt.optmaxbound(stat_var, (self.statrelation, self.statvarrange))
            
            if (optmax):
                cprint.info("Use the optimition function to find the domainfor variable no. " + str(i), 2)
                stat_min = 0
                stat_max = MOD - 1
            else:
                o = z3p.Optimize()
                o.add(self.statrelation, self.statvarrange)
                
                stat_min, stat_max = o.minmax(stat_var)

            # Domain of r1cs private variable
            cprint.info("Get the domain of function in R1CS matrix for variable no. " + str(i), 1)
            
            optmax = opt.optmaxbound(r1cs_var, (self.r1csrelation, self.r1csvarrange, self.gadgetrelation))
            
            if (optmax):
                cprint.info("Use the optimition function to find the domainfor variable no. " + str(i), 2)
                r1cs_min = 0
                r1cs_max = MOD - 1
            else:
                o = z3p.Optimize()
                o.add(self.r1csrelation, self.r1csvarrange, self.gadgetrelation)
                
                r1cs_min, r1cs_max = o.minmax(r1cs_var)

            # compare domains
            cprint.info("Comapre if domains have same upper bound and lower bound", 2)
            
            stat_min = int(str(stat_min))
            stat_max = int(str(stat_max))
            r1cs_min = int(str(r1cs_min))
            r1cs_max = int(str(r1cs_max))

            if ((stat_min != r1cs_min) or (stat_max != r1cs_max)):
                return z3.sat

        # Find if r1cs equations have solution outside statement domain
        if (len(self.statvarrange) == 0):
            cprint.info("Skip check of outside domain since there is no integer statement variable", 2)
            return z3.unsat
        
        cprint.info("Find if R1CS matrix have solution outside statement function domain", 2)
        reserverange = opt.reverseRange(self.statvarrange)

        s = z3p.Solver()

        # add r1cs equation
        s.add(self.r1csrelation, self.r1csvarrange, self.gadgetrelation)
        
        # add statement reserve domain
        s.add(reserverange)

        # link private variables
        for num_pv in range(len(self.statrelation.private_var)):
            if (self.statrelation.private_var[num_pv] == None):
                continue
            
            s.add(self.statrelation.private_var[num_pv] == self.r1csrelation.private_var[num_pv])

        check = s.check()
        
        return check

    def domainFuzzing(self):
        """Check if the domain of r1cs equations has gap to cover the domain of statement equations
        
        snarkSolver -> z3.z3.CheckSatResult"""
        cprint.info("Use " + DOMAIN_FUZZING_TOOL + " tool to run the extra domain comparison")
        
        domains = {}

        # Calculate total doamin size
        dsize = 0

        for var in self.statvarrange:
            o = z3p.Optimize()
            o.add(self.statvarrange[var])
            rmin, rmax = o.minmax(var)
            
            domains[var] = (rmin, rmax)
            dsize += int(str(rmax)) - int(str(rmin)) + 1
            
        # Calculate the number of input
        if ("%" in DOMAIN_TEST_SIZE):
            tsize = int(dsize * float(DOMAIN_TEST_SIZE.strip("%")))
        else:
            tsize = min(int(DOMAIN_TEST_SIZE), dsize)
            
        cprint.info("Generate " + str(tsize) + " input value(s) to check the domain")

        for _ in range(tsize):
            # Generate random number for each private variable
            if (DOMAIN_FUZZING_TOOL.upper() == "DEFAULT"):
                tool_path = os.path.join(ABSPATH, "domain", "random", "sysRandom.py")
            else:
                tool_path = DOMAIN_FUZZING_TOOL
            
            stdin = [tool_path]

            size = len(self.statrelation.private_var) - self.statrelation.private_var.count(None)
            stdin.append(str(size))

            for i in range(len(self.statrelation.private_var)):
                var = self.statrelation.private_var[i]
                
                if (var == None):
                    continue
                
                stdin.append(str(domains[var][0]))
                stdin.append(str(domains[var][1]))
            
            exit = subprocess.run(stdin, stdout = subprocess.PIPE)

            stdout = exit.stdout.decode("utf-8")

            rnums = stdout.split(" ")
            print(rnums)
            rnums = list(map(int, rnums))

            # Check if r1cs equations do not have valid output in random input
            s = z3p.Solver()
            s.add(self.r1csrelation, self.r1csvarrange, self.gadgetrelation)

            # for i in range(len(self.statrelation.private_var)):
            #     var = self.statrelation.private_var[i]
                
            #     if (var == None):
            #         continue

            #     index = self.statrelation.private_var.index(var)
            #     r1csvar = self.r1csrelation.private_var[index]
                
            #     s.add(r1csvar == rnums[i])
            i = 0
            for var in self.statrelation.private_var:
                if (var == None):
                    continue
                
                index = self.statrelation.private_var.index(var)
                r1csvar = self.r1csrelation.private_var[index]
                
                s.add(r1csvar == rnums[i])
                
                i += 1

            check = s.check()
            
            if (check == z3.unsat):
                return z3.unsat

        return z3.sat