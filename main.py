class API(object):
    """"""
    def __init__(self, api_key, secret_key):
        """
        :param api_key:
        :param secret_key:
        """
        self.api_key = api_key
        self.secret_key = secret_key

    def generate_sign(self, payload):
        pass

    def do_post(self):
        pass

    def do_get(self):
        pass
