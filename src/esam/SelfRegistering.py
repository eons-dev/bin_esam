


###############################################################################
#
#                            This is not for you.
#
###############################################################################

#Self registration for use with json loading.
#see: https://stackoverflow.com/questions/55973284/how-to-create-self-registering-factory-in-python/55973426

import logging

class SelfRegistering(object):

    class Unknown(Exception): pass

    def __init__(self):
        super().__init__()

    @classmethod
    def GetSubclasses(cls):
        for subclass in cls.__subclasses__():
            # logging.info(f"Subclass dict: {subclass.__dict__}")
            yield subclass
            for subclass in subclass.GetSubclasses():
                yield subclass

    def __new__(cls, name):
        for subclass in cls.GetSubclasses():
            # logging.info(f"New Datum {name} - looking at subclass {subclass.__name__}")
            if subclass.__name__ == name:
                # Using "object" base class method avoids recursion here.
                child = object.__new__(subclass)
                logging.debug(f"Created object of {child.__dict__}")
                return child
        # no subclass with matching name found (and no default defined)
        raise SelfRegistering.Unknown(f'No known SelfRegistering class: {name}')


def RegisterAllClassesInDirectory(directory):
    for importer, datumFile, _ in pkgutil.iter_modules([directory]):
        if datumFile not in sys.modules and datumFile != 'main':
            module = importer.find_module(datumFile).load_module(datumFile)
