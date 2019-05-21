from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods


class SignupTest(BaseTest):
    rand = RandomGenerator()
    rm = RequestManager()

    def setUp(self):
        self.url = self.CONFIG['API_ADDRESS'] + '/signup'
        self.headers = {'Content-Type': 'application/vnd.api+json'}
        self.signup = SignupMethods()

    def test_01_add_new_account(self):
        logging.info('Trying to create new test user')
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(200)
        result[1]['response']['id'] | should.not_be.none
        result[1]['response']['firstname'] | should.be.equal.to(result[0]['firstname'])
        result[1]['response']['lastname'] | should.be.equal.to(result[0]['lastname'])
        result[1]['response']['username'] | should.be.equal.to(result[0]['username'])

    def test_02_add_account_same_login(self):
        pass

    def test_03_add_account_login_too_short(self):
        pass

    def test_04_add_account_too_long_login(self):
        pass

    def test_05_add_account_no_login(self):
        pass

    def test_06_add_account_no_password(self):
        pass

    def test_07_add_account_no_firstname(self):
        pass

    def test_08_add_account_no_lastname(self):
        pass

    def test_09_add_account_pass_too_short(self):
        pass

    def test_10_add_account_pass_too_long(self):
        pass

    def test_11_add_account_firstname_too_short(self):
        pass

    def test_12_add_account_firstname_too_long(self):
        pass

    def test_13_add_account_lastname_too_short(self):
        pass

    def test_14_add_account_lastname_too_long(self):
        pass

    def test_15_add_account_username_not_string(self):
        pass

    def test_16_add_account_pass_not_string(self):
        pass

    def test_17_add_account_firstname_not_string(self):
        pass

    def test_18_add_account_lastname_not_string(self):
        pass



