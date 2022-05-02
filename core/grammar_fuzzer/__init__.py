from core.base import BaseFuzzer

from api_interface.request_engine import RequestEngine
from core.grammar_fuzzer.data_generators import BaseGrammarGenerator


class GrammarFuzzer(BaseFuzzer):
    """
    Grammar Fuzzer
    """

    generator_class = BaseGrammarGenerator

    def __init__(self, iterations=None) -> None:
        super().__init__(iterations)

        self._requestEngines = dict()

        # Generate request engines
        for endpointName in self._endpoints.keys():
            self._requestEngines[endpointName] = RequestEngine(endpoint_name=endpointName, fuzzer_type="grammar")
            self.fuzz(self._requestEngines[endpointName], endpointName)

    def fuzz(self, requestEngine, endpointName) -> None:

        endpointDetails = self._API_CONFIGURATION["endpoints"][endpointName]
        requestMethod = endpointDetails["method"]
        payloadStructure = endpointDetails["payload"]

        self.dataGenerators = dict()

        for _ in range(self.iterations):

            payloadGenerated = self.generatePayload(payloadStructure)      
            
            if requestMethod == "GET":
                requestEngine.send_request(params=payloadGenerated)
            elif requestMethod in ["PUT", "POST", "UPDATE"]:
                requestEngine.send_request(json=payloadGenerated)
            elif requestMethod in ["DELETE", "OPTIONS"]:
                requestEngine.send_request()        


    def generatePayload(self, payloadStructure):

        payload = dict()
        for key, details in payloadStructure["payload"].items():
            if key not in self.dataGenerators:
                self.dataGenerators[key] = self.generator_class(
                    details["grammar"],
                    details["data_type"]
                )

            payload[key] = self.dataGenerators[key].generate()
        
        return payload
