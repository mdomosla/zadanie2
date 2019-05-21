from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from lib.configuration_reader import ConfigReader


class ThreadsMethods:
    rand = RandomGenerator()
    rm = RequestManager()
    CONFIG = ConfigReader().load_configuration_from_file('configuration.json')
    url = CONFIG['API_ADDRESS'] + '/threads'

    def create_sample_thread(self, authorization, thread_name=None, private=False):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        data = {
            "name":thread_name,
            "private":private
        }
        result = self.rm.post_request(url=self.url, headers=headers, data=data)
        return result
