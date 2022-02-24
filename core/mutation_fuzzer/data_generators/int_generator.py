from random import randint
from core.mutation_fuzzer.data_generators.base import BaseGenerator

class IntGenerator(BaseGenerator):

    def __init__(self, min_value=-1e9, max_value=1e9, fuzz_prob=1):

        self.min_value = min_value
        self.max_value = max_value
        self.fuzz_prob = fuzz_prob
    
    def generate(self):

        if self._should_fuzz():
            return randint(-1e9, 1e9)
        else:
            return randint(self.min_value, self.max_value)
