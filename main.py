import sys
from getopt import getopt, GetoptError

from api_interface.api_configuration import configure as configure_api

from core.sample_fuzzer import SampleFuzzer

HELP_TEXT = "\n\nInstructions to use:\npython3 fuzz.py -c path/to/api-config.yml\n\n"

def run_fuzzer(fuzzer_type: str, iterations: int):

    if fuzzer_type == "sample":
        SampleFuzzer(iterations)
    else:
        sys.exit(f"Invalid fuzzer type {fuzzer_type}")

def main(argv):
    """
    Driver code to run the fuzzer

    :param argv: list of command-line arguments given
    """

    # Extract list of command line arguments
    short_options = "hc:f:i:"
    long_options = [
        "help",
        "api-config",
        "fuzzer-type",
        "iterations"
    ]

    try:
        opts, args = getopt(argv, short_options, long_options)
    except GetoptError:
        print(HELP_TEXT)
        sys.exit(2)

    # Extract individual command line arguments from list
    fuzzer_type = None
    iterations = None
    api_config_file_path = None
    for opt, arg in opts:
        if opt in ["-c", "--api-config"]:
            api_config_file_path = arg
        elif opt in ["-f", "--fuzzer-type"]:
            fuzzer_type = arg
        elif opt in ["-i", "--iterations"]:
            iterations = arg
        else:
            print(HELP_TEXT)
            sys.exit(2)

    if not api_config_file_path:
        print(HELP_TEXT)
        sys.exit(2)

    # Generate API Configuration
    configure_api(api_config_file_path)

    # Start fuzzing
    run_fuzzer(fuzzer_type, iterations)


if __name__ == "__main__":
    main(sys.argv[1:])
