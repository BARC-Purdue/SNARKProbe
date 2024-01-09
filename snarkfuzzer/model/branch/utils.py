import os

def validpath(path):
    """Format the directory or file path and remove necessary actions (e.g. ../)
    
    str -> str"""
    node = path.split("/")
    
    while "." in node:
        node.remove(".")
        
    while ".." in node:
        index = node.index("..")
        if (index > 0):
            del node[index]
            del node[index - 1]
    
    if (path.startswith("./")):
        node.insert(0, "./")
    elif (path.startswith("/")):
        node.insert(0, "/")
    
    return os.path.join(*node)