from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from lib.configuration_reader import ConfigReader


class SignupMethods:
    rand = RandomGenerator()
    rm = RequestManager()
    CONFIG = ConfigReader().load_configuration_from_file('configuration.json')
    url = CONFIG['API_ADDRESS'] + '/signup'
    headers = {'Content-Type': 'application/vnd.api+json'}

    def create_test_account(self, unique_username=True, generate_fields=False, user_name=None, password=None,
                            firstname=None, lastname=None):
        if unique_username:
            username = 'test' + self.rand.get_date()
        else:
            username = user_name
        if generate_fields:
            password = self.rand.generate_random_string(10)
            firstname = self.rand.generate_random_string(10)
            lastname = self.rand.generate_random_string(10)
        data = {
            "username": username,
            "password": password,
            "firstname": firstname,
            "lastname": lastname
        }
        result = self.rm.post_request(url=self.url, data=data, headers=self.headers)
        return data, result
