import requests
import json
import base64


class RequestManager(object):

    @staticmethod
    def post_request(url, headers, data):
        r = requests.post(url, data=data, headers=headers)
        resp = {"response": r.json(), "code": r.status_code}
        print(resp["response"])
        return resp

    @staticmethod
    def get_request_with_header(url, headers):
        r = requests.request('GET', url, headers=headers)
        resp = {"response": r.json(), "code": r.status_code}
        print(resp["response"])
        return resp

username = "test1234"
password = "12345"
test = username + ":" + password
test2 = base64.b64encode(test.encode())
test_encoded = test2.decode("ASCII")


headers = {
    'Content-Type': 'application/vnd.api+json'
}

data2 = {
    "username":"test1234",
    "password":"12345",
    "firstname":"mdmd",
    "lastname":"mdmdm"
}

# test = json.dumps(data2)
# response = requests.request("POST", 'http://18.195.251.80:9000/signup', data=json.dumps(data2), headers=headers)
# print(response.text)

RequestManager().post_request('http://18.195.251.80:9000/signup', data=json.dumps(data2), headers=headers)

# url = 'http://18.195.251.80:9000/threads'
#
# data3 = {
#     "name":"testthread",
#     "private":False
# }
#
# test = json.dumps(data3)
#
# RequestManager().post_request('http://18.195.251.80:9000/threads', data=json.dumps(data3), headers=headers)

thread_headers = {'Authorization':'Basic ' + test_encoded}

RequestManager().get_request_with_header('http://18.195.251.80:9000/threads', headers=thread_headers)