from abc import ABC, abstractmethod
from api_interface import api_configuration

class BaseFuzzer(ABC):
    
    @abstractmethod
    def __init__(self, iterations=None):
        """
        Initialise SampleFuzzer instance with the API Configuration

        Args:
            iterations (int): Number of requests to send per endpoint
        """

        self._API_CONFIGURATION = api_configuration.API_CONFIGURATION.structure
        self._endpoints = self._API_CONFIGURATION["endpoints"]
        self.iterations = iterations if iterations else 100
