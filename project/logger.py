import logging

from utils.path_locator import get_package_location
from project import EnvironmentConfig


class PaddedFormatter(logging.Formatter):
    def format(self, record):
        record.name = f"{record.name:<12}"
        record.levelname = f"{record.levelname:<5}"
        record.filename = f"{record.filename:<18}"
        record.funcName = f"{record.funcName:<25}"
        record.lineno = int(record.lineno)
        return super().format(record)


class Logger:
    def __init__(self):
        name, level, file_name = self.get_logger_config()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = PaddedFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            if file_name is not None and file_name != '':
                file_location = get_package_location() + "/" + file_name
                file_handler = logging.FileHandler(file_location)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            self.logger.propagate = False

    @staticmethod
    def get_logger_config():
        try:
            file = EnvironmentConfig.get_string('logger.file_name')
        except KeyError:
            file = None
        logger_name = EnvironmentConfig.get_string('logger.logger_name')
        logger_level = EnvironmentConfig.get_string('logger.level')
        level = logging.INFO
        match logger_level:
            case 'debug':
                level = logging.DEBUG
            case 'info':
                level = logging.INFO
            case 'warning':
                level = logging.WARNING
            case 'error':
                level = logging.ERROR
            case _:
                level = logging.INFO
        return logger_name, level, file

def get_logger():
    return Logger().logger
