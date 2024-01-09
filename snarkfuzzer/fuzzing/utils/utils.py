class Filename(object):
    def __init__(self, name, ext):
        self.name = name
        self.ext = ext
        
    def __str__(self):
        return self.name + self.ext
    
    def __repr__(self):
        return str(self)