import z3
import os
import subprocess
import shutil

import fuzzing.utils.fuzzMatrix as mt
import fuzzing.utils.utils as ut

from config import *

def plusList(equation):
    """Add FieldT for all integer variable in libsnark script
    
    str -> str"""
    pluslst = equation.split(" + ")
    
    for i in range(len(pluslst)):
        part = pluslst[i]
        if "*" in part:
            x, y = part.split("*")
            
            if (x.isnumeric()):
                if (x != "1"):
                    pluslst[i] = "(E::Fr::from_str(\"{}\").unwrap(), {})".format(x, y)
                elif (x == "1"):
                    pluslst[i] = y
            elif (y.isnumeric()):
                if (y != "1"):
                    pluslst[i] = "(E::Fr::from_str(\"{}\").unwrap(), {})".format(y, x)
                elif (y == "1"):
                    pluslst[i] = x
        else:
            if (part.isnumeric()):
                if (part != "1"):
                    pluslst[i] = "(E::Fr::from_str(\"{}\").unwrap(), CS::one())".format(part)
                elif (part == "1"):
                    pluslst[i] = "CS::one()"
            
    return " + ".join(pluslst)

class Cargotoml(object):
    def __init__(self, filename):
        """Create Cargo.toml file
        
        Cargo.toml, str -> None"""
        self.filename = filename
        
    def buildcargotoml(self):
        """Save Cargo.toml file to dependent library
        
        Cargotoml -> None"""  
        filepath = os.path.join(COMPILE_PATH, "Cargo.toml")

        prog_name = self.filename.name
        
        f = open(filepath, "w")
        f.write("[package]\n")
        f.write("name = \"{}\"\n".format(prog_name))
        f.write("version = \"0.1.0\"\n")
        f.write("edition = \"2021\"\n")
        f.write("\n")
        f.write("[[bin]]\n")
        f.write("name = \"{}\"\n".format(prog_name))
        f.write("path = \"{}\"\n".format("src/" + prog_name + ".rs"))
        f.write("\n")
        f.write("[dependencies]\n")
        f.write("rand = \"0.4\"\n")
        f.write("bit-vec = \"0.4.4\"\n")
        f.write("pairing = \"0.14\"\n")
        f.write("byteorder = \"1\"\n")
        f.write("bellman = \"0.1.0\"\n")
        
        f.close()

class BellmanGenerator(object):
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

        f.write('#![allow(unused_imports)]\n')
        f.write('#![allow(unused_variables)]\n')
        f.write('extern crate bellman;\n')
        f.write('extern crate pairing;\n')
        f.write('extern crate rand;\n\n')

        f.write('use self::rand::{thread_rng, Rng};\n')
        f.write('use self::pairing::{Engine, Field, PrimeField};\n')
        f.write('use self::pairing::bls12_381::{Bls12, Fr};\n')
        f.write('use self::bellman::{Circuit, ConstraintSystem, SynthesisError};\n')
        f.write('use self::bellman::groth16::{Proof, generate_random_parameters, prepare_verifying_key, create_random_proof, verify_proof};\n\n')
        line += 12

        f.write("pub struct TestDemo<E: Engine> {\n")
        line += 1
        for var in self.proggen.variables[1:]:
            f.write('\tpub {}: Option<E::Fr>,\n'.format(var))
            line += 1
        f.write('}\n\n')
        line += 2

        f.write("impl <E: Engine> Circuit<E> for TestDemo<E> {\n")
        f.write("\tfn synthesize<CS: ConstraintSystem<E>>(self, cs: &mut CS) -> Result<(), SynthesisError>\n")
        f.write('\t{\n')
        line += 3

        # alloc
        # NOTE: first one is output/primary variable
        
        for output_var in self.proggen.variables[1:(self.proggen.num_pubinput + 1)]:
            info_1 = "\t\tlet {} = cs.alloc_input(|| \"{}\", || {{".format(output_var, output_var)
            info_2 = "self.{}.ok_or(SynthesisError::AssignmentMissing)}})?;\n".format(output_var)
            info = info_1 + info_2
            f.write(info)
            line += 1
        
        for var in self.proggen.variables[(self.proggen.num_pubinput + 1):]:
            info_1 = "\t\tlet {} = cs.alloc(|| \"{}\", || {{".format(var, var)
            info_2 = "self.{}.ok_or(SynthesisError::AssignmentMissing)}})?;\n".format(var)
            info = info_1 + info_2
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
            info = "\t\tcs.enforce(|| \"{}\", |lc| lc + {}, |lc| lc + {}, |lc| lc + {});\n".format("constraint_" + str(i), plusList(A), plusList(B), plusList(C))
            f.write(info)
            line += 1
            i = i + 1
        f.write("\n")

        f.write("\t\tOk(())\n")
        f.write("\t}\n")
        f.write("}\n\n")

        f.write('fn main(){\n')
        
        f.write('\tlet rng = &mut thread_rng();\n\n')
        
        f.write('\tprintln!("Creating parameters...");\n\n')
        
        f.write('\tlet params = {\n')

        f.write('\t\tlet c = TestDemo::<Bls12> {\n')
        line += 12

        for var in self.proggen.variables[1:]:
            f.write('\t\t\t{}: None,\n'.format(var))
            line += 1

        f.write('\t\t};\n')
        f.write('\t\tgenerate_random_parameters(c, rng).unwrap()\n')
        f.write('\t};\n\n')
        line += 3
        line1 = line

        f.write('\tlet pvk = prepare_verifying_key(&params.vk);\n\n')
        line += 3
        f.write('\tprintln!("Creating proofs...");\n\n')
        line += 2
        
        pub_input_list = []
        i = 0

        while (i < self.proggen.num_pubinput):
            var = list(self.proggen.witnessvalue.keys())[i]
            f.write('\tlet public_input_{} = Fr::from_str(\"{}\");\n'.format(i, self.proggen.witnessvalue[var]))
            line += 1
            pub_input_list.append("public_input_{}.unwrap()".format(i))
            i += 1
        
        f.write('\tlet c = TestDemo::<Bls12> {\n') 
        line += 1
        for j in range(self.proggen.num_pubinput): 
            f.write('\t\tsym_{}: public_input_{},\n'.format(j, j))
            line += 1

        while (i < len(self.proggen.witnessvalue.keys())):
            var = list(self.proggen.witnessvalue.keys())[i]
            f.write('\t\t{}: Fr::from_str(\"{}\"),\n'.format(var, self.proggen.witnessvalue[var]))
            line += 1
            i += 1

        # for var in self.proggen.witnessvalue.keys():
        #     if (i < self.proggen.num_pubinput):
        #         f.write('\tlet public_input_{} = Fr::from_str(\"{}\");\n'.format(i, self.proggen.witnessvalue[var]))
        #         line += 1
        #         pub_input_list.append("public_input_{}.unwrap()".format(i))
        #     elif (i == self.proggen.num_pubinput):
        #         f.write('\n\tlet c = TestDemo::<Bls12> {\n') 
        #         line += 2 
        #         for j  in range(self.proggen.num_pubinput): 
        #             f.write('\t\tsym_{}: public_input_{},\n'.format(j, j))
        #             line += 1
        #         f.write('\t\t{}: Fr::from_str(\"{}\"),\n'.format(var, self.proggen.witnessvalue[var]))
        #         line += 1
        #     else:
        #         f.write('\t\t{}: Fr::from_str(\"{}\"),\n'.format(var, self.proggen.witnessvalue[var]))
        #         line += 1
        #     i = i + 1

        f.write('\t};\n\n')
        line += 2

        f.write('\tlet proof = create_random_proof(c, &params, rng).unwrap();\n\n')
        line += 1
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

class BellmanCompiler(object):
    def __init__(self, name):
        self.dstfile = ut.Filename(name, ".rs")

    def compile(self):
        # Save original Cargo.toml
        makefilepath = os.path.join(COMPILE_PATH, "Cargo.toml")
        if (os.path.exists(makefilepath)):
            f = open(makefilepath)
            cgcontent = f.read()
            f.close()

        outprog = os.path.join(PROG_OUTPUT, str(self.dstfile))
        outbinary = os.path.join(BINARY_OUTPUT, self.dstfile.name)
        libprog = os.path.join(COMPILE_PATH, "src", str(self.dstfile))
        libbinary = os.path.join(COMPILE_PATH, "target", "debug", self.dstfile.name)

        # Move program to bellman src directory     
        shutil.copy(outprog, libprog)

        # Create Cargo.toml
        make = Cargotoml(self.dstfile)
        make.buildcargotoml()

        # Call Cargo
        buildpath = os.path.join(COMPILE_PATH, "Cargo.toml")
        subprocess.call(["cargo", "build", "--manifest-path=" + buildpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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