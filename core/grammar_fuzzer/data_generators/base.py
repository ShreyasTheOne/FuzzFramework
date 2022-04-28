import re
from copy import deepcopy
from random import choice, seed

from core.grammar_fuzzer.constants.regex import RE_NONTERMINAL

class BaseGenerator:
    
    def __init__(self, grammar):

        self.min_nonterminals = grammar["min_nonterminals"]
        self.max_nonterminals = grammar["max_nonterminals"]

        self.expansions = grammar["expansions"]
        self.start = grammar.get("start", None) if grammar.get("start", None) else "<start>"
        
        self.__initialise_grammar()

        self.random_seed = 0

    def generate(self):
        """
        Derives a new tree from the start symbol
        and returns it as a string of terminals.
        """

        root = self.__init_tree()
        root = self.__expand_tree(root)

        return self.__tree_to_string(root)

    def __initialise_grammar(self):
        """
        Calculates symbol and expansion costs
        to be used in different phases
        """
        
        self.symbol_costs = dict()
        self.expansion_costs = dict()
        self.__expanded_children = dict()

        for symbol in self.expansions.keys():
            _ = self.__get_symbol_cost(symbol)


    def __get_symbol_cost(self, symbol, seen = set()):
        """
        Returns the minimum number of steps 
        required to reach a sentence starting from
        the given symbol
        """

        if symbol not in self.symbol_costs:
            self.symbol_costs[symbol] = min(
                self.__get_expansion_cost(p, seen | {symbol})
                for p in self.expansions[symbol]
            )
        
        return self.symbol_costs[symbol]

    def __get_expansion_cost(self, expansion, seen = set()):
        """
        Sum of symbol costs of all
        symbols in the string
        """

        if expansion not in self.expansion_costs:
            symbols = self.__extract_non_terminals(expansion)
            
            if len(symbols) == 0:
                return 1
            
            elif any(symbol in seen for symbol in symbols):
                self.expansion_costs[expansion] = float('inf')
            
            else:
                self.expansion_costs[expansion] = sum(
                    self.__get_symbol_cost(symbol, seen) 
                    for symbol in symbols
                ) + 1

        return self.expansion_costs[expansion]

    def __extract_non_terminals(self, expansion):
        """
        Returns a list of non_terminals
        in the given expansion
        """

        if isinstance(expansion, tuple):
            expansion = expansion[0]
        expansion = str(expansion)
        
        return RE_NONTERMINAL.findall(expansion)
    
    def __is_non_terminal(self, string):
        return RE_NONTERMINAL.match(string)
    
    def __init_tree(self):
        """
        Returns an empty root node to
        be expanded at the beginning of 
        data generation
        """

        return (self.start, None)
    
    def __expand_tree(self, root):
        """
        Expand tree in three phases
        """
        
        phases = [
            (self.__expand_node_max_cost, self.min_nonterminals),
            (self.__expand_node_randomly, self.max_nonterminals),
            (self.__expand_node_min_cost, None)
        ]

        for p in phases:
            expand_node_method, limit = p
            root = self.__expand_tree_by_phase(root, expand_node_method, limit)
        
        return root

    def __expand_tree_by_phase(self, root, expand_node_method, limit=None):
        """
        Expand tree using the given node expansion
        method which is based on the phase
        """

        self.__expand_node = expand_node_method
        while (
            ((limit is None) or (self.__possible_expansions(root) < limit))
            and
            self.__able_to_expand(root)            
        ):
            root = self.__expand_tree_once(root)
        
        return root
    
    def __expand_node_max_cost(self, node):
        return self.__expand_node_by_cost(node, max)
    
    def __expand_node_min_cost(self, node):
        return self.__expand_node_by_cost(node, min)

    def __expand_node_randomly(self, node):
        return self.__expand_node_by_cost(node, choice)
    
    def __expand_node_by_cost(self, node, choose):
        """
        Choose a node with min/max/random cost of expansion,
        based on the phase
        """

        symbol, children = node
        assert children == None

        expansions = self.expansions[symbol]
        possible_children_with_costs = [
            (
                self.__expansion_to_children(e), 
                self.__get_expansion_cost(e, {symbol}),
                e
            )
            for e in expansions
        ]

        costs = [cost for (c, cost, e) in possible_children_with_costs]
        chosen_cost = choose(costs)

        children_with_chosen_cost = [
            c for (c, cost, _) in possible_children_with_costs
            if cost == chosen_cost
        ]
        chosen_children = choice(children_with_chosen_cost)
        return (symbol, chosen_children)

    def __expand_tree_once(self, root):
        """
        If the current node is yet to be expanded,
        expand it. Else, iterate over its children and expand
        a random child.
        """

        symbol, children = root
        if children is None:
            root = self.__expand_node(root)
        else:
            possible_children_to_expand = [
                i for (i, c) in enumerate(children) if
                self.__able_to_expand(c)
            ]

            chosen_index = choice(possible_children_to_expand)
            children[chosen_index] = self.__expand_tree_once(children[chosen_index])
        
        return root

    def __possible_expansions(self, root):
        """
        Count the number of non_terminals in
        the tree with the given root
        """

        symbol, children = root
        if children is None:
            return 1
        
        return sum(self.__possible_expansions(c) for c in children)

    def __able_to_expand(self, root):
        """
        Check if any non terminal exists in t==
        the tree with the given root
        """
        symbol, children = root
        if children is None:
            return True
        
        return any(self.__able_to_expand(c) for c in children)

    def __expansion_to_children(self, expansion):
        """
        Takes an expansion as a string and returns
        a list of children to be used as a tree node
        """

        if isinstance(expansion, tuple):
            expansion = expansion[0]
        expansion = str(expansion)

        if expansion not in self.__expanded_children:
            if expansion == "":
                self.__expanded_children[expansion] = [("", [])]
            else:
                all_strings = re.split(RE_NONTERMINAL, expansion)
                self.__expanded_children[expansion] = \
                [
                    (
                        s,
                        None if self.__is_non_terminal(s) else []
                    )
                    for s in all_strings
                ]
        children = deepcopy(self.__expanded_children[expansion])
        return children

    def __tree_to_string(self, root):
        """
        Return a string of all terminals in the tree 
        (which is the result of the derivation tree with the given root)
        """
        
        symbol, children = root

        if children is None:
            # Non terminal which hasn't been expanded yet
            return ''
        if not children:
            # Terminal reached
            return symbol
        
        # Non terminal which has been expanded
        return ''.join([self.__tree_to_string(s) for s in children])
