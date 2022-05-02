from random import randint, choice
from copy import deepcopy
from pprint import pprint
from core.grammar_fuzzer.data_generators import BaseGrammarGenerator



class BaseGrammarMutationGenerator(BaseGrammarGenerator):

    def __init__(self, grammar, data_type, num_seeds=2):
        
        super().__init__(grammar, data_type)
        self.generate_seeds(num_seeds)
        self.seed_index = 0

    def generate(self):
        """
        """

        value = None

        if self.seed_index < len(self.seeds):
            value = self.tree_to_string(
                self.seeds[self.seed_index]
            )
            self.seed_index += 1
        else:
            value = self.create_candidate()

        return self.data_type(value)

    def create_candidate(self):
        """
        """

        seed_index = randint(0, len(self.seeds)-1)
        seed_root = self.seeds[seed_index]
        mutable_nodes = []

        queue = [seed_root]

        while len(queue):
            node = queue[-1]
            queue = queue[:-1]

            symbol, children = node
            if self.is_non_terminal(symbol):
                mutable_nodes.append(node)
            
            for c in children:
                queue.append(c)

        
        candidate_node = choice(mutable_nodes)
        original_candidate = deepcopy(candidate_node)
        symbol, children = candidate_node
        generator = BaseGrammarGenerator(self.grammar, self.data_type, symbol)

        candidate_mutated = generator.generate_tree()
        candidate_node[1] = candidate_mutated[1]
        value = self.tree_to_string(seed_root)
        candidate_node[1] = original_candidate[1]

        return value
    
    def generate_seeds(self, num_seeds):
        """
        """

        self.seeds = []
        
        for i in range(num_seeds):

            seed = self.generate_tree()
            self.seeds.append(seed)
