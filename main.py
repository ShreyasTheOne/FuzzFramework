import sys
from getopt import getopt, GetoptError

from api_interface.api_configuration import configure as configure_api
from core.pentest_fuzzer import PentestFuzzer

from core.sample_fuzzer import SampleFuzzer
from core.mutation_fuzzer import MutationFuzzer
from core.grammar_fuzzer import GrammarFuzzer
from core.grammar_mutation_fuzzer import GrammarMutationFuzzer

HELP_TEXT = "\n\nInstructions to use:\npython3 fuzz.py -c path/to/api-config.yml\n\n"


def run_fuzzer(fuzzer_type: str, iterations: int, workers: int = None):
    fuzzer = None
    if fuzzer_type == "sample":
        fuzzer = SampleFuzzer(iterations=iterations)
    elif fuzzer_type == "mutation":
        fuzzer = MutationFuzzer(iterations=iterations)
    elif fuzzer_type == "grammar":
        fuzzer = GrammarFuzzer(iterations=iterations)
    elif fuzzer_type == "grammar_mutation":
        fuzzer = GrammarMutationFuzzer(iterations=iterations)
    elif fuzzer_type == "pentest":
        fuzzer = PentestFuzzer(iterations=iterations, workers=workers)
    else:
        sys.exit(f"Invalid fuzzer type {fuzzer_type}")
    fuzzer.fuzz_all()


def main(argv):
    """
    Driver code to run the fuzzer

    :param argv: list of command-line arguments given
    """

    # Extract list of command line arguments
    short_options = "hc:f:i:w:"
    long_options = ["help", "api-config", "fuzzer-type", "iterations", "workers"]

    try:
        opts, args = getopt(argv, short_options, long_options)
    except GetoptError:
        print(HELP_TEXT)
        sys.exit(2)

    # Extract individual command line arguments from list
    fuzzer_type = None
    iterations = None
    api_config_file_path = None
    workers = None
    for opt, arg in opts:
        if opt in ["-c", "--api-config"]:
            api_config_file_path = arg
        elif opt in ["-f", "--fuzzer-type"]:
            fuzzer_type = arg
        elif opt in ["-i", "--iterations"]:
            iterations = int(arg)
        elif opt in ["-w", "--workers"]:
            workers = int(arg)
        else:
            print(HELP_TEXT)
            sys.exit(2)

    if not api_config_file_path:
        print(HELP_TEXT)
        sys.exit(2)

    # Generate API Configuration
    configure_api(api_config_file_path)

    # Start fuzzing
    run_fuzzer(fuzzer_type=fuzzer_type, iterations=iterations, workers=workers)


if __name__ == "__main__":
    main(sys.argv[1:])
