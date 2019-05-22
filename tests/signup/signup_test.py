from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods


class SignupTest(BaseTest):
    rand = RandomGenerator()
    rm = RequestManager()

    def setUp(self):
        BaseTest.setUp(self)
        self.url = self.CONFIG['API_ADDRESS'] + '/signup'
        self.headers = {'Content-Type': 'application/vnd.api+json'}
        self.signup = SignupMethods()

    def test_01_add_new_account_min_allowable_chars(self):
        password = self.rand.generate_random_string(4)
        first_name = self.rand.generate_random_string(2)
        last_name = self.rand.generate_random_string(2)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(200)
        result[1]['response']['id'] | should.not_be.none
        result[1]['response']['id'] | should.be.a(str)
        result[1]['response']['firstname'] | should.be.equal.to(result[0]['firstname'])
        result[1]['response']['lastname'] | should.be.equal.to(result[0]['lastname'])
        result[1]['response']['username'] | should.be.equal.to(result[0]['username'])
        result[1]['response']['createdAt'] | should.not_be.none
        result[1]['response']['createdAt'] | should.be.a(int)
        result[1]['response']['updatedAt'] | should.not_be.none
        result[1]['response']['updatedAt'] | should.be.a(int)
        result[1]['response']['modelType'] | should.be.equal.to('UserModel')

    def test_02_add_new_account_max_allowable_chars(self):
        password = self.rand.generate_random_string(20)
        first_name = self.rand.generate_random_string(20)
        last_name = self.rand.generate_random_string(50)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(200)
        result[1]['response']['id'] | should.not_be.none
        result[1]['response']['id'] | should.be.a(str)
        result[1]['response']['firstname'] | should.be.equal.to(result[0]['firstname'])
        result[1]['response']['lastname'] | should.be.equal.to(result[0]['lastname'])
        result[1]['response']['username'] | should.be.equal.to(result[0]['username'])
        result[1]['response']['createdAt'] | should.not_be.none
        result[1]['response']['createdAt'] | should.be.a(int)
        result[1]['response']['updatedAt'] | should.not_be.none
        result[1]['response']['updatedAt'] | should.be.a(int)
        result[1]['response']['modelType'] | should.be.equal.to('UserModel')

    def test_03_add_account_same_login(self):
        username = 'test' + self.rand.get_date()
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user with login %s' % username)
        result = self.signup.create_test_account(unique_username=False, user_name=username, password=password,
                                                 firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        logging.info('Trying to create same test user with login %s' % username)
        result = self.signup.create_test_account(unique_username=False, user_name=username, password=password,
                                                 firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(409)
        result[1]['response']['message'].lower() | should.contain('username already taken')

    def test_04_add_account_login_too_short(self):
        username = 'a'
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user with login %s' % username)
        result = self.signup.create_test_account(unique_username=False, user_name=username, password=password,
                                                 firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('username length must be between 2 and 20 characters')

    def test_05_add_account_too_long_login(self):
        username = 'toolo' + self.rand.get_date()
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user with login %s' % username)
        result = self.signup.create_test_account(unique_username=False, user_name=username, password=password,
                                                 firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('username length must be between 2 and 20 characters')

    def test_06_add_account_no_login(self):
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user with empty login %s')
        result = self.signup.create_test_account(unique_username=False, password=password,
                                                 firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(409)
        result[1]['response']['message'].lower() | should.contain('username required')

    def test_07_add_account_no_password(self):
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user with no password')
        result = self.signup.create_test_account(unique_username=True, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(409)
        result[1]['response']['message'].lower() | should.contain('password required')

    def test_08_add_account_no_firstname(self):
        password = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user with no password')
        result = self.signup.create_test_account(unique_username=True, password=password, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(409)
        result[1]['response']['message'].lower() | should.contain('firstname required')

    def test_09_add_account_no_lastname(self):
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user with no password')
        result = self.signup.create_test_account(unique_username=True, password=password, firstname=first_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(409)
        result[1]['response']['message'].lower() | should.contain('firstname required')

    def test_10_add_account_pass_too_short(self):
        password = self.rand.generate_random_string(3)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('password length must be between 4 and 20 characters')

    def test_11_add_account_pass_too_long(self):
        password = self.rand.generate_random_string(21)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('password length must be between 4 and 20 characters')

    def test_12_add_account_firstname_too_short(self):
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(1)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('first name length must be between 2 and 20 '
                                                                  'characters')

    def test_13_add_account_firstname_too_long(self):
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(21)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('first name length must be between 2 and 20 '
                                                                  'characters')

    def test_14_add_account_lastname_too_short(self):
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(1)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('last name length must be between 2 and 50 '
                                                                  'characters')

    def test_15_add_account_lastname_too_long(self):
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(51)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('last name length must be between 2 and 50 '
                                                                  'characters')

    def test_16_add_account_username_not_string(self):
        username = self.rand.get_date()
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(unique_username=False, user_name=username, password=password,
                                                 firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['code'] | should.be.equal.to(422)
        result[1]['response']['message'].lower() | should.contain('username must not be a number')

    def test_17_add_second_account_check_user_id(self):
        password = self.rand.generate_random_string(5)
        first_name = self.rand.generate_random_string(5)
        last_name = self.rand.generate_random_string(5)
        logging.info('Trying to create new test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        user_id = result[1]['response']['id']
        logging.info('Trying to create another test user')
        result = self.signup.create_test_account(password=password, firstname=first_name, lastname=last_name)
        logging.info('Server responded with %s' % result[1])
        result[1]['response']['id'] | should.not_be.equal.to(user_id)


