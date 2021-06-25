


###############################################################################
#
#                            This is not for you.
#
###############################################################################

#Self registration for use with json loading.
#see: https://stackoverflow.com/questions/55973284/how-to-create-self-registering-factory-in-python/55973426

import os, sys
import logging
import pkgutil

class SelfRegistering(object):

    class ClassNotFound(Exception): pass

    def __init__(self, *args, **kwargs):
        #ignore args.
        super().__init__()

    @classmethod
    def GetSubclasses(cls):
        for subclass in cls.__subclasses__():
            # logging.info(f"Subclass dict: {subclass.__dict__}")
            yield subclass
            for subclass in subclass.GetSubclasses():
                yield subclass

    #TODO: How do we pass args to the subsequently called __init__()?
    def __new__(cls, classname, *args, **kwargs):
        for subclass in cls.GetSubclasses():
            # logging.info(f"New Datum {classname} - looking at subclass {subclass.__name__}")
            if subclass.__name__ == classname:

                # Using "object" base class method avoids recursion here.
                child = object.__new__(subclass)

                #__dict__ is always blank during __new__ and only populated by __init__.
                #This is only useful as a negative control.
                # logging.debug(f"Created object of {child.__dict__}")

                return child
        
        # no subclass with matching classname found (and no default defined)
        raise SelfRegistering.ClassNotFound(f'No known SelfRegistering class: {classname}')

def RegisterAllClassesInDirectory(directory):
    logging.debug(f"Loading SelfRegistering classes in {directory}")
    # logging.debug(f"Available files: {os.listdir(directory)}")
    for importer, datumFile, _ in pkgutil.iter_modules([directory]):
        logging.debug(f"Found {datumFile} with {importer}")
        if datumFile not in sys.modules and datumFile != 'main':
            module = importer.find_module(datumFile).load_module(datumFile)
