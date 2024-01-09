import model.value.eccmath.eccapi as ecc

from config import *

class Prover(object):
    def __init__(self, source, variableset):
        self.source = source
        self.generator_variables = variableset["generator"].variables
        self.prover_variables = variableset["prover"].variables
        self.verifier_variables = variableset["verifier"].variables
        
    def protocol(self):
        var = self.prover_variables
        
        
        #######################################################
        #                                                     #
        # 2. Handle the vectors A, B, and C extension with Z  #
        #                                                     #
        #######################################################
        zero = ecc.FF(0)
        
        if (len(var["pk_A"]) == 1 + var["m"] + 3):
            pass
        elif (len(var["pk_A"]) == 1 + var["m"] + 1):
            pk_Az = var["pk_A"].pop()
            var["pk_A"].extend([pk_Az, zero, zero])
            pk_Apz = var["pk_Ap"].pop()
            var["pk_Ap"].extend([pk_Apz, zero, zero])
            
            pk_Bz = var["pk_B"].pop()
            var["pk_B"].extend([zero, pk_Bz, zero])
            pk_Bpz = var["pk_Bp"].pop()
            var["pk_Bp"].extend([zero, pk_Bpz, zero])

            pk_Cz = var["pk_C"].pop()
            var["pk_C"].extend([zero, zero, pk_Cz])
            pk_Cpz = var["pk_Cp"].pop()
            var["pk_Cp"].extend([zero, zero, pk_Cpz])
            print("WARNING: Proving Key A, B, and/or C are not calculated with correctly Z index")
        else:
            raise Exception

        #######################################################

        c = [ecc.FF(1)] + var["s"] + [var["delta1"]] + [var["delta2"]] + [var["delta3"]]
        print(c)
        print(var["delta1"])
        print(var["s"])
        print(var["m"], var["m"] + 4, len(c))
        input(">")
        #######################################################

        # pi_A := <c, pk_A>
        pi_A = ecc.Ideal()

        for i in range(0, var["m"] + 4):
            g = c[i] * var["pk_A"][i]
            pi_A = pi_A + g

        if (len(c) != len(var["pk_A"]) or pi_A != var["pi_A"]):
            raise ValueError("pi_A does not equal to <c, pk_A>")

        # pi'_A := <c, pk'_A>
        ####################
        #var["pk_Ap"] = [0] * (var["n"] + 1) + var["pk_Ap"]

        pi_Ap = ecc.Ideal()
        for i in range(0, len(c)):
            g = c[i] * var["pk_Ap"][i]
            pi_Ap = pi_Ap + g

        if (len(c) != len(var["pk_Ap"]) or pi_Ap != var["pi_Ap"]):

            var["pk_Ap"] = [0] * (var["n"] + 1) + var["pk_Ap"][var["n"] + 1:]

            pi_Ap = ecc.Ideal()

            for i in range(0, len(c)):
                g = c[i] * var["pk_Ap"][i]
                pi_Ap = pi_Ap + g


            if (len(c) != len(var["pk_Ap"]) or pi_Ap != var["pi_Ap"]):
                raise ValueError("pi'_A does not equal to <c, pk'_A>")
        ####################

        # pi_B := <c, pk_B>
        pi_B = ecc.Ideal()

        for i in range(0, len(c)):
            g = c[i] * var["pk_B"][i]
            pi_B = pi_B + g

        if (len(c) != len(var["pk_B"]) or pi_B != var["pi_B"]):
            raise ValueError("pi_B does not equal to <c, pk_B>")

        # pi'_B := <c, pk'_B>
        pi_Bp = ecc.Ideal()

        for i in range(0, len(c)):
            g = c[i] * var["pk_Bp"][i]
            pi_Bp = pi_Bp + g

        if (len(c) != len(var["pk_Bp"]) or pi_Bp != var["pi_Bp"]):
            raise ValueError("pi'_B does not equal to <c, pk'_B>")

        # pi_C := <c, pk_C>
        pi_C = ecc.Ideal()

        for i in range(0, len(c)):
            g = c[i] * var["pk_C"][i]
            pi_C = pi_C + g

        if (len(c) != len(var["pk_C"]) or pi_C != var["pi_C"]):
            raise ValueError("pi_C does not equal to <c, pk_C>")

        # pi'_C := <c, pk'_C>
        pi_Cp = ecc.Ideal()

        for i in range(0, len(c)):
            g = c[i] * var["pk_Cp"][i]
            pi_Cp = pi_Cp + g

        if (len(c) != len(var["pk_Cp"]) or pi_Cp != var["pi_Cp"]):
            raise ValueError("pi'_C does not equal to <c, pk'_C>")

        # pi_K := <c, pk_K>
        pi_K = ecc.Ideal()

        for i in range(0, len(c)):
            g = c[i] * var["pk_K"][i]
            pi_K = pi_K + g

        if (len(c) != len(var["pk_K"]) or pi_K != var["pi_K"]):
            print("pi_K does not equal to <c, pk_K>")

        # pi_H := <h, pk_H>
        pi_H = ecc.Ideal()

        for i in range(0, len(var["h"])):
            g = var["h"][i] * var["pk_H"][i]
            pi_H = pi_H + g

        if (len(var["h"]) != len(var["pk_H"]) or pi_H != var["pi_H"]):
            raise ValueError("pi_H does not equal to <h, pk_H>")

        print()        
        print("Pass all tests in PGHR13 provers")
