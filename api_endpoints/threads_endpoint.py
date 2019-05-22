from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from lib.configuration_reader import ConfigReader


class ThreadsMethods:
    rand = RandomGenerator()
    rm = RequestManager()
    CONFIG = ConfigReader().load_configuration_from_file('configuration.json')
    url = CONFIG['API_ADDRESS'] + '/threads'
    thread_url = CONFIG['API_ADDRESS'] + '/threads/id'

    def get_threads(self, authorization):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        result = self.rm.get_request(self.url, headers=headers)
        return result

    def create_sample_thread(self, authorization, thread_name=None, private=None):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        data = {
            "name":thread_name,
            "private":private
        }
        result = self.rm.post_request(url=self.url, headers=headers, data=data)
        return result

    def get_thread(self, authorization, thread_id):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        result = self.rm.get_request(url=self.thread_url + '/' + thread_id, headers=headers)
        return result

    def delete_thread(self, authorization, thread_id):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        result = self.rm.delete_request(url=self.thread_url + '/' + thread_id, headers=headers)
        return result

    def invite_user_to_thread(self, authorization, thread_id, user_id):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        data = {
            "users": user_id
        }
        result = self.rm.post_request(url=self.thread_url + '/' + thread_id + '/invite', headers=headers, data=data)
        return result

    def accept_invitation_to_thread(self, authorization, invitation_id, accept=True):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        data = {
            "accept": accept
        }
        result = self.rm.post_request(url=self.url + '/invitations/id/' + invitation_id, headers=headers, data=data)
        return result

    def kick_user_from_thread(self, authorization, thread_id, user_id):
        headers = authorization
        headers['Content-Type'] = 'application/json'
        data = {
            "users": user_id
        }
        result = self.rm.post_request(url=self.thread_url + '/' + thread_id + '/kick', headers=headers, data=data)
        return result