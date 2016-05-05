import copy
from cky_parser import CkyParser
from tree_binarization import binarize_grammar

def print_tree(tree, depth):
        if tree is None:
            return
        print_tree(tree['right'], depth + 1)
        print "\t    " * depth + "/" if tree['right'] is not None else ""
        print "\t" * depth + tree['symbol']
        print "\t    " * depth + "\\" if tree['left'] is not None else ""
        print_tree(tree['left'], depth + 1)

def stringify_cfg(cfg):
    stringified = ""
    for k,v in cfg.iteritems():
        v_ = [''.join(c) for c in v]
        stringified += "{}->{}\n".format(k, "|".join(v_))
    return stringified

if __name__ == "__main__":
    """Test binarization"""
    grammar_ = {
        'S': [('A', 'S', 'A'), ('a', 'B')],
        'A': [('B',), ('S',)],
        'B': [('b',), ('e',)],
    }
    terminals_ = ['a', 'b', 'e']
    nonterminals_ = ['S', 'A', 'B']

    grammar_chomsky_nf = binarize_grammar(grammar_, 'S', terminals_, nonterminals_)
    
    print "Pre-binarization:\n%s" % stringify_cfg(grammar_)
    print "Post-binarization:\n%s" % stringify_cfg(grammar_chomsky_nf)

    """Test Parser"""
    grammar = {
        'S': [('NP', 'VP')],
        'VP': [('V', 'NP'), ('VP', 'PP')],
        'V': [('eat',)],
        'NP': [('NP', 'PP'), ('we',), ('sushi',), ('tuna',)],
        'PP': [('P', 'NP')],
        'P': [('with',)],
    }
    terminals = ['eat', 'we', 'sushi', 'tuna', 'with']
    nonterminals = grammar.keys()
    cky = CkyParser(grammar, terminals, nonterminals)
    parse_trees = cky.parse("we eat sushi with tuna".split())
    for tree in parse_trees:
        print "tree:"
        print_tree(tree, 1)
        print "\n\n"