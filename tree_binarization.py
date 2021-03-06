# -*- coding: utf-8 -*-

"""
tree_binarization: a set of functions used to binarize a CFG (Chomsky normal form)
"""

import copy
import itertools
import random
import string

def get_or_create_rule(grammar, nonterminals, target):
    """Returns the name of the rule X->target, or creates the rule if it is not
    already in the grammar."""
    exists = [n for n in nonterminals if target == grammar[n]]
    if exists:
        return exists[0]
    
    while True:
        alphabet = string.ascii_uppercase
        try:
            new_name = random.choice(list(set(alphabet) - set(nonterminals)))
            nonterminals.append(new_name)
            grammar[new_name] = target
            return new_name
        except IndexError:
            alphabet = [''.join(z) for z in zip(alphabet, string.ascii_uppercase)]
            continue
        break

def unit_productions(grammar, nonterminals):
    """Retrieve all rules of the form A->B where A,B are nonterminals"""
    unit_prods = []
    for k,v in grammar.iteritems():
        unit_prods.extend([(k, c[0]) for c in v if (len(c) == 1 and 
                          c[0] in nonterminals and k in nonterminals)])
    return unit_prods

def null_productions_swaps(production, symbol):
    """Given ('A', 'B', 'A') and 'A', returns: 
    [('B', 'A'), ('A', 'B'), ('B',)]"""
    productions = []
    symbol_indeces = [i for i,k in enumerate(production) if k == symbol]
    permutations = []
    for i in range(1, len(production) + 1): #aggregate all combinations of indeces to nullify
        permutations.extend(list(itertools.combinations(symbol_indeces, i)))

    for p in permutations:
        new_prod = tuple(sym for k,sym in enumerate(production) if k not in p)
        productions.append(new_prod)
        
    productions = [p for p in productions if p]
    return productions

def multivariable_productions(grammar, nonterminals):
    """Retrieve all rules of the form A->X where X is a number of symbols > 2"""
    multivar_prods = []
    for k,v in grammar.iteritems():
        multivar_prods.extend([(k,c) for c in v if len(c) > 2])
    return multivar_prods

def two_variable_productions(grammar, nonterminals, terminals):
    """Retrieve all rules of the form A->aB"""
    twovar_prods = []
    for k,v in grammar.iteritems():
        twovar_prods.extend([(k,c) for c in v if (len(c) == 2 and c[0] in 
                              terminals and c[1] in nonterminals)])
    return twovar_prods

def binarize_grammar(grammar, startsym, terminals, nonterminals):
    """Transforms a grammar to Chomsky normal form"""
    grammar = copy.deepcopy(grammar)

    """Add a new start symbol -- 
    start symbol cannot occur on right-hand side of a rule."""
    grammar[startsym + '0'] = [(startsym,)]
    nonterminals.append(startsym + '0')

    """Remove null productions --
    For every A->e, change the productions containing A by replacing 
    each occurence of A with e, then remove A->e."""
    null_prods = [(k, 'e') for k,v in grammar.iteritems() if ('e',) in v]
    while null_prods:
        for np in null_prods:
            #find each X->K such that K reduces to np[0]
            for k,v in grammar.iteritems():
                for i,c in enumerate(v[:]):
                    if np[0] in c:
                        if c == (np[0],):
                            grammar[k].append(('e',))
                        else:
                            grammar[k].extend(null_productions_swaps(c, np[0]))  
            grammar[np[0]].remove(('e',))
        null_prods = [(k, 'e') for k,v in grammar.iteritems() if ('e',) in v]

    """Remove unit productions -- 
    for every A->B, append A->X for every X in B->X, remove A->B."""
    unit_prods = unit_productions(grammar, nonterminals)
    while unit_prods: #removal of unit productions can generate more
        for up in unit_prods:
            "Append rules of the form A->X for every rule B->X"
            grammar[up[0]].extend( [x for x in grammar[up[1]] if x not in 
                                  grammar[up[0]]] )
            grammar[up[0]].remove( (up[1],) )
        unit_prods = unit_productions(grammar, nonterminals)

    """Remove multi-variable productions --
    for every A->B1...Bn, replace with A->B1C C->B2...Bn"""
    multivar_prods = multivariable_productions(grammar, nonterminals)
    while multivar_prods:
        for k,c in multivar_prods:
            grammar[k].remove(c)
            prod_name = get_or_create_rule(grammar, nonterminals, [c[1:]])
            grammar[k].append((c[0], prod_name))
        multivar_prods = multivariable_productions(grammar, nonterminals)

    """Remove productions of the form A->aB --
    for every A->aB, replace with A->XB and X->a"""
    twovar_prods = two_variable_productions(grammar, nonterminals, terminals)
    while twovar_prods:
        for k,c in twovar_prods:
            grammar[k].remove(c)
            prod_name = get_or_create_rule(grammar, nonterminals, [(c[0],)])
            grammar[k].append((prod_name, c[1]))
        twovar_prods = two_variable_productions(grammar, nonterminals, terminals)

    """remove emptied productions and duplicate ORs"""
    to_del = [k for k in grammar if not grammar[k]]
    for k in to_del:
        grammar.pop(k)

    for k,v in grammar.iteritems():
        grammar[k] = list(set(v))

    return grammar