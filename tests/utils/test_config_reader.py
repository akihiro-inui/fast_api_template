import os
import sys
import unittest
sys.path.insert(0, os.getcwd())
from src.utils.custom_error_handlers import ConfigError


class ConfigReaderTest(unittest.TestCase):
    @staticmethod
    def _load_config_variable():
        from src.utils.config_reader import CFG
        return CFG

    def test_01_read_config(self):
        os.environ["ENV"] = "wrong_environment"
        self.assertRaises(ConfigError, ConfigReaderTest._load_config_variable)

    def test_02_read_config_wrong_environment(self):
        del os.environ["ENV"]
        os.environ["ENV"] = "test"
        CFG = ConfigReaderTest._load_config_variable()
        self.assertNotEqual(CFG, None)
