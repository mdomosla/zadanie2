from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods
from api_endpoints.threads_endpoint import ThreadsMethods
from lib.data_encoder import Encoder
from json.decoder import JSONDecodeError


class CreateThreadsTest(BaseTest):
    rand = RandomGenerator()
    rm = RequestManager()
    encoder = Encoder()

    @classmethod
    def setUpClass(cls):
        BaseTest.setUpClass()
        account_data = SignupMethods().create_test_account(generate_fields=True)[0]
        data_to_encode = account_data['username'] + ':' + account_data['password']
        encoded_credentials = cls.encoder.encode_data(data_to_encode)
        cls.thread_headers = {'Authorization': 'Basic ' + encoded_credentials}

    def setUp(self):
        BaseTest.setUp(self)
        self.threads_url = self.CONFIG['API_ADDRESS'] + '/threads'
        self.thread_id = None

    def test_01_create_public_thread(self):
        sample_thread = self.rand.generate_random_string(34) + self.rand.get_date()
        logging.info('Trying to create new public thread')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=False)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['createdAt'] | should.be.a(int)
        result['response']['updatedAt'] | should.be.a(int)
        result['response']['id'] | should.be.a(str)
        result['response']['id'] | should.not_be.none
        result['response']['modelType'] | should.be.equal.to('ThreadModel')
        result['response']['name'] | should.be.a(str)
        result['response']['owner'] | should.be.a(str)
        result['response']['users'] | should.be.a(list)
        result['response']['private'] | should.be.a(bool)
        result['response']['private'] | should.be.false
        result['response']['deleted'] | should.be.a(bool)
        self.thread_id = result['response']['id']
        logging.info('Trying to get created thread')
        result = ThreadsMethods().get_thread(authorization=self.thread_headers, thread_id=self.thread_id)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['createdAt'] | should.be.a(int)
        result['response']['updatedAt'] | should.be.a(int)
        result['response']['id'] | should.be.a(str)
        result['response']['id'] | should.not_be.none
        result['response']['modelType'] | should.be.equal.to('ThreadModel')
        result['response']['name'] | should.be.a(str)
        result['response']['owner'] | should.be.a(str)
        result['response']['users'] | should.be.a(list)
        result['response']['private'] | should.be.a(bool)
        result['response']['private'] | should.be.false
        result['response']['deleted'] | should.be.a(bool)

    def test_02_create_private_thread(self):
        sample_thread = self.rand.generate_random_string(10)
        logging.info('Trying to create new private thread')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=True)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['createdAt'] | should.be.a(int)
        result['response']['updatedAt'] | should.be.a(int)
        result['response']['id'] | should.be.a(str)
        result['response']['id'] | should.not_be.none
        result['response']['modelType'] | should.be.equal.to('ThreadModel')
        result['response']['name'] | should.be.a(str)
        result['response']['owner'] | should.be.a(str)
        result['response']['users'] | should.be.a(list)
        result['response']['private'] | should.be.a(bool)
        result['response']['private'] | should.be.true
        result['response']['deleted'] | should.be.a(bool)
        self.thread_id = result['response']['id']
        logging.info('Trying to get created thread')
        result = ThreadsMethods().get_thread(authorization=self.thread_headers, thread_id=self.thread_id)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['createdAt'] | should.be.a(int)
        result['response']['updatedAt'] | should.be.a(int)
        result['response']['id'] | should.be.a(str)
        result['response']['id'] | should.not_be.none
        result['response']['modelType'] | should.be.equal.to('ThreadModel')
        result['response']['name'] | should.be.a(str)
        result['response']['owner'] | should.be.a(str)
        result['response']['users'] | should.be.a(list)
        result['response']['private'] | should.be.a(bool)
        result['response']['private'] | should.be.true
        result['response']['deleted'] | should.be.a(bool)

    def test_03_create_thread_name_too_short(self):
        sample_thread = 'a'
        logging.info('Trying to create sample thread')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=False)
        logging.info('Server responded with %s' % result)
        result['code'] = 422
        result['response']['message'].lower() | should.contain('thread name length must be between 2 and 50 characters')

    def test_04_create_thread_name_too_long(self):
        sample_thread = self.rand.get_date() + self.rand.generate_random_string(35)
        logging.info('Trying to create sample thread')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=False)
        logging.info('Server responded with %s' % result)
        result['code'] = 422
        result['response']['message'].lower() | should.contain('thread name length must be between 2 and 50 characters')

    def test_05_create_thread_name_number(self):
        sample_thread = self.rand.get_date()
        logging.info('Trying to create sample thread')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=False)
        logging.info('Server responded with %s' % result)
        result['code'] = 422
        result['response']['message'].lower() | should.contain('thread name must not be a number')

    def test_06_create_second_thread_with_same_name(self):
        sample_thread = self.rand.get_date() + self.rand.generate_random_string(10)
        logging.info('Trying to create sample thread')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=False)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(200)
        self.thread_id = result['response']['id']
        logging.info('Trying to create thread with the same name')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=False)
        logging.info('Server responded with %s' % result)
        result['code'] = 409
        result['response']['message'].lower() | should.contain('thread name already taken')

    def test_07_create_thread_no_name(self):
        logging.info('Trying to create thread with no name')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, private=False)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(409)
        result['response']['message'].lower() | should.contain('thread name required')

    def test_08_create_thread_no_private(self):
        sample_thread = self.rand.get_date() + self.rand.generate_random_string(10)
        logging.info('Trying to create thread with no private setting')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(409)
        result['response']['message'].lower() | should.contain('private required')

    def test_09_create_thread_private_not_bool(self):
        sample_thread = self.rand.get_date() + self.rand.generate_random_string(10)
        private = int(self.rand.get_date())
        logging.info('Trying to create thread with private setting as int')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=private)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(422)
        result['response']['message'].lower() | should.contain('private should be bool')

        private = self.rand.generate_random_string(10)
        logging.info('Trying to create thread with private setting as string')
        result = ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread,
                                                       private=private)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(422)
        result['response']['message'].lower() | should.contain('private should be bool')

    def test_10_create_thread_by_non_existing_user(self):
        sample_thread = self.rand.get_date() + self.rand.generate_random_string(10)
        logging.info('Trying to create thread with private setting as int')
        thread_headers = {'Authorization': 'Basic ' + self.rand.generate_random_string(10)}
        try:
            result = ThreadsMethods().create_sample_thread(authorization=thread_headers, thread_name=sample_thread)
            result | should.be.none
        except JSONDecodeError as e:
            logging.info('Server responded with %s' % e.doc)
            e.doc.lower() | should.contain('unauthorized access')

    def tearDown(self):
        if self.thread_id is not None:
            logging.info('Cleaning up, deleting sample thread')
            ThreadsMethods().delete_thread(authorization=self.thread_headers, thread_id=self.thread_id)
        BaseTest.tearDown(self)
