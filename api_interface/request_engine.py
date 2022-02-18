import requests
from api_interface import api_configuration

class RequestEngine:
    """
    This class contains methods used to
    send requests the API using the given   
    """

    def __init__(self, endpoint_name):
        """
        Initialise request
        """

        self.API_CONFIGURATION = api_configuration.API_CONFIGURATION.structure
        self.endpoint_name = endpoint_name
    
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
