
from importlib.resources import path

class FileParam(object):
    def __init__(self, path, line, varname):
        self.path = path
        self.line = line
        self.varname = varname

    def __str__(self):
        return "FileParam({}, {}, {})".format(self.path, self.line, self.varname)

    def __repr__(self):
        return str(self)

class ModelSource(object):
    def __init__(self, generator, prover, verifier, progname, groundtruth):
        self.generator = generator
        self.prover = prover
        self.verifier = verifier

        self.progname = progname

        self.groundtruth = groundtruth

    def __str__(self):
        return "ProgName: {}\nGroundTruth: {}\nGenerator: {}\nProver: {}\nVerifier: {}".format(self.progname,
                                                                                               self.groundtruth,
                                                                                               self.generator,
                                                                                               self.prover,
                                                                                               self.verifier)