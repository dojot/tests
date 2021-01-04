import argparse
import os
from utils import Utils

import fnmatch
import importlib
import unittest
import sys

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

logger = Utils.create_logger("root")

def load_test_modules():


    result = {}

    for root, dirs, filenames in os.walk(os.path.join(ROOT_DIR, "tests")):
        # Iterate over each python file
        for filename in fnmatch.filter(filenames, '[!.]*.py'):
            modname = os.path.splitext(os.path.basename(filename))[0]

            try:
                if modname in sys.modules:
                    mod = sys.modules[modname]
                else:
                    mod = importlib.import_module("tests."+modname)
            except:
                logger.warning("Could not import file " + filename)
                raise

            # Find all testcases defined in the module
            tests = dict((k, v) for (k, v) in mod.__dict__.items() if type(v) == type and
                                                                      issubclass(v, unittest.TestCase) and
                                                                      hasattr(v, "runTest"))
            if tests:
                for (testname, test) in tests.items():
                    # Set default annotation values
                    if not hasattr(test, "_groups"):
                        test._groups = []
                    if not hasattr(test, "_nonstandard"):
                        test._nonstandard = False
                    if not hasattr(test, "_disabled"):
                        test._disabled = False

                    # Put test in its module's test group
                    if not test._disabled:
                        test._groups.append(modname)

                    # Put test in the standard test group
                    if not test._disabled and not test._nonstandard:
                        test._groups.append("standard")
                        test._groups.append("all") # backwards compatibility

                result[modname] = (mod, tests)

    return result

def getTest(name):
    test_modules = load_test_modules()

    sorted_tests = []
    for (modname, (mod, tests)) in sorted(test_modules.items()):
        for (testname, test) in sorted(tests.items()):
            sorted_tests.append(test)

    for test in sorted_tests:
        if name == test.__name__:
            return test

if __name__ == "__main__":
    if "linux" in sys.platform and os.getuid() != 0:
        print("Super-user privileges required. Please re-run with sudo or as root.")
        sys.exit(1)

    # Building the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("test")
    args = parser.parse_args()
    teste = args.test
    logger.info("Trying to execute test " + teste)

    result = unittest.TextTestRunner(verbosity=2).run(getTest(teste)())
