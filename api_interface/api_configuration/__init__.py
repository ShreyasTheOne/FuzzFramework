import io
import sys
import yaml

from api_interface.constants import (
    HTTPMethod,
    DataType,
    DataTypeNotAccepted,
    HTTPMethodNotAccepted,
)


class APIConfiguration:
    """
    Converts API Configuration from YAML to
    Python data object
    """

    def __init__(self, file_path):
        """
        Processes configuration file provided as input
        :param file_path: Path to configuration file
        """

        # Load file contents
        try:
            with io.open(file_path, "r") as stream:
                API_CONFIG = yaml.safe_load(stream)
        except Exception as E:
            sys.exit(E)

        # Parse endpoints configuration
        parsed_endpoints = self.__parse_endpoints_configuration(API_CONFIG.get("endpoints"))

        self.structure = {
            **API_CONFIG,
            "endpoints": parsed_endpoints,
        }

    def __parse_endpoints_configuration(self, endpoints):
        """
        Iterate over all endpoints and validate their
        configurations

        :param endpoints: dict of raw endpoints configuration
        :return: dict of parsed endpoints configuration
        """

        if not endpoints:
            sys.exit("No endpoints to fuzz")

        parsed_endpoints = dict()
        for name, endpoint in endpoints.items():
            # Set current enpoint being parsed
            self.current_parsed_endpoint_name = name

            # Validate request method type
            self.current_parsed_field = "request method"
            raw_method = endpoint.get("method")
            parsed_method = self.__validate_request_method(raw_method)

            # Validate request payload configuration
            self.current_parsed_field = "payload"
            raw_payload = endpoint.get("payload", None)
            parsed_payload = self.__parse_payload_object(raw_payload)

            # Validate response payload configuration
            self.current_parsed_field = "responses"
            raw_responses = endpoint.get("responses", None)
            parsed_responses = self.__parse_responses_configuration(raw_responses)

            # Update contents in parsed_endpoints
            parsed_endpoints[name] = {
                **endpoint,
                "method": parsed_method,
                "payload": parsed_payload,
                "responses": parsed_responses,
            }

        return parsed_endpoints

    def __validate_request_method(self, method):
        """
        Method type must be one of the HTTP Methods
        accepted by our fuzzer
        """

        try:
            parsed_method = HTTPMethod.validate(method, silent=False)
        except HTTPMethodNotAccepted as E:
            self.__exit_with_message(E)
        else:
            return parsed_method

    def __parse_payload_object(self, raw_payload):
        """
        Converts raw payload object from configuration file to pythonic form

        :param payload: Dictionary with keys {data_type, field}
        :return: Same dictionary with field_types converted to python data types
        """

        # Validate data type
        try:
            pythonic_data_type = DataType.get_data_type(raw_payload["data_type"])
        except DataTypeNotAccepted as E:
            self.__exit_with_message(E)
        except KeyError as E:
            self.__exit_with_message(f"Key {E} not found in payload {raw_payload}")
        except Exception as E:
            self.__exit_with_message(E)

        # Validate fuzz probability
        fuzz_prob = raw_payload.get("fuzz_prob", 1)
        try:
            fuzz_prob = float(fuzz_prob)
        except Exception:
            fuzz_prob = 1

        # Generate updated payload
        payload = None
        if pythonic_data_type in [str, int, bool, None]:
            pass
        elif pythonic_data_type == dict:
            payload = dict()
            for key, item in raw_payload["payload"].items():
                payload[key] = self.__parse_payload_object(item)
        elif pythonic_data_type == list:
            payload = self.__parse_payload_object(raw_payload["payload"])

        # If it is a mutation fuzzer, there would be seeds given
        config_seeds = raw_payload.get("seeds", None)
        parsed_seeds = None
        if config_seeds:
            if pythonic_data_type == int:
                min_value = config_seeds.get("min")
                max_value = config_seeds.get("max")
                parsed_seeds = {"min_value": min_value, "max_value": max_value}
            elif pythonic_data_type in [str, list]:
                if not type(config_seeds) == list:
                    self.__exit_with_message("Seeds for data type str must in a list")
                parsed_seeds = config_seeds

        # If it is a grammar fuzzer, a grammar would be given
        config_grammar = raw_payload.get("grammar", None)

        return {
            "data_type": pythonic_data_type,
            "fuzz_prob": fuzz_prob,
            "payload": payload,
            "seeds": parsed_seeds,
            "grammar": config_grammar,
        }

    def __parse_responses_configuration(self, responses):
        """
        Converts raw responses object from strings in configuration file to pythonic form

        :param responses: Dictionary with keys {status: response}
        :return: Same dictionary with appropriate strings converted to python data types
        """

        if not responses:
            self.__exit_with_message("Responses list not provided")

        parsed_responses = dict()
        for status, detail in responses.items():
            # Valid response status
            try:
                response_status = int(status)
            except Exception as E:
                self.__exit_with_message(E)

            # Validate response data configuration
            raw_data = detail.get("data", None)
            response_data = self.__parse_payload_object(raw_data)

            parsed_responses[response_status] = {
                **detail,
                "data": response_data,
            }

        return parsed_responses

    def __exit_with_message(self, message=""):
        """
        Exits program execution with detailed message
        """

        message = str(message)
        sys.exit(
            f"{message}\n^\n"
            "The above error occured while parsing "
            f"{self.current_parsed_field} for "
            f"endpoint '{self.current_parsed_endpoint_name}'."
        )


def configure(file_path):
    global API_CONFIGURATION
    API_CONFIGURATION = APIConfiguration(file_path)
