from __future__ import unicode_literals


from requests.auth import HTTPBasicAuth


class BasicCredentials(object):
    """Object to allow authentication with LiquidPlanner via 
    HTTP basic credentials.
    """

    def __init__(self, email, password):
        self.auth = HTTPBasicAuth(email, password)

