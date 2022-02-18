import requests

class RequestEngine:
    """
    This class contains methods used to
    send requests the API using the given   
    """

    def __init__(self, endpoint):
        """
        Initialise request
        """

        self.endpoint = endpoint
    
    def send_request(
        self, 
        data=None, 
        method=None,
        headers=None
    ):
        """
        Send request with values from parameters,
        else take default values from configuration
        """

        pass
