from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from lib.configuration_reader import ConfigReader


class MessageMethods:
    def __init__(self, thread_id):
        self.thread_id = thread_id
        CONFIG = ConfigReader().load_configuration_from_file('configuration.json')
        url = CONFIG['API_ADDRESS'] + '/threads/' + self.thread_id + '/messages'

    rand = RandomGenerator()
    rm = RequestManager()
    CONFIG = ConfigReader().load_configuration_from_file('configuration.json')
    url = CONFIG['API_ADDRESS'] + '/threads/' +