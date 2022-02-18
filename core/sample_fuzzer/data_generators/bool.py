from core.sample_fuzzer.data_generators.base import BaseDataGenerator


class BoolGenerator(BaseDataGenerator):

    def generate(self):
        return True
