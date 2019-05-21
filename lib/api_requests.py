import requests
import json


class RequestManager(object):

    @staticmethod
    def post_request(url, headers, data):
        """
        Function sends POST request with headers to API
        :param url: url to send request
        :param headers: headers to send
        :param data: data to send
        :return: response from server
        """
        data = json.dumps(data)
        r = requests.post(url, data=data, headers=headers)
        resp = {"response": r.json(), "code": r.status_code}
        return resp

    @staticmethod
    def get_request(url, headers):
        """
        Function sends GET request with headers to API
        :param url: url to send request
        :param headers: headers to include with GET request
        :return: response from server
        """
        r = requests.request('GET', url, headers=headers)
        resp = {"response": r.json(), "code": r.status_code}
        return resp
