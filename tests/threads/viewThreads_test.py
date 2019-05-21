from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods
from api_endpoints.threads_endpoint import ThreadsMethods
from lib.data_encoder import Encoder


class ViewThreadsTest(BaseTest):
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
        sample_thread = cls.rand.generate_random_string(10)
        ThreadsMethods().create_sample_thread(authorization=cls.thread_headers, thread_name=sample_thread)

    def setUp(self):
        self.threads_url = self.CONFIG['API_ADDRESS'] + '/threads'
        self.thread_url = self.CONFIG['API_ADDRESS'] + '/threads/id'

    def test_01_get_last_threads(self):
        logging.info('Trying to get last threads')
        result = self.rm.get_request(self.threads_url, headers=self.thread_headers)
        result['code'] | should.be.equal.to(200)
        int(result['response']['itemsFound']) | should.be.higher.than(0)
        int(result['response']['itemsFound']) | should.be.lower.than(101)

    def test_02_get_last_100_threads(self):
        for i in range(0, 101):
            sample_thread = self.rand.generate_random_string(10)
            ThreadsMethods().create_sample_thread(authorization=self.thread_headers, thread_name=sample_thread)
        logging.info('Trying to get last 100 threads')
        result = self.rm.get_request(self.threads_url, headers=self.thread_headers)
        result['code'] | should.be.equal.to(200)
        int(result['response']['itemsFound']) | should.be.equal.to(100)
