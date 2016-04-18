"""
S → NP VP
VP → V NP
VP → VP PP
V → eat
NP → NP PP
NP → we
NP → sushi
NP → tuna
PP → P NP
P → with
"""
grammar = {
    'S': [('NP', 'VP')],
    'VP': [('V', 'NP'), ('VP', 'PP')],
    'V': [('eat',)],
    'NP': [('NP', 'PP'), ('we',), ('sushi',), ('tuna',)],
    'PP': [('P', 'NP')],
    'P': ['with'],
}

class CkyParser():
    def __init__(self, grammar, terminals, nonterminals):
        self.grammar = grammar
        self.terminals = terminals
        self.nonterminals = nonterminals

    def parse(self, input_):
        parse_table = [[None for i in range(len(input_) + 1)] for i in range(len(input_) + 1)]
        for i,j in zip(range(1, len(input_)), range(1, len(input_))):
            

        for i in range(1, len(input_) + 1):
            for j in range(1, len(input_) + 1):
                []


