import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configuration')


class ConfigReader:

    @staticmethod
    def load_configuration_from_file(file_name):
        """
        Function opens configuration file from configuration directory
        :param file_name: config file name to read
        :return: data from json file
        """
        file_location = os.path.join(CONFIG_PATH, file_name)
        with open(file_location, 'r') as file:
            config = json.load(file)
        return config
