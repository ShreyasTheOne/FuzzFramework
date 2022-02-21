import string
import random
from core.sample_fuzzer.data_generators.base import BaseDataGenerator
from core.sample_fuzzer.data_generators.int_generator import IntGenerator


class StrGenerator(BaseDataGenerator):
    def generate(self):
        # random length
        # min_number = 0
        # max_number = 100
        
        random_string_length = IntGenerator().generate()

        # string of random uppercase & lowercase alphabets
        random_string = "".join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase)
            for x in range(random_string_length)
        )

        # covert the string to list & shuffle the list
        random_list = list(random_string)
        random.shuffle(random_list)

        # final random string
        random_string = "".join(random_list)

        return random_string
