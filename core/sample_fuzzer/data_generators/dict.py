from core.sample_fuzzer.data_generators.base import BaseDataGenerator


class DictGenerator(BaseDataGenerator):

    def generate(self):
        return {}
