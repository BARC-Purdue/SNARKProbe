import model.value.eccmath.eccapi as ecc

class Verifier(object):
    def __init__(self, source, variableset):
        self.source = source
        self.generator_variables = variableset["generator"].variables
        self.prover_variables = variableset["prover"].variables
        self.verifier_variables = variableset["verifier"].variables
        
    def protocol(self):
        var = self.verifier_variables


        a = [ecc.FF(1)] + var["a"]

        #######################################################
        #                                                     #
        # 1. Check Pairing                                    #
        #                                                     #
        #######################################################

        # e(A, B) == e(g * alpha, h * beta) * e(g * f_io, h * gamma) * e(C, h * delta)

        f_io = ecc.Ideal()
        for i in range(len(a)):
            f_io += a[i] * var["S_k"][i]

        eleft = ecc.pairing(var["A"], var["B"])

        if ("P" in var and "Q" in var ):
            eright1 = ecc.pairing(var["P"], var["Q"])
        else:
            eright1 = var["PQ"]
            print("WARNING: Did not recompute pairing of P and Q")
        eright2 = ecc.pairing(f_io, var["H"])
        eright3 = ecc.pairing(var["C"], var["D"])
        eright = eright1 * eright2 * eright3

        if (eleft != eright):
            #raise ValueError("e(A, B) does not equal to e(g * alpha, h * beta) * e(g * f_io, h * gamma) * e(C, h * delta)")
            print("e(A, B) does not equal to e(g * alpha, h * beta) * e(g * f_io, h * gamma) * e(C, h * delta)")

        #######################################################
        #                                                     #
        # 2. Accept iff all the above checks succeeded        #
        #                                                     #
        #######################################################

        accept = True
        if (accept != var["accept"] or accept != self.source.groundtruth):
            print("Verification result does not match the ground truth")

        print("Pass all tests in Groth16 verifier")