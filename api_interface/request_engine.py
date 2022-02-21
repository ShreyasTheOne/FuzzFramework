import sys
import textwrap
from os import path
from requests import request
from requests.exceptions import JSONDecodeError

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

        # Endpoint name for logs
        self.endpoint_name = endpoint_name

        # Extract configuration for endpoint to store in class variables
        api_structure = api_configuration.API_CONFIGURATION.structure
        self.endpoint_configuration = api_structure["endpoints"][endpoint_name]

        # Where to send request?
        base_url = api_structure["base_url"]
        path = self.endpoint_configuration["path"]
        self.request_URL = f"{base_url}{path}"

    def send_request(
        self,
        headers=None,
        params={},
        data={},
        json={},
        # cookies=None
    ):
        """
        Send request with values from parameters,
        else take default values from configuration
        """

        if headers is None:
            headers = self.endpoint_configuration["request_headers"]

        method = self.endpoint_configuration["method"]

        response = request(
            method=method,
            url=self.request_URL,
            headers=headers,
            params=params,
            data=data,
            json=json,
            # cookies=None
        )

        response_status = response.status_code
        try:
            response_json = response.json()
        except JSONDecodeError:
            response_json = "Response not in json format"
        response_headers = response.headers

        self.__log_details(
            request={
                "headers": headers,
                "params": params,
                "data": data,
                "json": json,
            },
            response={
                "status": response_status,
                "data": response_json,
                "headers": response_headers,
            },
        )

    def __log_details(self, request, response):
        """
        Write results of request and response
        to a file. If file does not exist, create one
        """

        # Temporarily use custom directory path
        # to store the files, take file path from
        # user later.

        FOLDER_PATH = "playground/logs"
        if not (path.exists(FOLDER_PATH) and path.isdir(FOLDER_PATH)):
            sys.exit(f"Directory not found at path {FOLDER_PATH}!")

        FILE_NAME = f"{str(self.endpoint_name)}.log"
        FILE_PATH = path.join(FOLDER_PATH, FILE_NAME)

        log_file = None
        if path.exists(FILE_PATH):
            if path.isfile(FILE_PATH):
                log_file = open(FILE_PATH, "a")
            else:
                sys.exit(
                    f"Unrecognised file type for logs of endpoint " 
                    f"{self.endpoint_name} at {FOLDER_PATH}!"
                )
        else:
            log_file = open(FILE_PATH, "w")

        # In case some field is empty
        _N_O_N_E_ = "_"

        # Write results to log file
        log_string = f"""
        ---------------
        Request Details
        ---------------
        Headers: {str(request['headers']) if request['headers'] else _N_O_N_E_}
        Parameters: {str(request['params']) if request['params'] else _N_O_N_E_}
        Data: {str(request['data']) if request['data'] else _N_O_N_E_}
        JSON: {str(request['json']) if request['json'] else _N_O_N_E_}
        ----------------
        Response Details
        ----------------
        Status: {str(response['status']) if response['status'] else _N_O_N_E_}
        Headers: {str(response['headers']) if response['headers'] else _N_O_N_E_}
        Data: {str(response['data']) if response['data'] else _N_O_N_E_}
        \n\n
        """

        log_file.write(textwrap.dedent(log_string))
        log_file.close()
