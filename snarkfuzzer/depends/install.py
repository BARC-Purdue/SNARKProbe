import subprocess

MFUZZ = True

if (MFUZZ):
    PATH = "libsnark-for-mfuzz" 
    URL = "https://github.com/fanym919/libsnark-for-mfuzz.git"
else:
    PATH = "libsnark-tutorial"
    URL = "https://github.com/howardwu/libsnark-tutorial.git"


def replace(flag):
    result = subprocess.run(["grep", "-r", flag, "./" + PATH], stdout = subprocess.PIPE, text = True)

    info = result.stdout.strip("\n").split("\n")
    
    for line in info:
        if (line.startswith("Binary file")):
            continue
        
        file, *_ = line.split(":")

        command =["sed", "-i", "s/" + flag + "//g", file]
        subprocess.run(command)

def removeflag():
    flags = ["\-O0", "\-O2", "\-O3", "\-Os"]
    for flag in flags:
        replace(flag)
        
def git2https():
    result = subprocess.run(["grep", "-r", "git:", "./" + PATH], stdout = subprocess.PIPE, text = True)
    
    info = result.stdout.strip("\n").split("\n")
    
    for line in info:
        file, *_ = line.split(":")
        
        command =["sed", "-i", "s/git:/https:/g", file]
        subprocess.run(command)

def install():
    subprocess.run(["rm", "-rf", PATH])
    subprocess.run(["git", "clone", URL])
    
    subprocess.run(["git", "submodule", "init"], cwd = PATH + "/depends/libsnark")
    subprocess.run(["git", "submodule", "update"], cwd = PATH + "/depends/libsnark")
    
    git2https()
    
    subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd = PATH)
    subprocess.run(["mkdir", "build"], cwd = PATH)
    subprocess.run(["cmake", ".."], cwd = PATH + "/build")
    removeflag()
    subprocess.run(["make"], cwd = PATH + "/build")

if __name__ == "__main__":
    install()
    
    print("END OF INSTALLATION")
