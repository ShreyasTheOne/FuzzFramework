from api_interface import api_configuration
from api_interface.request_engine import RequestEngine
from core.sample_fuzzer.data_generators import *

class SampleFuzzer:

    def __init__(self):
        self.API_CONFIGURATION = api_configuration.API_CONFIGURATION.structure
        requestEngine = RequestEngine('create_instant_meeting')
        requestEngine.send_request()
        requestEngine.send_request()
        requestEngine.send_request()
        requestEngine.send_request()
