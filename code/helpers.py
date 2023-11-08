
def load():
    return

def print_versions(modules):
    """
        Prints the names and versions of Python modules. This is useful for 
        understanding which version of a module was used to run a program.
        
        Parameters:
            modules: Array-like of Python modules
    """
    
    for module in modules:
        print(module.__name__ + "==" + module.__version__)
    return