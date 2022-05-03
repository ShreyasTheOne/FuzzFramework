from core.base import BaseFuzzer

from api_interface.request_engine import RequestEngine
from core.mutation_fuzzer.data_generators import BoolGenerator
from core.mutation_fuzzer.data_generators.int_generator import IntGenerator
from core.mutation_fuzzer.data_generators.list_generator import ListGenerator
from core.mutation_fuzzer.data_generators.str_generator import StrGenerator


class MutationFuzzer(BaseFuzzer):
    """
    Mutation Fuzzer
    """

    def __init__(self, iterations=None, min_mutations: int = 2, max_mutations: int = 10) -> None:

        super().__init__(iterations)

        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.configuration = {}

        self.initializeConfiguration()

        self.fuzz()

    def fuzz(self) -> None:
        for endpoint_name, endpoint_config in self.configuration.items():
            for _ in range(self.iterations):
                payloadGenerated = self.generatePayload(endpoint_config["payload_configuration"])

                if endpoint_config["request_method"] == "GET":
                    endpoint_config["request_engine"].send_request(params=payloadGenerated)
                elif endpoint_config["request_method"] in ["PUT", "POST", "UPDATE"]:
                    endpoint_config["request_engine"].send_request(json=payloadGenerated)
                elif endpoint_config["request_method"] in ["DELETE", "OPTIONS"]:
                    endpoint_config["request_engine"].send_request()

    def initializeConfiguration(self) -> None:
        """
        Endpoint structure: key: endpoint_name
        {
            request_engine: RequestEngine Instance,
            request_method: Request method
            payload_configuration: Generator Configuration of payload
        }
        Tree node structure for payload:
        {
            generator: GeneratorObject,
            data_type: DataType,
            children: Dict containing children of the node, None if leaf node
        }
        """

        for endpointName, endpointDetails in self._endpoints.items():
            self.configuration[endpointName] = {
                "request_engine": RequestEngine(endpoint_name=endpointName, iterations=self.iterations, fuzzer_type="mutation"),
                "request_method": endpointDetails["method"],
                "payload_configuration": self.__initalizeConfiguration(endpointDetails["payload"]),
            }

    def __initalizeConfiguration(self, payload):
        """
        Utility function to run DFS on the API configuration graph and return required configuration
        """
        config = {
            "data_type": payload["data_type"], 
            "generator": self.__createGeneratorInstance(payload)
        }
        if payload["data_type"] == dict:
            # Call function recursively for all children and create Generator Instances for them
            children = {}
            for key, value in payload["payload"].items():
                children[key] = self.__initalizeConfiguration(value)
            config["children"] = children
        return config

    def __createGeneratorInstance(self, payload):
        if payload is None or payload["data_type"] is None:
            return None
        if payload["data_type"] == bool:
            return BoolGenerator()
        elif payload["data_type"] == int:
            return IntGenerator(
                min_value=payload["seeds"]["min_value"],
                max_value=payload["seeds"]["max_value"],
                fuzz_prob=payload["fuzz_prob"],
            )
        elif payload["data_type"] == str:
            return StrGenerator(
                seeds=payload["seeds"],
                min_mutations=self.min_mutations,
                max_mutations=self.max_mutations,
                fuzz_prob=payload["fuzz_prob"],
            )
        elif payload["data_type"] == list:
            return ListGenerator(
                seeds=payload["payload"]["seeds"],
                data_type=payload["payload"]["data_type"],
                list_fuzz_prob=payload["fuzz_prob"],
                fuzz_prob=payload["payload"]["fuzz_prob"],
            )

        return None

    def generatePayload(self, payload_configuration):
        if payload_configuration is None:
            return None
        payload = None
        if payload_configuration["data_type"] == dict:
            payload = {}
            for key, value in payload_configuration["children"].items():
                payload[key] = self.generatePayload(value)
        else:
            payload = payload_configuration["generator"].generate()
        return payload
