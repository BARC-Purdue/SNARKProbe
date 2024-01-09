import z3
import os

import utils.fuzzMatrix as mt

from config import *

class CMakeLists(object):
    def __init__(self, filecpp, filebinary):
        self.filecpp = filecpp
        self.filebinary = filebinary
        
    def buildmakefile(self):
        filepath = os.path.join(COMPILE_PATH, "src", "CMakeLists.txt")
        
        f = open(filepath, "w")
        f.write("include_directories(.)\n")
        f.write("\n")
        
        for i in range(len(self.filecpp)):
            f.write("add_executable(\n")
            f.write("\t" + self.filebinary[i] + "\n")
            f.write("\n")
            f.write("\t" + self.filecpp[i] + "\n")
            f.write(")\n")
            f.write("\n")
            
            f.write("target_link_libraries(\n")
            f.write("\t" + self.filebinary[i] + "\n")
            f.write("\n")
            f.write("\tsnark\n")
            f.write(")\n")
            f.write("\n")
            
            f.write("target_include_directories(\n")
            f.write("\t" + self.filebinary[i] + "\n")
            f.write("\n")
            f.write("\tPUBLIC\n")
            f.write("\t${DEPENDS_DIR}/libsnark\n")
            f.write("\t${DEPENDS_DIR}/libsnark/depends/libfqfft\n")
            f.write(")\n")
            f.write("\n")
        
        f.close()

class ProgFeature(object):
    def __init__(self, protocol, verifier):
        """Stpre the output libsnark program features including protocol and verifier type
        
        ProgFeature, str, str -> None"""
        self.protocol = protocol
        self.verifier = verifier
        
        self.include = []
        
        self.validparameter()
        
    def __str__(self):
        """Return feature as string for file name
        
        ProgFeature -> str"""
        return self.protocol.lower() + "_" + self.verifier.lower()
        
    def validparameter(self):
        """Check if the protocol and verifier options are valid
        
        ProgFeature -> None"""
        protocol = ["PGHR13", "GROTH16"]
        verifier = ["STRONG_IC", "WEAK_IC"]
        
        if (self.protocol not in protocol):
            raise ValueError("Does not have protocol option: " + protocol)
        
        if (self.verifier not in verifier):
            raise ValueError("Does not have verifier option: " + verifier)

class ProGenerator(object):
    def __init__(self, src, feature: ProgFeature, primary_input_size = 0):
        """Generate libsnark program from R1CS matrix from r1cs martix
        
        ProGenerator, str, ProgFeature[, int] -> None"""
        self.src = src
        
        self.num_variables = []
        self.num_constraint = []
        self.witness = []
        self.witnessvalue = {}
        self.r1csmatrix = []
        
        self.primary_input_size = primary_input_size
        self.feature = feature
        
        self.variables = []
        self.constraints = []
        
    def readMatrixFromFile(self):
        """Rad the matrix information from provided file
        
        ProGenerator -> None"""
        matrix = mt.Matrix(self.src)
        self.num_variables = matrix.num_variables
        self.num_constraint = matrix.num_constraint
        self.witness = matrix.witness
        self.r1csmatrix = matrix.r1csmatrix

    def readMatrixFromClass(self, matrixClass : mt.Matrix):
        """Rad the matrix information from RandomMatrix class
        
        ProGenerator, RandomMatrix -> None"""
        self.num_variables = matrixClass.num_variables
        self.num_constraint = matrixClass.num_constraint
        self.witness = matrixClass.witness
        self.r1csmatrix = matrixClass.r1csmatrix

    def setvariables(self):
        """Create variables in the R1CS matrix
        
        RandomMatrix -> None"""
        self.variables.append(z3.IntVal(1))
        
        for i in range(1, self.num_variables):
            self.variables.append(z3.Int("sym_" + str(i - 1)))
        
        for i in range(1, self.num_variables):
            var = self.variables[i]
            val = self.witness[i]
            self.witnessvalue[var] = val
    
    def getRelation(self):
        """Convert the R1CS matrix to math equations set
        
        RandomMatrix -> None"""
        for cons in range(0, self.num_constraint):
            gate = self.createEquation(self.r1csmatrix[0][cons], self.r1csmatrix[1][cons], self.r1csmatrix[2][cons])
            self.constraints.append(gate)
            
    def createEquation(self, A, B, C):
        """Convert the R1CS matrix to math equations set for one constraint
        
        RandomMatrix -> tuple of instance(z3py)"""
        clauseA = z3.IntVal("0")
        for i in range(self.num_variables):
            if (A[i] != 0):
                clauseA = clauseA + A[i] * self.variables[i]

        clauseB = z3.IntVal("0")
        for i in range(self.num_variables):
            if (B[i] != 0):
                clauseB = clauseB + B[i] * self.variables[i]
        
        clauseC = z3.IntVal("0")
        for i in range(self.num_variables):
            if (C[i] != 0):
                clauseC = clauseC + C[i] * self.variables[i]
        
        return z3.simplify(clauseA), z3.simplify(clauseB), z3.simplify(clauseC)
    
    def generateProg(self, dst):
        """Generate libsnark program file
        
        RandomMatrix, str -> None"""
        if (self.feature.protocol == "PGHR13"):
            self.generateProgPGHR13(dst)
        elif (self.feature.protocol == "GROTH16"):
            self.generateProgGROTH16(dst)

    def generateProgPGHR13(self, dst):
        """Generate libsnark program file with PGHR13 protocol
        
        RandomMatrix, str -> None"""
        f = open(dst, "w")

        f.write('#include <stdlib.h>\n')
        f.write('#include <iostream>\n\n')

        f.write('#include "libff/algebra/fields/field_utils.hpp"\n')
        f.write('#include "libsnark/zk_proof_systems/ppzksnark/r1cs_ppzksnark/r1cs_ppzksnark.hpp"\n')
        f.write('#include "libsnark/common/default_types/r1cs_ppzksnark_pp.hpp"\n')
        f.write('#include "libsnark/gadgetlib1/pb_variable.hpp"\n\n')

        f.write("using namespace libsnark;\n")
        f.write("using namespace std;\n\n")

        f.write("int main()\n")
        f.write("{\n")
        f.write("\ttypedef libff::Fr<default_r1cs_ppzksnark_pp> FieldT;\n\n")

        f.write("\tdefault_r1cs_ppzksnark_pp::init_public_params();\n\n")

        f.write("\tprotoboard<FieldT> pb;\n\n")

        for var in self.variables[1:]:
            info = "\tpb_variable<FieldT> {};\n".format(var)
            f.write(info)
        f.write("\n")

        for var in self.variables[1:]:
            info = '\t{}.allocate(pb, "{}");\n'.format(var, var)
            f.write(info)
        f.write("\n")

        if (self.primary_input_size > 0):
            info = '\tpb.set_input_sizes({});\n'.format(self.primary_input_size)
            f.write(info)
        
        for constraint in self.constraints:
            A, B, C = constraint
            A = str(z3.simplify(A)).replace("\n", " ")
            B = str(z3.simplify(B)).replace("\n", " ")
            C = str(z3.simplify(C)).replace("\n", " ")
            info = "\tpb.add_r1cs_constraint(r1cs_constraint<FieldT>({}, {}, {}));\n".format(A, B, C)
            f.write(info)
        f.write("\n")

        for var in self.witnessvalue.keys():
            info = "\tpb.val({}) = {};\n".format(var, self.witnessvalue[var])
            f.write(info)
        f.write("\n")

        f.write("\tconst r1cs_constraint_system<FieldT> constraint_system = pb.get_constraint_system();\n\n")

        f.write("\tconst r1cs_ppzksnark_keypair<default_r1cs_ppzksnark_pp> keypair = r1cs_ppzksnark_generator<default_r1cs_ppzksnark_pp>(constraint_system);\n\n")

        f.write("\tconst r1cs_ppzksnark_proof<default_r1cs_ppzksnark_pp> proof = r1cs_ppzksnark_prover<default_r1cs_ppzksnark_pp>(keypair.pk, pb.primary_input(), pb.auxiliary_input());\n\n")

        if (self.feature.verifier == "WEAK_IC"):
            f.write("\tbool verified = r1cs_ppzksnark_verifier_weak_IC<default_r1cs_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")
        elif (self.feature.verifier == "STRONG_IC"):
            f.write("\tbool verified = r1cs_ppzksnark_verifier_strong_IC<default_r1cs_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")

        f.write('\tcout << "Number of R1CS constraints: " << constraint_system.num_constraints() << endl;\n')
        f.write('\tcout << "Primary (public) input: " << pb.primary_input() << endl;\n')
        f.write('\tcout << "Auxiliary (private) input: " << pb.auxiliary_input() << endl;\n')
        f.write('\tcout << "Verification status: " << verified << endl;\n\n')

        f.write("\tconst r1cs_ppzksnark_verification_key<default_r1cs_ppzksnark_pp> vk = keypair.vk;\n\n")

        f.write("\treturn 0;\n")
        f.write("}")

        f.close()
        
    def generateProgGROTH16(self, dst):
        """Generate libsnark program file with PGHR13 protocol
        
        RandomMatrix, str -> None"""
        f = open(dst, "w")

        f.write('#include <stdlib.h>\n')
        f.write('#include <iostream>\n\n')

        f.write('#include "libff/algebra/fields/field_utils.hpp"\n')
        f.write('#include "libsnark/zk_proof_systems/ppzksnark/r1cs_gg_ppzksnark/r1cs_gg_ppzksnark.hpp"\n')
        f.write('#include "libsnark/common/default_types/r1cs_gg_ppzksnark_pp.hpp"\n')
        f.write('#include "libsnark/gadgetlib1/pb_variable.hpp"\n\n')

        f.write("using namespace libsnark;\n")
        f.write("using namespace std;\n\n")

        f.write("int main()\n")
        f.write("{\n")
        f.write("\ttypedef libff::Fr<default_r1cs_gg_ppzksnark_pp> FieldT;\n\n")

        f.write("\tdefault_r1cs_gg_ppzksnark_pp::init_public_params();\n\n")

        f.write("\tprotoboard<FieldT> pb;\n\n")

        for var in self.variables[1:]:
            info = "\tpb_variable<FieldT> {};\n".format(var)
            f.write(info)
        f.write("\n")

        for var in self.variables[1:]:
            info = '\t{}.allocate(pb, "{}");\n'.format(var, var)
            f.write(info)
        f.write("\n")

        if (self.primary_input_size > 0):
            info = '\tpb.set_input_sizes({});\n'.format(self.primary_input_size)
            f.write(info)
        
        for constraint in self.constraints:
            A, B, C = constraint
            A = str(z3.simplify(A)).replace("\n", " ")
            B = str(z3.simplify(B)).replace("\n", " ")
            C = str(z3.simplify(C)).replace("\n", " ")
            info = "\tpb.add_r1cs_constraint(r1cs_constraint<FieldT>({}, {}, {}));\n".format(A, B, C)
            f.write(info)
        f.write("\n")

        for var in self.witnessvalue.keys():
            info = "\tpb.val({}) = {};\n".format(var, self.witnessvalue[var])
            f.write(info)
        f.write("\n")

        f.write("\tconst r1cs_constraint_system<FieldT> constraint_system = pb.get_constraint_system();\n\n")

        f.write("\tconst r1cs_gg_ppzksnark_keypair<default_r1cs_gg_ppzksnark_pp> keypair = r1cs_gg_ppzksnark_generator<default_r1cs_gg_ppzksnark_pp>(constraint_system);\n\n")

        f.write("\tconst r1cs_gg_ppzksnark_proof<default_r1cs_gg_ppzksnark_pp> proof = r1cs_gg_ppzksnark_prover<default_r1cs_gg_ppzksnark_pp>(keypair.pk, pb.primary_input(), pb.auxiliary_input());\n\n")

        if (self.feature.verifier == "WEAK_IC"):
            f.write("\tbool verified = r1cs_gg_ppzksnark_verifier_weak_IC<default_r1cs_gg_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")
        elif (self.feature.verifier == "STRONG_IC"):
            f.write("\tbool verified = r1cs_gg_ppzksnark_verifier_strong_IC<default_r1cs_gg_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")

        f.write('\tcout << "Number of R1CS constraints: " << constraint_system.num_constraints() << endl;\n')
        f.write('\tcout << "Primary (public) input: " << pb.primary_input() << endl;\n')
        f.write('\tcout << "Auxiliary (private) input: " << pb.auxiliary_input() << endl;\n')
        f.write('\tcout << "Verification status: " << verified << endl;\n\n')

        f.write("\tconst r1cs_gg_ppzksnark_verification_key<default_r1cs_gg_ppzksnark_pp> vk = keypair.vk;\n\n")

        f.write("\treturn 0;\n")
        f.write("}")

        f.close()
