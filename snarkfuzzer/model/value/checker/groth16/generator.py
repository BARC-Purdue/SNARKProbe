import model.value.eccmath.eccapi as ecc

from config import *

class Generator(object):
    def __init__(self, source, variableset):
        self.source = source
        self.generator_variables = variableset["generator"].variables
        self.prover_variables = variableset["prover"].variables
        self.verifier_variables = variableset["verifier"].variables
        
    def protocol(self):
        var = self.generator_variables
        

        #######################################################
        #                                                     #
        # ?. Key Generation Setup                             #
        #                                                     #
        #######################################################


        #######################################################
        #                                                     #
        # ?. Proving Key Recalculation                        #
        #                                                     #
        #######################################################

        # G1 elements

        # g_alpha = g * alpha
        g_alpha = var["g"] * var["alpha"]
        if (g_alpha != var["g_alpha"]):
            raise ValueError("alpha_g1 does not equal to g * alpha")

        # g_beta = g * beta
        g_beta = var["g"] * var["beta"]
        if (g_beta != var["g_beta"]):
            raise ValueError("g_beta does not equal to g * beta")

        # g_delta = g * delta
        g_delta = var["g"] * var["delta"]
        if (g_delta != var["g_delta"]):
            raise ValueError("g_delta does not equal to g * delta")

        # G2 elements

        # h_beta = h * beta
        h_beta = var["h"] * var["beta"]
        if (h_beta != var["h_beta"]):
            raise ValueError("h_beta does not equal to h * beta")

        # h_gamma = h * gamma
        h_gamma = var["h"] * var["gamma"]
        if (h_gamma != var["h_gamma"]):
            raise ValueError("h_gamma does not equal to h * gamma")

        # h_delta = h * delta
        h_delta = var["h"] * var["delta"]
        if (h_delta != var["h_delta"]):
            raise ValueError("h_delta does not equal to h * delta")

        # {h * s^i}_{i=0}^{d-1}
        # gsi = []
        # for i in range(0, var["d"] - 1 + 1):
        #     gsi.append(var["g"] * (var["s"] ** i))
        
        #print(gsi)

        # g * ((beta * v_k(s) + alpha * w_k(s) + y_k(s)) / delta)
        end = len(var["A"])
        delta_inverse = var["delta"].inverse()

        f_mid = []
        for k in range(var["l"] + 1, end):
            g = var["g"] * ((var["beta"] * var["A"][k] + var["alpha"] * var["B"][k] + var["C"][k]) * delta_inverse)
            f_mid.append(g)

        if (f_mid != var["f_mid"]):
            raise ValueError("f_mid does not equal to g * ((beta * v_k(s) + alpha * w_k(s) + y_k(s)) / delta)")

        #######################################################
        #                                                     #
        # ?. Verification Key Recalculation                   #
        #                                                     #
        #######################################################

        # G1 elements


        # alpha_g1 beta_g2 pairing
        # alpha_g1_beta_g2 = ecc.pairing(var["g"] * var["alpha"], var["h"] * var["beta"])
        # # if (alpha_g1_beta_g2 != var["beta_g2"]):
        # #     raise ValueError("alpha_g1_beta_g2 pairing does no equal to alpha_g1_beta_g2")
        # print(alpha_g1_beta_g2)
        
        # S_k = g * ((beta * v_k(s) + alpha * w_k(s) + y_k(s)) / gamma)
        gamma_inverse = var["gamma"].inverse()

        S_k = []
        for k in range(0, var["l"] + 1):
            g = var["g"] * ((var["beta"] * var["A"][k] + var["alpha"] * var["B"][k] + var["C"][k]) * gamma_inverse)
            S_k.append(g)

        if (S_k != var["S_k"]):
            raise ValueError("S_k does not equal to g * ((beta * v_k(s) + alpha * w_k(s) + y_k(s)) / gamma)")

        print("Pass all tests in Groth16 generator")