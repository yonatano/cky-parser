# -*- coding: utf-8 -*-

"""
A CKY parser implementation.
"""

class CkyParser():
    
    def __init__(self, grammar, terminals, nonterminals):
        self.grammar = grammar
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.new_entry = lambda symbol, leftChild, rightChild: {'symbol': symbol, 'left':leftChild, 'right':rightChild}

    def rules_for_entry(self, entry):
        rules = []
        for rule, components in self.grammar.iteritems():
            if entry in components:
                rules.append(rule)
        return rules

    def parse(self, input_):
        cky_table = {}
        for i in range(1, len(input_) + 1):
            for j in range(1, len(input_) + 1):
                cky_table[i, j] = []

        #initialize the table
        for i in range(1, len(input_) + 1):
            symbols = self.rules_for_entry((input_[i-1],))
            for s in symbols:
                cky_table[i, i].append(self.new_entry(s, None, None))

        #fill out the table
        def fill_chart(chartsz):
            for span in range(1, chartsz):
                for i in range(1, chartsz - span + 1):
                    fill_cell(i, i + span)

        def fill_cell(i, j):
            for k in range(i, j):
                combine_cells(i, k, j)

        def combine_cells(i, k, j):
            for y in cky_table[i, k]:
                for z in cky_table[k + 1, j]:
                    for x in self.nonterminals:
                        if (y['symbol'], z['symbol']) in self.grammar[x]:
                            cky_table[i, j].append(self.new_entry(x, y, z))
                     
        fill_chart(len(input_))
        return cky_table[1, len(input_)]