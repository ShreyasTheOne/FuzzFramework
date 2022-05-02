from random import choice, randint
from core.mutation_fuzzer.data_generators.base import BaseGenerator


class StrGenerator(BaseGenerator):
    """
    Takes initial list of seeds to mutate, and generates
    mutated strings from them
    """

    def __init__(self, seeds, min_mutations=2, max_mutations=10, fuzz_prob=1):

        self.seeds = seeds
        self.fuzz_prob = fuzz_prob
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.seed_index = 0

    def generate(self):

        value = None
        if self.seed_index < len(self.seeds):
            value = self.seeds[self.seed_index]
            self.seed_index += 1
        else:
            value = self.__create_candidate()

        return value

    def __create_candidate(self):
        """
        Chose random seed and modify it
        self.trials number of times
        """

        value = choice(self.seeds)
        if self._should_fuzz():
            # Record values for each generation, and analyse results,
            # And choose optimal value (and/or range) to decide trial number.
            trials = randint(self.min_mutations, self.max_mutations)
            for _ in range(trials):
                value = self.__mutate(value)
        return value

    def __mutate(self, value):
        """
        Choose random mutator and mutate
        """

        mutators = [
            self.__delete_random_character,
            self.__insert_random_character,
            self.__modify_random_character,
            self.__flip_random_character,
        ]

        random_mutator = choice(mutators)
        return random_mutator(value)

    def __delete_random_character(self, value):
        """
        Return value with random character deleted
        """

        if not value:
            return value

        random_index = randint(0, len(value) - 1)
        return value[0:random_index] + value[random_index + 1 :]

    def __insert_random_character(self, value):
        """
        Return value with random character
        inserted at random position
        """

        random_character = chr(randint(32, 126))
        if not value:
            return str(random_character)

        random_index = randint(0, len(value) - 1)
        return value[:random_index] + random_character + value[random_index:]

    def __flip_random_character(self, value):
        """
        Return value with character
        flipped at random position
        """

        if not value:
            return value

        random_index = randint(0, len(value) - 1)
        char_at_index = value[random_index]
        flipped_char = chr(ord(char_at_index) ^ (1 << randint(0, 6)))
        return value[:random_index] + flipped_char + value[random_index + 1 :]

    def __modify_random_character(self, value):
        """
        Return value with character
        modified at random position
        """

        if not value:
            return value

        random_index = randint(0, len(value) - 1)
        random_character = chr(randint(32, 126))
        return value[:random_index] + random_character + value[random_index + 1 :]
