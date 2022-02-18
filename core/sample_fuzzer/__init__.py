from api_interface import api_configuration
from core.sample_fuzzer.data_generators import *

class SampleFuzzer:

    def __init__(self):
        self.API_CONFIGURATION = api_configuration.API_CONFIGURATION.structure
    
        print(IntGenerator().generate())
        print(StrGenerator().generate())
        print(BoolGenerator().generate())
        print(ListGenerator().generate())
        print(DictGenerator().generate())
