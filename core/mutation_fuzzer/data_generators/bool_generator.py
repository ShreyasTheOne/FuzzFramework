import random


class BoolGenerator:
    def generate(cls):
        random_bool = bool(random.getrandbits(1))
        return random_bool
