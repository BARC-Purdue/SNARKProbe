import model.value.eccmath.eccapi as ecc

class Verifier(object):
    def __init__(self, source, variableset):
        self.source = source
        self.generator_variables = variableset["generator"].variables
        self.prover_variables = variableset["prover"].variables
        self.verifier_variables = variableset["verifier"].variables
        
    def protocol(self):
        var = self.verifier_variables

        #######################################################
        #                                                     #
        # 1. Compute vk_X                                     #
        #                                                     #
        #######################################################

        # vk_x = vk_IC,0 + sum{x_i * vk_IC, i}_{i = 1}^{n}
        n = len(var["x"])

        vk_x = var["vk_IC"][0]
        for i in range(1, n + 1):
            vk_x = vk_x + var["vk_IC"][i] * var["x"][i - 1]

        accept = True

        #######################################################
        #                                                     #
        # 2. Check validity of knowledge commitments          #
        #                                                     #
        #######################################################

        e11 = ecc.pairing(var["pi_A"], var["vk_A"])
        e12 = ecc.pairing(var["pi_Ap"], var["P2"])

        e21 = ecc.pairing(var["vk_B"], var["pi_B"])
        e22 = ecc.pairing(var["pi_Bp"], var["P2"])

        e31 = ecc.pairing(var["pi_C"], var["vk_C"])
        e32 = ecc.pairing(var["pi_Cp"], var["P2"])

        if ((e11 != e12) or (e21 != e22) or (e21 != e22)):
            #raise ValueError("Fail in checking validity of knowledge commitments for A, B, C")
            print("Fail in checking validity of knowledge commitments for A, B, C")
            accept = False

        #######################################################
        #                                                     #
        # 3. Check same coefficients were used                #
        #                                                     #
        #######################################################

        e41 = ecc.pairing(var["pi_K"], var["vk_gamma"])
        e42 = ecc.pairing(vk_x + var["pi_A"] + var["pi_C"], var["vk_beta_gamma_2"]) * ecc.pairing(var["vk_beta_gamma_1"], var["pi_B"])

        if (e41 != e42):
            #raise ValueError("Fail in checking same coefficients were used")
            print("Fail in checking same coefficients were used")
            accept = False

        #######################################################
        #                                                     #
        # 4. Check QAP divisibility                           #
        #                                                     #
        #######################################################

        e51 = ecc.pairing(vk_x + var["pi_A"], var["pi_B"])
        e52 = ecc.pairing(var["pi_H"], var["vk_Z"]) * ecc.pairing(var["pi_C"], var["P2"])

        if (e51 != e52):
            #raise ValueError("Fail in checking QAP divisibility")
            print("Fail in checking QAP divisibility")
            accept = False

        #######################################################
        #                                                     #
        # 5. Accept iff all the above checks succeeded        #
        #                                                     #
        #######################################################

        if (accept != var["accept"] or accept != self.source.groundtruth):
            raise ValueError("Verification result does not match the ground truth")

        print("Pass all tests in PGHR13 verifier")