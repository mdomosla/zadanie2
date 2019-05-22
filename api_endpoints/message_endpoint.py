from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from lib.configuration_reader import ConfigReader


class MessageMethods:

    rand = RandomGenerator()
    rm = RequestManager()

    def __init__(self, thread_id):
        self.thread_id = thread_id
        CONFIG = ConfigReader().load_configuration_from_file('configuration.json')
        self.url = CONFIG['API_ADDRESS'] + '/threads/id/' + self.thread_id + '/messages'
        self.message_url = self.url + '/id/'

    def view_messages(self, authorization):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        result = self.rm.get_request(self.url, headers=headers)
        return result

    def send_message_in_thread(self, authorization, message=None):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        data = {
            "message": message
        }
        result = self.rm.post_request(url=self.url, headers=headers, data=data)
        return result
