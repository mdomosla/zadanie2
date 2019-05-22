from tests.baseTest import *
from lib.random_generator import RandomGenerator
from lib.api_requests import RequestManager
from grappa import should
from api_endpoints.signup_endpoint import SignupMethods
from api_endpoints.threads_endpoint import ThreadsMethods
from lib.data_encoder import Encoder


class ViewMessagesTest(BaseTest):
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
