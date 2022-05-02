import re
import sys
import textwrap
from os import path, mkdir
from requests import request
from requests.exceptions import JSONDecodeError

from api_interface import api_configuration


class RequestEngine:
    """
    This class contains methods used to
    send requests the API using the given
    """

    def __init__(self, endpoint_name, iterations, fuzzer_type=""):
        """
        Initialise request
        """

        # Endpoint name for logs
        self.endpoint_name = endpoint_name

        # Fuzzer type for log file name
        self.fuzzer_type = fuzzer_type

        self.total_iterations = iterations
        self.run_iterations = 0

        # Extract configuration for endpoint to store in class variables
        api_structure = api_configuration.API_CONFIGURATION.structure
        self.api_structure = api_structure
        self.endpoint_configuration = api_structure["endpoints"][endpoint_name]

        # Where to send request?
        base_url = api_structure["base_url"]
        path = self.endpoint_configuration["path"]
        self.request_URL = f"{base_url}{path}"

        # To name the 500 error log files
        self._500_count = 0
        self.response_status_counts = {}
        self.response_messages = {}

    def send_authenticated_request(
        self, user_idx, headers={}, params={}, data={}, json={}, cookies={}, log_details=True
    ) -> None:
        """Send an authenticated request using the credentials of user with index user_idx"""
        user = self.api_structure["users"][user_idx]
        headers = {
            **headers,
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            "X-CSRFToken": user["csrftoken"],
        }
        cookies[self.api_structure["sessionidname"]] = user["sessionid"]
        cookies[self.api_structure["csrftokenname"]] = user["csrftoken"]
        return self.send_request(
            headers=headers, params=params, data=data, json=json, log_details=log_details, cookies=cookies
        )

    def send_request(self, headers=None, params={}, data={}, json={}, log_details=True, cookies={}):
        """
        Send request with values from parameters,
        else take default values from configuration
        """

        if headers is None:
            headers = self.endpoint_configuration["request_headers"]

        method = self.endpoint_configuration["method"]

        response = request(
            method=method, url=self.request_URL, headers=headers, params=params, data=data, json=json, cookies=cookies
        )

        response_status = response.status_code
        if response_status in self.response_status_counts:
            self.response_status_counts[response_status] += 1
        else:
            self.response_status_counts[response_status] = 1
        
        _500 = False
        try:
            response_json = response.json()
            response_message = str(response_json)
        except JSONDecodeError:
            response_html = response.text
            response_json = f"playground/logs/{str(self.fuzzer_type)}_{str(self.endpoint_name)}_500/{self._500_count}.html"
            response_message = self.extract_message_from_json(response_html)
            _500 = True
        response_headers = response.headers

        if (response_status / 100) in [4, 5]:
            if response_message in self.response_messages:
                self.response_messages[response_message] += 1
            else:
                self.response_messages[response_message] = 1

        if log_details:
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

            if _500:
                self.__log_500(response_html=response_html)

        return {
            "status": response_status,
            "headers": response_headers,
            "data": response_json,
            "cookies": response.cookies,
        }

    def extract_message_from_json(self, response_html):

        pre, post = response_html.split('<pre class="exception_value">')
        message = post.split("</pre>")[0]
        heading = pre.split("<title>")[1].split("</title>")[0]
        heading = re.sub("\s+", " ", heading.replace("\n", ""))

        return f"{heading}: {message}"


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

        FILE_NAME = f"{str(self.fuzzer_type)}_{str(self.endpoint_name)}.log"
        FILE_PATH = path.join(FOLDER_PATH, FILE_NAME)

        log_file = None
        if path.exists(FILE_PATH):
            if path.isfile(FILE_PATH):
                log_file = open(FILE_PATH, "a")
            else:
                sys.exit(f"Unrecognised file type for logs of endpoint " f"{self.endpoint_name} at {FOLDER_PATH}!")
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

        self.run_iterations += 1

        if self.run_iterations == self.total_iterations:
            newline = "\n"
            status_count_heading = f"""
            ---------------------------
            Response Status Code Counts
            ---------------------------
            """
            log_file.write(textwrap.dedent(status_count_heading))

            for code, count in self.response_status_counts.items():
                status_count_string = f"""
                {code}: {count}"""
                log_file.write(textwrap.dedent(status_count_string))
            
            response_message_heading = f"""
            

            -----------------------
            Error Message Counts
            -----------------------            
            """
            log_file.write(textwrap.dedent(response_message_heading))

            for message, count in self.response_messages.items():
                response_message_string = f"""
                {message}: {count}"""
                log_file.write(textwrap.dedent(response_message_string))


        log_file.close()

    def __log_500(self, response_html):
        """ """

        FOLDER_PATH = f"playground/logs/{str(self.fuzzer_type)}_{str(self.endpoint_name)}_500"
        if not (path.exists(FOLDER_PATH) and path.isdir(FOLDER_PATH)):
            mkdir(FOLDER_PATH)
        FILE_NAME = f"{self._500_count}.html"
        FILE_PATH = path.join(FOLDER_PATH, FILE_NAME)

        log_file = None
        if path.exists(FILE_PATH):
            if path.isfile(FILE_PATH):
                log_file = open(FILE_PATH, "w")
            else:
                sys.exit(f"Unrecognised file type for logs of endpoint " f"{self.endpoint_name} at {FOLDER_PATH}!")
        else:
            log_file = open(FILE_PATH, "w")

        log_file.write(textwrap.dedent(response_html))
        log_file.close()

        self._500_count += 1
