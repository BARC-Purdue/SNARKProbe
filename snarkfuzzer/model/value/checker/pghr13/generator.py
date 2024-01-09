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
        # 1. Post-Processing QAP to QAP with evalution        #
        #                                                     #
        #######################################################


        #######################################################
        #                                                     #
        # 2. Handle the vectors A, B, and C extension with Z  #
        #                                                     #
        #######################################################
        zero = ecc.FF(0)

        if (len(var["A"]) != 1 + var["m"] + 3):
            if (len(var["A"]) == 1 + var["m"]):
                # Pure QAP without extension
                pass
            elif (len(var["A"]) == 1 + var["m"] + 1):
                # QAP with extension Z (did not follow the protocol index)
                var["A"].pop()
                var["A0"].pop()
                var["B"].pop()
                var["C"].pop()
                print("WARNING: Vectors A, B, and/or C are not extended Z with correct index")
            else:
                raise Exception
        
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
        #                                                     #
        # 3. Key Generation Setup                             #
        #                                                     #
        #######################################################

        # Extend vector A with Z
        var["A"].extend([var["Z"], zero, zero])
        var["A0"].extend([var["Z"], zero, zero])

        # Extend vector B with Z
        var["B"].extend([zero, var["Z"], zero])

        # Extend vector C with Z
        var["C"].extend([zero, zero, var["Z"]])

        #######################################################
        #                                                     #
        # 3. Proving Key Recalculation                        #
        #                                                     #
        #######################################################

        # pk_A = {A_i(tau) * rhoA * P1}_{i = 0}^{m + 3}
        pk_A = []
        for i in range(0, 1 + var["m"] + 3):
            g = var["A"][i] * var["rhoA"] * var["P1"]
            pk_A.append(g)
        
        if (pk_A != var["pk_A"]):
            raise ValueError("pk_A does not equal to {A_i(tau) * rhoA * P1}_{i = 0}^{m + 3}")

        # pk'_A = {A_i(tau) * alphaA * rhoA * P1}_{i = n}^{m + 3}
        # Check if protocol fix the problem found by Gabizon [Gab19] and reported as CVE-201907167 in Zcash
        pk_Ap = []
        for i in range(var["n"], 1 + var["m"] + 3):
            g = var["A"][i] * var["alphaA"] * var["rhoA"] * var["P1"]
            pk_Ap.append(g)
        
        if (pk_Ap != var["pk_Ap"]):
            print("WARNING: pk'_A may not follow the problem reported as CVE-201907167")

            pk_Ap = []
            for i in range(0, 1 + var["m"] + 3):
                g = var["A"][i] * var["alphaA"] * var["rhoA"] * var["P1"]
                pk_Ap.append(g)
                
            if (pk_Ap != var["pk_Ap"]):
                raise ValueError("pk'_A does not equal to {A_i(tau) * alphaA * rhoA * P1}_{i = n}^{m + 3}")
        
        # pk_B = {B_i(tau) * rhoB * P2}_{i = 0}^{m + 3}
        pk_B = []
        for i in range(0, 1 + var["m"] + 3):
            g = var["B"][i] * var["rhoB"] * var["P2"]
            pk_B.append(g)
        
        if (pk_B != var["pk_B"]):
            raise ValueError("pk_B does not equal to {B_i(tau) * rhoB * P2}_{i = 0}^{m + 3}")

        # pk'_B = {B_i(tau) * alphaB * rhoB * P1}_{i = 0}^{m + 3}
        pk_Bp = []
        for i in range(0, 1 + var["m"] + 3):
            g = var["B"][i] * var["alphaB"] * var["rhoB"] * var["P1"]
            pk_Bp.append(g)
        
        if (pk_Bp != var["pk_Bp"]):
            raise ValueError("pk'_B does not equal to {B_i(tau) * alphaB * rhoB * P1}_{i = 0}^{m + 3}")

        # pk_C = {C_i(tau) * rhoA * rhoB * P1}_{i = 0}^{m + 3}
        pk_C = []
        for i in range(0, 1 + var["m"] + 3):
            g = var["C"][i] * var["rhoA"] * var["rhoB"] * var["P1"]
            pk_C.append(g)

        if (pk_C != var["pk_C"]):
            raise ValueError("pk_C does not equal to {C_i(tau) * rhoA * rhoB * P1}_{i = 0}^{m + 3}")

        # pk'_C = {C_i(tau) * alphaC * rhoA * rhoB * P1}_{i = 0}^{m + 3}
        pk_Cp = []
        for i in range(0, 1 + var["m"] + 3):
            g = var["C"][i] * var["alphaC"] * var["rhoA"] * var["rhoB"] * var["P1"]
            pk_Cp.append(g)
        
        if (pk_Cp != var["pk_Cp"]):
            raise ValueError("pk'_C does not equal to {C_i(tau) * alphaC * rhoA * rhoB * P1}_{i = 0}^{m + 3}")

        # pk_K = {beta * (A_i(tau) * rhoA + B_i(tau) * rhoB + A_i(tau) * rhoA * rhoB) * P1}_{i = 0}_{m + 3}
        pk_K = []
        
        for i in range(0, 1 + var["m"] + 3):
            g = var["beta"] * (var["A0"][i] * var["rhoA"] + var["B"][i] * var["rhoB"] + var["C"][i] * var["rhoA"] * var["rhoB"]) * var["P1"]
            pk_K.append(g)

        if (pk_K != var["pk_K"]):
            raise ValueError("pk_K does not equal to {beta * (A_i(tau) * rhoA + B_i(tau) * rhoB + A_i(tau) * rhoA * rhoB) * P1}_{i = 0}_{m + 3}")
        
        # pk_H = {tau ^ i * P1}_{i=0}^{d}
        pk_H = []
        for i in range(0, var["d"] + 1):
            pk_H.append(var["P1"] * (var["tau"] ** i))
            
        if (pk_H != var["pk_H"]):
            raise ValueError("pk_H does not equal to {tau ^ i * P1}_{i=0}^{d}")
        
        #######################################################
        #                                                     #
        # 4. Verification Key Recalculation                   #
        #                                                     #
        #######################################################
        
        # vk_A = alphaA * P2
        vk_A = var["alphaA"] * var["P2"]
        if (vk_A != var["vk_A"]):
            raise ValueError("vk_A does not equal to alphaA * P2")
        
        # vk_B = alphaB * P1
        vk_B = var["alphaB"] * var["P1"]
        if (vk_B != var["vk_B"]):
            raise ValueError("vk_B does not equal to alphaB * P1")
        
        # vk_C = alphaC * P2
        vk_C = var["alphaC"] * var["P2"]
        if (vk_C != var["vk_C"]):
            raise ValueError("vk_C does not equal to alphaC * P2")
        
        # vk_gamma = gamma * P2
        vk_gamma = var["gamma"] * var["P2"]
        if (vk_gamma != var["vk_gamma"]):
            raise ValueError("vk_gamma does not equal to gamma * P2")
        
        # vk_beta_gamma_1 = gamma * beta * P1
        vk_beta_gamma_1 = (var["gamma"] * var["beta"]) * var["P1"]
        if (vk_beta_gamma_1 != var["vk_beta_gamma_1"]):
            raise ValueError("vk_beta_gamma_1 does not equal to gamma * beta * P1")
        
        # vk_beta_gamma_2 = gamma * beta * P2
        vk_beta_gamma_2 = (var["gamma"] * var["beta"]) * var["P2"]
        if (vk_beta_gamma_2 != var["vk_beta_gamma_2"]):
            raise ValueError("vk_beta_gamma_2 does not equal to gamma * beta * P2")

        # vk_Z = Z(tau) * rhoA * rhoB * P2
        vk_Z = (var["Z"] * var["rhoA"] * var["rhoB"]) * var["P2"]
        if (vk_Z != var["vk_Z"]):
            raise ValueError("vk_Z does not equal to Z(tau) * rhoA * rhoB *P2")

        # vk_IC = A(tau) * rhoA * P1
        curvelist = []
        for i in range(0, var["n"] + 1): # sum of i = 0 to n
            Ai = var["A0"][i]
            curve = (Ai * var["rhoA"]) * var["P1"]
            curvelist.append(curve)
        
        if (curvelist != var["vk_IC"]):
            raise ValueError("vk_IC does not equal to A(tau) * rhoA * P1")
        
        print("Pass all tests in PGHR13 generator")