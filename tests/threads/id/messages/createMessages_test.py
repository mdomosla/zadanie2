from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods
from api_endpoints.threads_endpoint import ThreadsMethods
from api_endpoints.message_endpoint import MessageMethods
from lib.data_encoder import Encoder
from json.decoder import JSONDecodeError


class CreateMessagesTest(BaseTest):
    rand = RandomGenerator()
    rm = RequestManager()
    encoder = Encoder()
    auth_header = None
    thread_to_delete = None

    @classmethod
    def setUpClass(cls):
        BaseTest.setUpClass()
        account_data = SignupMethods().create_test_account(generate_fields=True)
        cls.account_id = account_data[1]['response']['id']
        data_to_encode = account_data[0]['username'] + ':' + account_data[0]['password']
        encoded_credentials = cls.encoder.encode_data(data_to_encode)
        cls.thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        sample_thread = cls.rand.generate_random_string(10)
        logging.info('Creating user and sample thread for tests')
        result = ThreadsMethods().create_sample_thread(authorization=cls.thread_auth_headers, thread_name=sample_thread,
                                                       private=False)
        cls.thread_id = result['response']['id']
        cls.thread_to_delete = cls.thread_id
        cls.auth_header = cls.thread_auth_headers

    def setUp(self):
        BaseTest.setUp(self)

    def test_01_create_max_long_message(self):
        message = self.rand.generate_random_string(300)
        logging.info('Creating sample message in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=self.thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['createdAt'] | should.be.a(int)
        result['response']['updatedAt'] | should.be.a(int)
        result['response']['id'] | should.be.a(str)
        result['response']['id'] | should.not_be.none
        result['response']['modelType'] | should.be.equal.to('ThreadMessageModel')
        result['response']['user'] | should.be.a(str)
        result['response']['user'] | should.be.equal.to(self.account_id)
        result['response']['thread'] | should.be.a(str)
        result['response']['thread'] | should.be.equal.to(self.thread_id)
        result['response']['message'] | should.be.a(str)
        result['response']['message'] | should.be.equal.to(message)
        result['response']['deleted'] | should.be.a(bool)
        result['response']['deleted'] | should.be.equal.to(False)

    def test_02_create_min_long_message(self):
        message = self.rand.generate_random_string(1)
        logging.info('Creating sample message in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=self.thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['createdAt'] | should.be.a(int)
        result['response']['updatedAt'] | should.be.a(int)
        result['response']['id'] | should.be.a(str)
        result['response']['id'] | should.not_be.none
        result['response']['modelType'] | should.be.equal.to('ThreadMessageModel')
        result['response']['user'] | should.be.a(str)
        result['response']['user'] | should.be.equal.to(self.account_id)
        result['response']['thread'] | should.be.a(str)
        result['response']['thread'] | should.be.equal.to(self.thread_id)
        result['response']['message'] | should.be.a(str)
        result['response']['message'] | should.be.equal.to(message)
        result['response']['deleted'] | should.be.a(bool)
        result['response']['deleted'] | should.be.equal.to(False)

    def test_03_create_too_short_message(self):
        message = ''
        logging.info('Creating sample message in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=self.thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] = 422
        result['response']['message'].lower() | should.contain('text has to be between 1 and 300 characters')

    def test_04_create_too_long_message(self):
        message = self.rand.generate_random_string(301)
        logging.info('Creating sample message in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=self.thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] = 422
        result['response']['message'].lower() | should.contain('text has to be between 1 and 300 characters')

    def test_05_create_message_no_message(self):
        logging.info('Creating sample message without message in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=self.thread_auth_headers)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(409)
        result['response']['message'].lower() | should.contain('text required')

    def test_06_create_message_in_public_thread_as_another_not_invited_user(self):
        account_data = SignupMethods().create_test_account(generate_fields=True)
        data_to_encode = account_data[0]['username'] + ':' + account_data[0]['password']
        encoded_credentials = self.encoder.encode_data(data_to_encode)
        thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        message = self.rand.generate_random_string(50)
        logging.info('Creating sample message as another user in public thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(403)
        result['response']['message'].lower() | should.contain('is not a member of the thread')

    def test_07_create_message_in_private_thread_as_another_not_invited_user(self):
        sample_thread = self.rand.generate_random_string(10)
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_auth_headers,
                                                       thread_name=sample_thread,
                                                       private=True)
        self.thread_id = result['response']['id']
        account_data = SignupMethods().create_test_account(generate_fields=True)
        data_to_encode = account_data[0]['username'] + ':' + account_data[0]['password']
        encoded_credentials = self.encoder.encode_data(data_to_encode)
        thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        message = self.rand.generate_random_string(50)
        logging.info('Creating sample message as another user in private thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(403)
        result['response']['message'].lower() | should.contain('is not a member of the thread')

    def test_08_create_message_by_non_existing_user(self):
        logging.info('Creating sample message by non existing user in public thread %s' % self.thread_id)
        thread_auth_headers = {'Authorization': 'Basic ' + self.rand.generate_random_string(10)}
        message = self.rand.generate_random_string(50)
        try:
            result = MessageMethods(self.thread_id).send_message_in_thread(authorization=thread_auth_headers,
                                                                           message=message)
            result | should.be.none
        except JSONDecodeError as e:
            logging.info('Server responded with %s' % e.doc)
            e.doc.lower() | should.contain('unauthorized access')

    def test_09_create_message_by_invited_user(self):
        account_data = SignupMethods().create_test_account(generate_fields=True)
        account_id = account_data[1]['response']['id']
        data_to_encode = account_data[0]['username'] + ':' + account_data[0]['password']
        encoded_credentials = self.encoder.encode_data(data_to_encode)
        thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        logging.info('Inviting user to thread %s' % self.thread_id)
        result = ThreadsMethods().invite_user_to_thread(authorization=self.thread_auth_headers,
                                                        thread_id=self.thread_id,
                                                        user_id=account_id)
        logging.info('Server returned %s' % result)
        invitation_id = result['response'][0]['id']
        message = self.rand.generate_random_string(50)
        logging.info('Creating sample message as invited user in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(403)
        result['response']['message'].lower() | should.contain('is not a member of the thread')
        logging.info('Accepting invitation to a thread %s' % self.thread_id)
        result = ThreadsMethods().accept_invitation_to_thread(authorization=thread_auth_headers,
                                                              invitation_id=invitation_id, accept=True)
        logging.info('Server returned %s' % result)
        logging.info('Creating sample message as invited and accepted user in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(200)

    def test_10_create_message_by_kicked_user(self):
        account_data = SignupMethods().create_test_account(generate_fields=True)
        account_id = account_data[1]['response']['id']
        data_to_encode = account_data[0]['username'] + ':' + account_data[0]['password']
        encoded_credentials = self.encoder.encode_data(data_to_encode)
        thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        logging.info('Inviting user to thread %s' % self.thread_id)
        result = ThreadsMethods().invite_user_to_thread(authorization=self.thread_auth_headers,
                                                        thread_id=self.thread_id,
                                                        user_id=account_id)
        logging.info('Server returned %s' % result)
        invitation_id = result['response'][0]['id']

        logging.info('Accepting invitation to a thread %s' % self.thread_id)
        result = ThreadsMethods().accept_invitation_to_thread(authorization=thread_auth_headers,
                                                              invitation_id=invitation_id, accept=True)
        logging.info('Server returned %s' % result)
        logging.info('Kicking user from a thread %s' % self.thread_id)
        result = ThreadsMethods().kick_user_from_thread(authorization=self.thread_auth_headers,
                                                        thread_id=self.thread_id, user_id=account_id)
        logging.info('Server returned %s' % result)
        message = self.rand.generate_random_string(50)
        logging.info('Creating sample message as kicked user in thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).send_message_in_thread(authorization=thread_auth_headers,
                                                                       message=message)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(403)
        result['response']['message'].lower() | should.contain('is not a member of the thread')

    @classmethod
    def tearDownClass(cls):
        if cls.auth_header is not None and cls.thread_to_delete is not None:
            logging.info('Deleting sample thread created for tests')
            ThreadsMethods().delete_thread(authorization=cls.auth_header, thread_id=cls.thread_to_delete)