import unittest2 as unittest
import time
import sys

class _WritelnDecorator: 
    """Used to decorate file-like objects with a handy 'writeln' method""" 
    
    def __init__(self,stream): 
        self.stream = stream

    # Needed for pickling between processes
    def __setstate__(self, data):
        self.__dict__.update(data)
   
    def __getattr__(self, attr): 
        return getattr(self.stream,attr) 

    def writeln(self, arg=None): 
        if arg: self.write(arg) 
        self.write('\n') 

class CCParallelTextTestRunner(unittest.TextTestRunner):
    
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1): 
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions 
        self.verbosity = verbosity
        
    def run(self, test): 
        "Run the given test case or test suite." 
        result = self._makeResult() 
        startTime = time.time() 
        test(result) 
        stopTime = time.time() 
        timeTaken = stopTime - startTime 
        result.printErrors() 
        run = result.testsRun 
        return result

