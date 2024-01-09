import z3

import solver.statRelation as sr
import solver.r1csRelation as rr
import solver.gadgetRelation as gr

from config import *

class Solver():
    def __init__(self):
        """An enhanced z3py SMT solver design for equations comparison
        
        Solver -> None"""
        if (QF_BV):
            self.s = z3.SolverFor("QF_BV")
            z3.set_option("parallel.enable", True)
        else:
            self.s = z3.Solver()

    def __str__(self):
        """Return the same string format as z3py
        
        Solver -> str"""
        return str(self.s)

    def __repr__(self):
        """Return the same string format as z3py
        
        Solver -> str"""
        return str(self)

    def add(self, *args, domain = True):
        """Add constraints as the same as z3py add method
        
        Solver, list -> None"""
        def addState(statrelation: sr.StatRelation, statvarrange):
            for equation in statrelation.equations:
                self.s.add(equation)

            if (domain):
                for var in statvarrange:
                    self.s.add(statvarrange[var])

        def addR1CS(r1csrelation: rr.R1CSRelation, r1csvarrange, gadgetrelation: gr.GadgetRelation):
            for equation in r1csrelation.equations:
                self.s.add(equation)

            if (domain):
                for var in r1csvarrange:
                    self.s.add(r1csvarrange[var])

            for equation in gadgetrelation.equations:
                self.s.add(equation)

        if (isinstance(args[0], sr.StatRelation)):
            statrelation, statvarrange = args
            addState(statrelation, statvarrange)

        elif (isinstance(args[0], rr.R1CSRelation)):
            r1csrelation, r1csvarrange, gadgetrelation = args
            addR1CS(r1csrelation, r1csvarrange, gadgetrelation)

        else:
            if (len(args) == 1):
                if (isinstance(args[0], z3.z3.BoolRef)):
                    self.s.add(args[0])
                else:
                    for arg in args[0]:
                        self.s.add(arg)
            else:
                for arg in args:
                    self.s.add(arg)

    def check(self):
        """Check method same as z3py check method
        
        Solver -> None"""
        return self.s.check()

    def reset(self):
        """Reset method same as z3py reset method
        
        Solver -> None"""
        self.s.reset()

    def deepreset(self):
        """Deep reset by creating a new z3 solver
        
        Solver -> None"""
        if (QF_BV):
            self.s = z3.SolverFor("QF_BV")
            z3.set_option("parallel.enable", True)
        else:
            self.s = z3.Solver()

class Optimize(object):
    def __init__(self):
        """An enhanced z3py SMT optimizer to get the minimum and maximum values
        
        Optimize -> None"""
        self.o = z3.Optimize()
    
    def __str__(self):
        """Return the same string format as z3py
        
        Optimize -> str"""
        return str(self.o)

    def __repr__(self):
        """Return the same string format as z3py
        
        Optimize -> str"""
        return str(self)

    def add(self, *args):
        """Add constraints as the same as z3py add method
        
        Optimize, list -> None"""
        def addState(statrelation: sr.StatRelation, statvarrange):
            for equation in statrelation.equations:
                self.o.add(equation)

            for var in statvarrange:
                self.o.add(statvarrange[var])

        def addR1CS(r1csrelation: rr.R1CSRelation, r1csvarrange, gadgetrelation: gr.GadgetRelation):
            for equation in r1csrelation.equations:
                self.o.add(equation)

            for var in r1csvarrange:
                self.o.add(r1csvarrange[var])

            for equation in gadgetrelation.equations:
                self.o.add(equation)

        if (isinstance(args[0], sr.StatRelation)):
            statrelation, statvarrange = args
            addState(statrelation, statvarrange)

        elif (isinstance(args[0], rr.R1CSRelation)):
            r1csrelation, r1csvarrange, gadgetrelation = args
            addR1CS(r1csrelation, r1csvarrange, gadgetrelation)

        else:
            if (len(args) == 1):
                if (isinstance(args[0], z3.z3.BoolRef)):
                    self.o.add(args[0])
                else:
                    for arg in args[0]:
                        self.o.add(arg)
            else:
                for arg in args:
                    self.o.add(arg)

    def reset(self):
        """Reset method same as z3py reset method
        
        Optimize -> None"""
        self.o.reset()

    def deepreset(self):
        """Deep reset by creating a new z3 solver
        
        Optimize -> None"""
        self.o = z3.Optimize()

    def minmax(self, var):
        self.o.push()
        self.o.minimize(var)
        self.o.check()
        minval = self.o.model()[var]

        self.o.pop()
        self.o.maximize(var)
        self.o.check()
        maxval = self.o.model()[var]

        return minval, maxval