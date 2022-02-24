from random import randint
from core.mutation_fuzzer.data_generators.int_generator import IntGenerator
from core.mutation_fuzzer.data_generators.str_generator import StrGenerator
from core.mutation_fuzzer.data_generators.base import BaseGenerator


class ListGenerator(BaseGenerator):
    def __init__(self, seeds, data_type, list_fuzz_prob, min_length=0, max_length=10, fuzz_prob=1):
        self.seeds = seeds
        self.data_type = data_type
        self.min_length = min_length
        self.max_length = max_length
        self.fuzz_prob = list_fuzz_prob

        if self.data_type == int:
            self.generator = IntGenerator(
                min_value=seeds["min_value"], max_value=seeds["max_value"], fuzz_prob=fuzz_prob
            )

        if self.data_type == str:
            self.generator = StrGenerator(seeds=self.seeds, fuzz_prob=fuzz_prob)

        # data_type = list, dict to be continued...

    def generate(self):
        if self.data_type == str and (not self._should_fuzz()):
            return self.seeds

        random_length = randint(self.min_length, self.max_length)
        mutated_list = [self.generator.generate() for _ in range(random_length)]

        return mutated_list
