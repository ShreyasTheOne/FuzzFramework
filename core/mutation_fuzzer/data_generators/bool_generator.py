from random import getrandbits


class BoolGenerator:
    def generate(cls):
        random_bool = bool(getrandbits(1))
        return random_bool
