from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods
from api_endpoints.threads_endpoint import ThreadsMethods
from api_endpoints.message_endpoint import MessageMethods
from lib.data_encoder import Encoder


class ViewMessagesTest(BaseTest):
    rand = RandomGenerator()
    rm = RequestManager()
    encoder = Encoder()

    @classmethod
    def setUpClass(cls):
        BaseTest.setUpClass()
        account_data = SignupMethods().create_test_account(generate_fields=True)
        cls.account_id = account_data[1]['response']['id']
        data_to_encode = account_data[0]['username'] + ':' + account_data[0]['password']
        encoded_credentials = cls.encoder.encode_data(data_to_encode)
        cls.thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        sample_thread = cls.rand.generate_random_string(10)
        result = ThreadsMethods().create_sample_thread(authorization=cls.thread_auth_headers, thread_name=sample_thread,
                                                       private=False)
        cls.thread_id = result['response']['id']

    def setUp(self):
        BaseTest.setUp(self)

    def test_01_view_message(self):
        message = self.rand.generate_random_string(50)
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
        logging.info('Getting messages list from thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).view_messages(authorization=self.thread_auth_headers)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['items'][0]['createdAt'] | should.be.a(int)
        result['response']['items'][0]['updatedAt'] | should.be.a(int)
        result['response']['items'][0]['id'] | should.be.a(str)
        result['response']['items'][0]['id'] | should.not_be.none
        result['response']['items'][0]['modelType'] | should.be.equal.to('ThreadMessageModel')
        result['response']['items'][0]['user'] | should.be.a(str)
        result['response']['items'][0]['user'] | should.be.equal.to(self.account_id)
        result['response']['items'][0]['thread'] | should.be.a(str)
        result['response']['items'][0]['thread'] | should.be.equal.to(self.thread_id)
        result['response']['items'][0]['message'] | should.be.a(str)
        result['response']['items'][0]['message'] | should.be.equal.to(message)
        result['response']['items'][0]['deleted'] | should.be.a(bool)
        result['response']['items'][0]['deleted'] | should.be.equal.to(False)

    def test_02_view_last_100_messages(self):
        logging.info('Creating 100 sample messages in thread %s' % self.thread_id)
        for i in range(0, 102):
            message = self.rand.generate_random_string(300)
            MessageMethods(self.thread_id).send_message_in_thread(authorization=self.thread_auth_headers,
                                                                  message=message)
        logging.info('Getting messages list from thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).view_messages(authorization=self.thread_auth_headers)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(200)
        len(result['response']['items']) | should.be.equal.to(100)

    def test_03_view_messages_as_non_invited_user(self):
        account_data = SignupMethods().create_test_account(generate_fields=True)
        data_to_encode = account_data[0]['username'] + ':' + account_data[0]['password']
        encoded_credentials = self.encoder.encode_data(data_to_encode)
        thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        logging.info('Getting messages list from thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).view_messages(authorization=thread_auth_headers)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(403)
        result['response']['message'].lower() | should.contain('is not a member of the thread')

    def test_04_view_messages_as_invited_user(self):
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
        logging.info('Getting messages list from thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).view_messages(authorization=thread_auth_headers)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(403)
        result['response']['message'].lower() | should.contain('is not a member of the thread')
        logging.info('Accepting invitation to a thread %s' % self.thread_id)
        result = ThreadsMethods().accept_invitation_to_thread(authorization=thread_auth_headers,
                                                              invitation_id=invitation_id, accept=True)
        logging.info('Server returned %s' % result)
        logging.info('Getting messages list from thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).view_messages(authorization=thread_auth_headers)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(200)

    def test_05_view_messages_as_kicked_user(self):
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
        logging.info('Getting messages list from thread %s' % self.thread_id)
        result = MessageMethods(self.thread_id).view_messages(authorization=thread_auth_headers)
        logging.info('Server returned %s' % result)
        result['code'] | should.be.equal.to(403)
        result['response']['message'].lower() | should.contain('is not a member of the thread')