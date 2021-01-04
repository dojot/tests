from utils import Utils
import unittest


class BaseTest(unittest.TestCase):
    def __str__(self):
        return self.id().replace('.runTest', '')

    def setUp(self):
        self.logger = Utils.create_logger(str(self))
        self.logger.info("** START TEST CASE " + str(self))


    def tearDown(self):

        self.logger.info("** END TEST CASE " + str(self))

    def assertTrue(self, cond, msg):
        if not cond:
            self.logger.error("** FAILED ASSERTION: " + msg)
        unittest.TestCase.assertTrue(self, cond, msg)
