import yaml
import os

from utils.path_locator import get_package_location


class EnvironmentConfig:
    _configuration = None

    @classmethod
    def load_configuration(cls):
        if cls._configuration is None:
            try:
                path = os.path.join(get_package_location(), 'configuration.yaml')
                with open(path, 'r') as configuration_file:
                    cls._configuration = yaml.safe_load(configuration_file)
            except FileNotFoundError:
                print('Configuration file not found')
                exit(1)
            except Exception as e:
                print(f"Exception while loading configuration file: {str(e)}")
                exit(1)

    @classmethod
    def get_values(cls, key):
        cls.load_configuration()
        values = cls._configuration
        keys = key.split('.')
        for key in keys:
            if isinstance(values, dict):
                values = values.get(key)
            else:
                values = None
        return values

    @classmethod
    def get_string(cls, key):
        value = cls.get_values(key)
        if value:
            return str(value)
        else:
            return ""

    @classmethod
    def get_boolean(cls, key):
        value = cls.get_values(key)
        if value:
            if value in [1, '1', 'true', 'True', True]:
                return True
            elif value in [0, '0', 'false', 'False', False]:
                return False
            else:
                return False
        else:
            return False

    @classmethod
    def get_tuple(cls, key):
        value = cls.get_values(key)
        if value:
            return tuple(value)
        else:
            return ()
            

