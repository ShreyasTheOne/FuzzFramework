from core.base import BaseFuzzer

from api_interface.request_engine import RequestEngine
from core.grammar_fuzzer.data_generators import BaseGenerator


class GrammarFuzzer(BaseFuzzer):
    """
    Grammar Fuzzer
    """

    def __init__(self, iterations=None) -> None:
        super().__init__(iterations)

        self._requestEngines = dict()

        # Generate request engines
        for endpointName, endpointDetails in self._endpoints.items():
            self._requestEngines[endpointName] = RequestEngine(endpoint_name=endpointName, fuzzer_type="grammar")

        for endpointName, endpointDetails in self._endpoints.items():
            self.fuzz(self._requestEngines[endpointName], endpointName)

    def fuzz(self, requestEngine, endpointName) -> None:

        endpointDetails = self._API_CONFIGURATION["endpoints"][endpointName]
        requestMethod = endpointDetails["method"]
        payloadStructure = endpointDetails["payload"]

        self.dataGenerators = dict()

        for _ in range(self.iterations):

            payloadGenerated = self.generatePayload(payloadStructure)
            print(payloadGenerated)            
            
            # if requestMethod == "GET":
            #     requestEngine.send_request(params=payloadGenerated)
            # elif requestMethod in ["PUT", "POST", "UPDATE"]:
            #     requestEngine.send_request(json=payloadGenerated)
            # elif requestMethod in ["DELETE", "OPTIONS"]:
            #     requestEngine.send_request()        


    def generatePayload(self, payloadStructure):

        payload = dict()
        for key, details in payloadStructure["payload"].items():
            if key not in self.dataGenerators:
                self.dataGenerators[key] = BaseGenerator(details["grammar"])
            payload[key] = self.dataGenerators[key].generate()
        
        return payload
