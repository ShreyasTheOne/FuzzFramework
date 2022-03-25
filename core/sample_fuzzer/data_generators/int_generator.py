import random
from core.sample_fuzzer.data_generators.base import BaseDataGenerator


class IntGenerator(BaseDataGenerator):
    @classmethod
    def generate(cls):
        min_number = 0
        max_number = 100
        # random number
        random_number = random.randrange(min_number, max_number)

        return random_number
