import base64


class Encoder:

    @staticmethod
    def encode_data(data_to_encode):
        base_data = base64.b64encode(data_to_encode.encode())
        data_encoded = base_data.decode("ASCII")
        return data_encoded