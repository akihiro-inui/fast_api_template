import os
import configparser


class ConfigReader:
    """
    Reading configuration file data. Define module specific configuration in different functions.
    """

    def __init__(self, config_file_path: str):
        """
        Read common configuration data from configuration file
        """
        cfg = configparser.ConfigParser()
        self.cfg = cfg
        assert os.path.isfile(config_file_path), config_file_path + " is not a valid configuration file!"
        cfg.read(config_file_path)

        # Read category specific config
        self.__init_db(cfg)

    def __init_db(self, cfg):
        # Parameters for database
        self.DB_HOST = str(cfg.get('database', 'host'))
        self.DB_PORT = str(cfg.get('database', 'port'))
        self.DB_NAME = str(cfg.get('database', 'name'))
        self.DB_USER = str(cfg.get('database', 'user'))
        self.DB_PASSWORD = str(cfg.get('database', 'password'))


# This is the list of environments in config folder
accepted_env_values = ['test', 'development', 'production']
try:
    env = os.environ['ENV']
except KeyError:
    raise Exception(f"Pass env variable ENV with values: {', '.join(accepted_env_values)}")

if env not in accepted_env_values:
    raise Exception(f"Wrong ENV value. Got {env}, should be: {', '.join(accepted_env_values)}")

CFG = ConfigReader(f"../config/{env}.ini")