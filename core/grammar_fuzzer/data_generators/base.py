import re
from pprint import pprint

class BaseGenerator:
    
    def __init__(self, grammar):

        self.min_nonterminals = grammar["min_nonterminals"]
        self.max_nonterminals = grammar["max_nonterminals"]

        expansions = grammar["expansions"]
        self.start = grammar.get("start", None) if grammar.get("start", None) else "<start>"
        
        self.__initialise_grammar(expansions)
    
    def generate(self):
        pass

    def __initialise_grammar(self, expansions):
        
        self.symbol_costs = dict()
        self.expansion_costs = dict()
        for symbol in expansions.keys():
            _ = self.__get_symbol_cost(symbol, expansions)
        
    
    def __get_symbol_cost(self, symbol, expansions, seen = set()):

        if symbol not in self.symbol_costs:
            self.symbol_costs[symbol] = min(
                self.__get_expansion_cost(p, expansions, seen | {symbol})
                for p in expansions[symbol]
            )
        
        return self.symbol_costs[symbol]

    def __get_expansion_cost(self, expansion, expansions, seen = set()):

        if expansion not in self.expansion_costs:
            symbols = self.__extract_non_terminals(expansion)
            
            if len(symbols) == 0:
                return 1
            
            elif any(symbol in seen for symbol in symbols):
                self.expansion_costs[expansion] = float('inf')
            
            else:
                self.expansion_costs[expansion] = sum(
                    self.__get_symbol_cost(symbol, expansions, seen) 
                    for symbol in symbols
                ) + 1

        return self.expansion_costs[expansion]

    def __extract_non_terminals(self, expansion):

            if isinstance(expansion, tuple):
                expansion = expansion[0]
            
            expansion = str(expansion)
            
            RE_NONTERMINAL = re.compile(r'(<[^<>]*>)')
            return RE_NONTERMINAL.findall(expansion)
