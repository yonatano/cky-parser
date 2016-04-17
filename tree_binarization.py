import random
import simplejson

grammar_ = {
    'S':  [('NP', 'VP')],
    'VP': [('V', 'NP'), ('V', 'NP', 'PP')],
    'NP': [('NP', 'NP'), ('NP', 'PP'), ('N'), ('e')], #NP -> NP NP|NP PP|N|e
    'PP': [('P', 'NP')],
    'N':  [('people'), ('fish'), ('tanks'), ('rods')],
    'V':  [('people'), ('fish'), ('tanks'), ('with')]
}

grammar_ = {
    'S': [('N', 'N')],
    'B': [('derp',)],
    'N': [('fish',), ('taco',), ('B',)] #N -> fish|taco|B
}

def unit_productions(grammar, nonterminals):
    """Retrieve all rules of the form A->B where A,B are nonterminals"""
    unit_prods = []
    for k,v in grammar.iteritems():
        unit_prods.extend([(k, c[0]) for c in v if (len(c) == 1 and 
                          c[0] in nonterminals and k in nonterminals)])
    return unit_prods

def binarize_grammar(grammar, startsym, terminals, nonterminals):
    """Transforms a grammar to Chomsky normal form"""

    """Add a new start symbol -- 
    start symbol cannot occur on right-hand side of a rule."""
    grammar[startsym + '0'] = [(startsym)]
    nonterminals.append(startsym)
    startsym += '0'

    """Remove null productions --
    remove all X where X->e or X->...->e."""

    """Remove unit productions -- 
    for every A->B, append A->X for every X in B->X, remove A->B."""
    unit_prods = unit_productions(grammar, nonterminals)
    while unit_prods: #removal of unit productions can generate more
        for up in unit_prods:
            "Append rules of the form A->X for every rule B->X"
            grammar[up[0]].extend( [x for x in grammar[up[1]]] )
            grammar[up[0]].remove( (up[1],) )
        unit_prods = unit_productions(grammar, nonterminals)


    print grammar

binarize_grammar(grammar_, 'S', ['fish', 'taco', 'derp', 'e'], ['B', 'N'])



