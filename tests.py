import copy
from tree_binarization import binarize_grammar

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