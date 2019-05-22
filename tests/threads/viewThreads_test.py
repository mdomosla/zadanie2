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
        cls.thread_auth_headers = {'Authorization': 'Basic ' + encoded_credentials}
        sample_thread = cls.rand.generate_random_string(10)
        ThreadsMethods().create_sample_thread(authorization=cls.thread_auth_headers, thread_name=sample_thread,
                                              private=False)

    def setUp(self):
        self.threads_url = self.CONFIG['API_ADDRESS'] + '/threads'

    def test_01_get_last_threads(self):
        logging.info('Trying to get last threads')
        result = ThreadsMethods().get_threads(authorization=self.thread_auth_headers)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(200)
        result['response']['itemsFound'] | should.be.a(int)
        result['response']['limit'] | should.be.a(int)
        result['response']['limit'] | should.be.equal.to(100)
        len(result['response']['items']) | should.be.higher.than(0)
        len(result['response']['items']) | should.be.lower.than(101)
        result['response']['items'][0]['createdAt'] | should.be.a(int)
        result['response']['items'][0]['updatedAt'] | should.be.a(int)
        result['response']['items'][0]['id'] | should.be.a(str)
        result['response']['items'][0]['id'] | should.not_be.none
        result['response']['items'][0]['modelType'] | should.be.equal.to('ThreadModel')
        result['response']['items'][0]['name'] | should.be.a(str)
        result['response']['items'][0]['owner'] | should.be.a(str)
        result['response']['items'][0]['users'] | should.be.a(list)
        result['response']['items'][0]['private'] | should.be.a(bool)
        result['response']['items'][0]['deleted'] | should.be.a(bool)

    def test_02_get_last_100_threads(self):
        logging.info('Generating 100 threads')
        for i in range(0, 101):
            sample_thread = self.rand.generate_random_string(10)
            ThreadsMethods().create_sample_thread(authorization=self.thread_auth_headers, thread_name=sample_thread,
                                                  private=False)
        logging.info('Trying to get last 100 threads')
        result = ThreadsMethods().get_threads(authorization=self.thread_auth_headers)
        logging.info('Server responded with %s' % result)
        result['code'] | should.be.equal.to(200)
        len(result['response']['items']) | should.be.equal.to(100)
