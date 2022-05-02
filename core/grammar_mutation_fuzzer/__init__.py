from core.grammar_fuzzer import GrammarFuzzer

from api_interface.request_engine import RequestEngine
from core.grammar_mutation_fuzzer.data_generators import BaseGrammarMutationGenerator

class GrammarMutationFuzzer(GrammarFuzzer):
    """
    """

    generator_class = BaseGrammarMutationGenerator
