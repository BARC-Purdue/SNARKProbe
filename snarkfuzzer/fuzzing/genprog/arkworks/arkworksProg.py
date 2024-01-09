import z3
import os
import subprocess
import shutil

import fuzzing.utils.fuzzMatrix as mt
import fuzzing.utils.utils as ut

from config import *

def plusList(equation):
    """Add FieldT for all integer variable in arkworks script
    
    str -> str"""
    pluslst = equation.split(" + ")
    
    for i in range(len(pluslst)):
        part = pluslst[i]
        if "*" in part:
            x, y = part.split("*")
            
            if (x.isnumeric()):
                if (x != "1"):
                    pluslst[i] = "(ConstraintF::from({}), {})".format(x, y)
                elif (x == "1"):
                    pluslst[i] = y
            elif (y.isnumeric()):
                if (y != "1"):
                    pluslst[i] = "(ConstraintF::from({}), {})".format(y, x)
                elif (y == "1"):
                    pluslst[i] = x
        else:
            if (part.isnumeric()):
                if (part != "1"):
                    pluslst[i] = "(ConstraintF::from({}), Variable::One)".format(part)
                elif (part == "1"):
                    pluslst[i] = "Variable::One"
            
    return " + ".join(pluslst)

class Cargotoml(object):
    def __init__(self, filename):
        """Create Cargo.toml file
        
        Cargo.toml, str -> None"""
        self.filename = filename
        
    def buildcargotoml(self, cgcontent):
        """Save Cargo.toml file to dependent library
        
        Cargotoml -> None"""  
        filepath = os.path.join(COMPILE_PATH, "Cargo.toml")

        prog_name = self.filename.name
        
        f = open(filepath, "w")
        f.write(cgcontent)
        f.write("\n")
        f.write("[[bin]]\n")
        f.write("name = \"{}\"\n".format(prog_name))
        f.write("path = \"{}\"\n".format("src/" + prog_name + ".rs"))
        
        f.close()

class ArkworksGenerator(object):
    def __init__(self, name, proggen):
        self.dstfile = ut.Filename(name, ".rs")

        self.proggen = proggen
        
    def generateProg(self):
        """Generate libsnark program file
        
        RandomMatrix, str -> None"""
        if (PROTOCOL == "GROTH16"):
            lines, varnames = self.generateProgGROTH16()
        else:
            raise Exception
            
        return lines, varnames
        
    def generateProgGROTH16(self):
        """Generate bellman program file with Groth16 protocol
        
        RandomMatrix, str -> None"""
        line = 0

        dst = os.path.join(PROG_OUTPUT, str(self.dstfile))
        
        f = open(dst, "w")

        f.write('use ark_groth16::{create_random_proof, generate_random_parameters, prepare_verifying_key, verify_proof};\n')
        f.write('use ark_ff::Field;\n')
        f.write('use ark_std::test_rng;\n')
        f.write('use ark_relations::{lc, r1cs::{ConstraintSynthesizer, ConstraintSystemRef, SynthesisError, Variable}};\n')
        f.write('use ark_bls12_381::Bls12_381;\n')
        f.write('use ark_bls12_381::Fr;\n\n')
        
        line += 7

        f.write("struct Circuit<F: Field> {\n")
        line += 1
        for var in self.proggen.variables[1:]:
            f.write('\t{}: Option<F>,\n'.format(var))
            line += 1
        f.write('}\n\n')
        line += 2

        f.write("impl<ConstraintF: Field + std::convert::From<i32>> ConstraintSynthesizer<ConstraintF> for Circuit<ConstraintF> {\n")
        f.write("\tfn generate_constraints(self, cs: ConstraintSystemRef<ConstraintF>) -> Result<(), SynthesisError> {\n")
        line += 2
        
        for output_var in self.proggen.variables[1:(self.proggen.num_pubinput + 1)]:
            info = "\t\tlet {} = cs.new_input_variable(|| self.{}.ok_or(SynthesisError::AssignmentMissing))?;\n".format(output_var, output_var)
            f.write(info)
            line += 1
        
        for var in self.proggen.variables[(self.proggen.num_pubinput + 1):]:
            info = "\t\tlet {} = cs.new_witness_variable(|| self.{}.ok_or(SynthesisError::AssignmentMissing))?;\n".format(var, var)
            f.write(info)
            line += 1
        f.write("\n")
        line += 1

        # enforce
        i = 0
        for constraint in self.proggen.constraints:
            A, B, C = constraint
            A = str(z3.simplify(A)).replace("\n", " ")
            B = str(z3.simplify(B)).replace("\n", " ")
            C = str(z3.simplify(C)).replace("\n", " ")
            info = "\t\tcs.enforce_constraint(lc!() + {}, lc!() + {}, lc!() + {});\n".format(plusList(A), plusList(B), plusList(C))
            f.write(info)
            line += 1
            i = i + 1
        f.write("\n")
        f.write("\t\tOk(())\n")
        f.write("\t}\n")
        f.write("}\n\n")
        line += 5

        f.write('fn main(){\n')
        f.write('\tlet rng = &mut test_rng();\n')
        f.write('\tprintln!("Creating parameters...");\n')
        f.write('\tlet params = generate_random_parameters::<Bls12_381, _, _>(Circuit {\n')
        line += 4

        for var in self.proggen.variables[1:]:
            f.write('\t\t{}: None,\n'.format(var))
            line += 1

        f.write('\t\t}, rng).unwrap();\n')
        line += 1
        line1 = line

        f.write('\tlet pvk = prepare_verifying_key::<Bls12_381>(&params.vk);\n\n')
        line += 2
        f.write('\tprintln!("Creating proofs...");\n\n')
        line += 2
        
        pub_input_list = []
        i = 0
        while (i < self.proggen.num_pubinput):
            var = list(self.proggen.witnessvalue.keys())[i]
            f.write('\tlet public_input_{} = Fr::from({}u8);\n'.format(i, self.proggen.witnessvalue[var]))
            line += 1
            pub_input_list.append("public_input_{}".format(i))
            i += 1
        
        f.write('\tlet proof = create_random_proof(\n') 
        f.write('\t\tCircuit {\n')
        line += 2
        for j in range(self.proggen.num_pubinput): 
            f.write('\t\t\tsym_{}: Some(public_input_{}),\n'.format(j, j))
            line += 1

        while (i < len(self.proggen.witnessvalue.keys())):
            var = list(self.proggen.witnessvalue.keys())[i]
            f.write('\t\t\t{}: Some(Fr::from({}u8)),\n'.format(var, self.proggen.witnessvalue[var]))
            line += 1
            i += 1
        f.write('\t\t},\n')
        f.write('\t\t&params,\n')
        f.write('\t\trng,\n')
        f.write('\t).unwrap();\n\n')
        line += 4
        line2 = line
        line += 1

        pub_input_str = ", ".join(pub_input_list)
        f.write('\tlet verified = verify_proof(&pvk, &proof, &[{}]).unwrap();\n'.format(pub_input_str))
        line += 1
        line3 = line
        f.write('\tprintln!("{}", verified);\n')
        f.write('}\n')

        f.close()
    
        return [line1, line2, line3], ["params", "proof", "verified"]

class ArkworksCompiler(object):
    def __init__(self, name):
        self.dstfile = ut.Filename(name, ".rs")

    def compile(self):
        # Save original Cargo.toml
        makefilepath = os.path.join(COMPILE_PATH, "Cargo.toml")
        if (os.path.exists(makefilepath)):
            f = open(makefilepath)
            cgcontent = ""
            for x in f:
                if ("dev-dependencies" in x): continue
                cgcontent = cgcontent + x
            f.close()

        outprog = os.path.join(PROG_OUTPUT, str(self.dstfile))
        outbinary = os.path.join(BINARY_OUTPUT, self.dstfile.name)
        libprog = os.path.join(COMPILE_PATH, "src", str(self.dstfile))
        libbinary = os.path.join(COMPILE_PATH, "target", "debug", self.dstfile.name)
<<<<<<< HEAD

        # Move program to bellman src directory     
        shutil.copy(outprog, libprog)

=======
        
        # Move program to bellman src directory     
        shutil.copy(outprog, libprog)
        
>>>>>>> 8f142d531b3e04691f10278a57f47e7202ca5511
        # Create Cargo.toml
        make = Cargotoml(self.dstfile)
        make.buildcargotoml(cgcontent)

        # Call Cargo
        buildpath = os.path.join(COMPILE_PATH, "Cargo.toml")
        subprocess.call(["cargo", "build", "--manifest-path=" + buildpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
<<<<<<< HEAD

=======
        
>>>>>>> 8f142d531b3e04691f10278a57f47e7202ca5511
        # Move binary file from library to output directory
        shutil.copy(libbinary, outbinary)

        # Remove files in libsnark build directory
        os.remove(libprog)
        os.remove(libbinary)
        os.remove(libbinary + ".d")

        # Reverse back Makefile
        if (os.path.exists(makefilepath)):
            f = open(makefilepath, "w")
            f.write(cgcontent)
            f.close()

        return outbinary