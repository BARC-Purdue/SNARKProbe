import model.value.eccmath.eccapi as ecc

class Prover(object):
    def __init__(self, source, variableset):
        self.source = source
        self.generator_variables = variableset["generator"].variables
        self.prover_variables = variableset["prover"].variables
        self.verifier_variables = variableset["verifier"].variables
        
    def protocol(self):
        var = self.prover_variables
        
        w = [1] + var["w1"] + var["w2"]

        # A = g * (alpha + v(s) + r * delta)
        A = ecc.Ideal()

        A += var["g_alpha"]

        for i in range(len(w)):
            A += (var["v_k"][i] * w[i])

        A += (var["r"] * var["g_delta"])

        if (A != var["A"]):
            raise ValueError("A does not equal to g * (alpha + v(s) + r * delta)")

        # Bg = g * (beta + w(s) + r * delta)
        Bg = ecc.Ideal()
        Bg += var["g_beta"]

        for i in range(len(w)):
            Bg += (var["w_kP"][i] * w[i])

        Bg += (var["u"] * var["g_delta"])

        # Bh = h * (beta + w(s) + r * delta)
        Bh = ecc.Ideal()

        Bh += var["h_beta"]

        for i in range(len(w)):
            Bh += (var["w_k"][i] * w[i])

        Bh += (var["u"] * var["h_delta"])

        if (Bh != var["B"]):
            raise ValueError("Bh does not equal to h * (beta + w(s) + r * delta)")

        # C = g * (f_mid + t(s)h(s)/delta + u*a + r*b -u*r*delta)
        C = ecc.Ideal()

        # thd = t(s) * h(s) / delta
        if ("thd" not in var):
            thd = ecc.Ideal()
            for i in range(0, len(var["hh"])):
                g = var["hc"][i] * var["hh"][i]
                thd = thd + g
        else:
            thd = var["thd"]
            print("WARNING: Did not recompute thd")

        C = var["f_mid"] + thd + var["u"] * A + var["r"] * Bg + (-(var["u"] * var["r"] * var["g_delta"]))

        if (C != var["C"]):
            raise ValueError("C does not equal to g * (f_mid + t(s)h(s)/delta + u*a + r*b -u*r*delta)")

        print("Pass all tests in Groth16 prover")