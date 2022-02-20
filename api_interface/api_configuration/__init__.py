import io
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

    def __init__(self, file_path):  # noqa: C901
        """
        Processes configuration file provided as input
        :param file_path: Path to configuration file
        """

        # Load file contents
        try:
            with io.open(file_path, "r") as stream:
                API_CONFIG = yaml.safe_load(stream)
        except Exception as E:
            print(E)
            return

        # Parse endpoints configuration
        endpoints = API_CONFIG.get("endpoints", None)
        if not endpoints:
            return

        parsed_endpoints = dict()
        for name, endpoint in endpoints.items():
            # Validate request method type
            method = endpoint.get("method", None)
            try:
                parsed_method = HTTPMethod.validate(method)
            except HTTPMethodNotAccepted as E:
                print(E)
                return

            # Validate request payload configuration
            payload = endpoint.get("payload", None)
            try:
                parsed_payload = self.__parse_payload_object(payload)
            except Exception as E:
                print(f"Error in parsing payload for endpoint {name}")
                print(E)
                return

            # Validate response payload configuration
            responses = endpoint.get("responses", None)
            if not responses:
                print("Responses list not provided")
                return

            parsed_responses = dict()
            for status, detail in responses.items():
                # Valid response status
                try:
                    response_status = int(status)
                except Exception as E:
                    print(E)
                    return

                # Validate response data configuration
                data = detail.get("data", None)
                try:
                    response_data = self.__parse_payload_object(data)
                except Exception as E:
                    print("Error in parsing response data")
                    print(E)
                    return

                parsed_responses[response_status] = {
                    **detail,
                    "data": response_data,
                }

            # Update contents in parsed_endpoints
            parsed_endpoints[name] = {
                **endpoint,
                "method": parsed_method,
                "payload": parsed_payload,
                "responses": parsed_responses,
            }

        self.structure = {
            **API_CONFIG,
            "endpoints": parsed_endpoints,
        }

    def __parse_payload_object(self, raw_payload):  # noqa: C901
        """
        Converts raw payload object from configuration file to python data type

        :param payload: Dictionary with keys {data_type, field}
        :return: Same dictionary with field_types converted to python data types
        """

        try:
            pythonic_data_type = DataType.get_data_type(raw_payload["data_type"])
        except DataTypeNotAccepted as E:
            print(str(E))
            raise Exception
        except KeyError as E:
            if raw_payload:
                print(f"Key {E} not found in payload {raw_payload}")
                return
        else:
            exact = raw_payload.get("exact", False)
            try:
                exact = bool(exact)
            except Exception:
                exact = False

            payload = None
            if pythonic_data_type in [str, int, bool, None]:
                if exact:
                    payload = raw_payload["payload"]
            elif pythonic_data_type == dict:
                payload = dict()
                for key, item in raw_payload["payload"].items():
                    payload[key] = self.__parse_payload_object(item)
            elif pythonic_data_type == list:
                payload = self.__parse_payload_object(raw_payload["payload"])

            return {
                "data_type": pythonic_data_type,
                "exact": exact,
                "payload": payload,
            }


def configure(file_path):
    global API_CONFIGURATION
    API_CONFIGURATION = APIConfiguration(file_path)
