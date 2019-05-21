import unittest
import logging
from lib.configuration_reader import ConfigReader


class BaseTest(unittest.TestCase):
    CONFIG = ConfigReader().load_configuration_from_file('configuration.json')

    @classmethod
    def setUpClass(cls):
        logging.info('New test suite started')

    def setUp(self):
        logging.info('Testcase started')

    def tearDown(self):
        logging.info('Testcase finished')

    @classmethod
    def tearDownClass(cls):
        logging.info('Test suite finished')