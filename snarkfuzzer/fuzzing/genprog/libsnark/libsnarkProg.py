import z3
import os
import subprocess
import shutil

import fuzzing.utils.utils as ut

from config import *

class CMakeLists(object):
    def __init__(self, filename):
        """Create CMakeLists file
        
        CMakeLists, str/list -> None"""
        self.filename = filename
        
    def buildmakefile(self):
        """Save CMakeLists file to dependent library
        
        CMakeLists -> None"""  
        filepath = os.path.join(COMPILE_PATH, "src", "CMakeLists.txt")
        
        f = open(filepath, "w")
        f.write("include_directories(.)\n")
        f.write("\n")
        
        for i in range(len(self.filename)):
            progfile = self.filename[i].name + self.filename[i].ext
            binaryfile = self.filename[i].name
        
            f.write("add_executable(\n")
            f.write("\t" + binaryfile + "\n")
            f.write("\n")
            f.write("\t" + progfile + "\n")
            f.write(")\n")
            f.write("\n")
            
            f.write("target_link_libraries(\n")
            f.write("\t" + binaryfile + "\n")
            f.write("\n")
            f.write("\tsnark\n")
            f.write(")\n")
            f.write("\n")
            
            f.write("target_include_directories(\n")
            f.write("\t" + binaryfile + "\n")
            f.write("\n")
            f.write("\tPUBLIC\n")
            f.write("\t${DEPENDS_DIR}/libsnark\n")
            f.write("\t${DEPENDS_DIR}/libsnark/depends/libfqfft\n")
            f.write(")\n")
            f.write("\n")
        
        f.close()

def fieldT(equation):
    """Add FieldT for all integer variable in libsnark script
    
    str -> str"""
    pluslst = equation.split(" + ")
    
    for i in range(len(pluslst)):
        part = pluslst[i]
        if "*" in part:
            x, y = part.split("*")
            
            if (x.isnumeric()):
                pluslst[i] = "FieldT({})*{}".format(x, y)
            elif (y.isnumeric()):
                pluslst[i] = "FieldT({})*{}".format(y, x)
        else:
            if (part.isnumeric()):
                pluslst[i] = "FieldT({})".format(part)
            
    return " + ".join(pluslst)

class LibsnarkGenerator(object):
    def __init__(self, name, proggen):
        self.dstfile = ut.Filename(name, ".cpp")
        #self.dstfile = ut.Filename(name + "_" + PROTOCOL.lower() + "_" + VERIFIERTYPE.lower(), ".cpp")
        
        self.proggen = proggen
    
    def generateProg(self):
        """Generate libsnark program file
        
        RandomMatrix, str -> None"""
        if (PROTOCOL == "PGHR13"):
            lines, varnames = self.generateProgPGHR13()
        elif (PROTOCOL == "GROTH16"):
            lines, varnames = self.generateProgGROTH16()
        
        return lines, varnames

    def generateProgPGHR13(self):
        """Generate libsnark program file with PGHR13 protocol
        
        RandomMatrix, str -> str"""
        line = 0
        
        dst = os.path.join(PROG_OUTPUT, str(self.dstfile))
        
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
        line += 19

        for var in self.proggen.variables[1:]:
            info = "\tpb_variable<FieldT> {};\n".format(var)
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        for var in self.proggen.variables[1:]:
            info = '\t{}.allocate(pb, "{}");\n'.format(var, var)
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        info = '\tpb.set_input_sizes({});\n'.format(self.proggen.num_pubinput)
        f.write(info)
        line += 1
        
        for constraint in self.proggen.constraints:
            A, B, C = constraint
            A = str(z3.simplify(A)).replace("\n", " ")
            B = str(z3.simplify(B)).replace("\n", " ")
            C = str(z3.simplify(C)).replace("\n", " ")
            info = "\tpb.add_r1cs_constraint(r1cs_constraint<FieldT>({}, {}, {}));\n".format(fieldT(A), fieldT(B), fieldT(C))
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        for var in self.proggen.witnessvalue.keys():
            info = "\tpb.val({}) = {};\n".format(var, self.proggen.witnessvalue[var])
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        f.write("\tconst r1cs_constraint_system<FieldT> constraint_system = pb.get_constraint_system();\n\n")
        line += 2

        f.write("\tconst r1cs_ppzksnark_keypair<default_r1cs_ppzksnark_pp> keypair = r1cs_ppzksnark_generator<default_r1cs_ppzksnark_pp>(constraint_system);\n\n")

        f.write("\tconst r1cs_ppzksnark_proof<default_r1cs_ppzksnark_pp> proof = r1cs_ppzksnark_prover<default_r1cs_ppzksnark_pp>(keypair.pk, pb.primary_input(), pb.auxiliary_input());\n\n")

        if (VERIFIERTYPE == "WEAK_IC"):
            f.write("\tbool verified = r1cs_ppzksnark_verifier_weak_IC<default_r1cs_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")
        elif (VERIFIERTYPE == "STRONG_IC"):
            f.write("\tbool verified = r1cs_ppzksnark_verifier_strong_IC<default_r1cs_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")

        f.write('\tcout << "Number of R1CS constraints: " << constraint_system.num_constraints() << endl;\n')
        f.write('\tcout << "Primary (public) input: " << pb.primary_input() << endl;\n')
        f.write('\tcout << "Auxiliary (private) input: " << pb.auxiliary_input() << endl;\n')
        f.write('\tcout << "Verification status: " << verified << endl;\n\n')

        f.write("\tconst r1cs_ppzksnark_verification_key<default_r1cs_ppzksnark_pp> vk = keypair.vk;\n\n")

        f.write("\treturn 0;\n")
        f.write("}")

        f.close()
        
        return [line + 1, line + 3, line + 5], ["keypair", "proof", "verified"]
        
    def generateProgGROTH16(self):
        """Generate libsnark program file with PGHR13 protocol
        
        RandomMatrix, str -> None"""
        line = 0

        dst = os.path.join(PROG_OUTPUT, str(self.dstfile))
        
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
        line += 19

        for var in self.proggen.variables[1:]:
            info = "\tpb_variable<FieldT> {};\n".format(var)
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        for var in self.proggen.variables[1:]:
            info = '\t{}.allocate(pb, "{}");\n'.format(var, var)
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        info = '\tpb.set_input_sizes({});\n'.format(self.proggen.num_pubinput)
        f.write(info)
        line += 1
        
        for constraint in self.proggen.constraints:
            A, B, C = constraint
            A = str(z3.simplify(A)).replace("\n", " ")
            B = str(z3.simplify(B)).replace("\n", " ")
            C = str(z3.simplify(C)).replace("\n", " ")
            info = "\tpb.add_r1cs_constraint(r1cs_constraint<FieldT>({}, {}, {}));\n".format(fieldT(A), fieldT(B), fieldT(C))
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        for var in self.proggen.witnessvalue.keys():
            info = "\tpb.val({}) = {};\n".format(var, self.proggen.witnessvalue[var])
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        f.write("\tconst r1cs_constraint_system<FieldT> constraint_system = pb.get_constraint_system();\n\n")
        line += 2

        f.write("\tconst r1cs_gg_ppzksnark_keypair<default_r1cs_gg_ppzksnark_pp> keypair = r1cs_gg_ppzksnark_generator<default_r1cs_gg_ppzksnark_pp>(constraint_system);\n\n")

        f.write("\tconst r1cs_gg_ppzksnark_proof<default_r1cs_gg_ppzksnark_pp> proof = r1cs_gg_ppzksnark_prover<default_r1cs_gg_ppzksnark_pp>(keypair.pk, pb.primary_input(), pb.auxiliary_input());\n\n")

        if (VERIFIERTYPE == "WEAK_IC"):
            f.write("\tbool verified = r1cs_gg_ppzksnark_verifier_weak_IC<default_r1cs_gg_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")
        elif (VERIFIERTYPE == "STRONG_IC"):
            f.write("\tbool verified = r1cs_gg_ppzksnark_verifier_strong_IC<default_r1cs_gg_ppzksnark_pp>(keypair.vk, pb.primary_input(), proof);\n\n")

        f.write('\tcout << "Number of R1CS constraints: " << constraint_system.num_constraints() << endl;\n')
        f.write('\tcout << "Primary (public) input: " << pb.primary_input() << endl;\n')
        f.write('\tcout << "Auxiliary (private) input: " << pb.auxiliary_input() << endl;\n')
        f.write('\tcout << "Verification status: " << verified << endl;\n\n')

        f.write("\tconst r1cs_gg_ppzksnark_verification_key<default_r1cs_gg_ppzksnark_pp> vk = keypair.vk;\n\n")

        f.write("\treturn 0;\n")
        f.write("}")

        f.close()

        return [line + 1, line + 3, line + 5], ["keypair", "proof", "verified"]

class LibsnarkCompiler(object):
    def __init__(self, name):
        self.dstfile = ut.Filename(name, ".cpp")

    def compile(self):
        # Save original Makefile
        makefilepath = os.path.join(COMPILE_PATH, "src", "CMakeLists.txt")
        if (os.path.exists(makefilepath)):
            f = open(makefilepath)
            mfcontent = f.read()
            f.close()

        # Create CMakeLists
        make = CMakeLists([self.dstfile])
        make.buildmakefile()

        outprog = os.path.join(PROG_OUTPUT, str(self.dstfile))
        outbinary = os.path.join(BINARY_OUTPUT, self.dstfile.name)
        libprog = os.path.join(COMPILE_PATH, "src", str(self.dstfile))
        libbinary = os.path.join(COMPILE_PATH, "build", "src", self.dstfile.name)

        # Move program to libsnark src directory     
        shutil.copy(outprog, libprog)

        # Call make
        buildpath = os.path.join(COMPILE_PATH, "build")
        subprocess.call(["make", "-C", buildpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Move binary file from library to output directory
        shutil.copy(libbinary, outbinary)

        # Remove files in libsnark build directory
        os.remove(libprog)
        os.remove(libbinary)

        # Reverse back Makefile
        if (os.path.exists(makefilepath)):
            f = open(makefilepath, "w")
            f.write(mfcontent)
            f.close()

        return outbinary