import string
import random
from datetime import datetime


class RandomGenerator:

    @staticmethod
    def generate_random_string(length):
        """
        Function generates random string with specified length
        :param length: length of string to generate
        :return: generated string
        """
        generated_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return generated_string

    @staticmethod
    def get_date():
        """
        Function generates date string including miliseconds so that generated string is unique
        :return: generated date
        """
        current_date = datetime.now()
        data_formatted = str(current_date.strftime('%m%d%H%M%S%f'))
        return data_formatted
