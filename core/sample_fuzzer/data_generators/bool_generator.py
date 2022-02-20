import random
from core.sample_fuzzer.data_generators.base import BaseDataGenerator


class BoolGenerator(BaseDataGenerator):
    def generate(self):
        random_bool = bool(random.getrandbits(1))
        return random_bool
