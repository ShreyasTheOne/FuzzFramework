
from random import randint


class ListGrammarGenerator:
    def __init__(
        self, 
        grammar, 
        data_type, 
        generator_class,
        min_length=0,
        max_length=10
    ):
        self.grammar = grammar
        self.data_type = data_type
        self.min_length = min_length
        self.max_length = max_length

        self.generator = generator_class(grammar, data_type)

    def generate(self):

        random_length = randint(self.min_length, self.max_length)
        if random_length:
            generated_list = [self.generator.generate() for _ in range(random_length)]
        else:
            generated_list = []
        return generated_list
