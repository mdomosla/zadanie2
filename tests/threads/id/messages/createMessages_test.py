from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods
from api_endpoints.threads_endpoint import ThreadsMethods
from api_endpoints.message_endpoint import MessageMethods
from lib.data_encoder import Encoder


class CreateMessagesTest(BaseTest):
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

    def test_02_create_too_short_message(self):
        pass

    def test_03_create_too_long_message(self):
        pass

    def test_04_create_message_no_message(self):
        pass

    def test_05_create_message_in_private_thread_as_unathorized_user(self):
        pass
