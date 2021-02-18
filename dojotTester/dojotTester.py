#!/usr/bin/env python
"""
This script is the entry point for running tests
"""
import argparse
import os
from utils import Utils

import fnmatch
import importlib
import unittest
import sys


class ListTestsAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest,
                 default=False,
                 required=False,
                 help=None):
        super(ListTestsAction, self).__init__(
            option_strings=option_strings,
            nargs=0,
            dest=dest,
            const=False,
            default=default,
            required=required,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        # le os testes disponiveis e os exibe
        test_modules = load_test_modules()
        mod_count = 0
        test_count = 0
        all_groups = set()
        for (modname, (mod, tests)) in test_modules.items():
            mod_count += 1
            desc = (mod.__doc__ or "No description").strip().split('\n')[0]
            print("  Module %13s: %s" % (mod.__name__, desc))

            for (testname, test) in tests.items():
                desc = (test.__doc__ or "No description").strip().split('\n')[0]

                groups = set(test._groups) - {"all", modname}
                all_groups.update(test._groups)
                if groups:
                    desc = "(%s) %s" % (",".join(groups), desc)

                start_str = " %s %s:" % (test._disabled and "!" or " ",
                                         testname)
                print("  %22s : %s" % (start_str, desc))
                test_count += 1

        print("'%d' modules shown with a total of '%d' tests\n" %
              (mod_count, test_count))
        print("Test groups: %s" % (', '.join(sorted(all_groups))))

        print('Test list:')
        for (modname, (mod, tests)) in test_modules.items():
            for (testname, test) in tests.items():
                print("%s.%s" % (modname, testname))

        sys.exit(0)


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
                    mod = importlib.import_module("tests." + modname)
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
                    if not hasattr(test, "_disabled"):
                        test._disabled = False

                    # Put test in its module's test group
                    if not test._disabled:
                        test._groups.append(modname)

                    # Put test in the all test group
                    if not test._disabled:
                        test._groups.append("all")

                result[modname] = (mod, tests)

    return result


def get_test(name):
    test_modules = load_test_modules()

    sorted_tests = []

    for (modname, (mod, tests)) in sorted(test_modules.items()):
        for (testname, test) in sorted(tests.items()):
            sorted_tests.append(test)

    logger.debug("test modules:" + str(sorted_tests))

    # verify if name is a suite
    if name in test_modules.keys():
        logger.info('Suite found')
        suite = unittest.TestSuite()
        _, tests = test_modules[name]
        for testname, test in tests.items():
            suite.addTest(test())
        return suite

    for test in sorted_tests:
        if name == test.__name__:
            return test


if __name__ == "__main__":
    if "linux" in sys.platform and os.getuid() != 0:
        print("Super-user privileges required. Please re-run with sudo or as root.")
        sys.exit(1)

    # Building the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("test", help="Test or test suite")
    parser.add_argument("-l", "--list", help="List available tests and exit", action=ListTestsAction)
    args = parser.parse_args()
    teste = args.test
    logger.info("Trying to execute test " + teste)

    runner = unittest.TextTestRunner(verbosity=2)

    test_obj = get_test(teste)

    if type(test_obj) == unittest.TestSuite:
        runner.run(test_obj)
    else:
        runner.run(test_obj())
