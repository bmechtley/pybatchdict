"""
batch.py
pybatchdict

2013 Brandon Mechtley

Tools for creating a list of dictionaries
specially formatted input dictionary.

Also has certain tools for helping set/get key-value pairs in nested dictionaries.
"""

from itertools import product
from copy import deepcopy

def getkeypath(d, keypath, default=None):
    """
    :type d: dict
    :param d: input dictionary
    :type keypath: str
    :param keypath: path to the key delimited by /. For example, to access key 'b' in {'a': {'b': 0}}, the path is
        'a/b'.
    :type default: anything
    :param default: optional default value to return if the key does not exist in the dictionary
    
    Given an input (nested) dictionary and a keypath to a particular key, return the key's value in the dictionary.
    """
    if default is None: default = {}

    v = d
    
    keys = keypath.split('/')
    
    for i, key in enumerate(keys):
        if len(key):
            v = v.get(key, {} if i < (len(keys) - 1) else default)
    
    return v

def setkeypath(d, keypath, value=None):
    """
    :type d: dict
    :param d: input dictionary
    :type keypath: str or dict
    :param keypath: if keypath is a string, it is path to the key delimited by /. For example, to access key 'b' in 
        {'a': {'b': 0}}, the path is '/a/b'. If keypath is a dictionary, it is dictionary of form {keypath: value}
        where each key corresponds to a unique keypath within the nested dictionary.
    :type value: anything
    :param value: optional value to assign the key in the dictionary. Required if keypath is a  str rather than a
        dictionary.
    
    Given an input dictionary and the path to a particular key, set the key's value in the dictionary.
    """

    if type(keypath) == dict:
        for k, v in keypath.items():
            setkeypath(d, k, v)
    else:
        keys = [k for k in keypath.split('/') if len(k)]
        
        for key in keys[:-1]:
            d = d[key]
        
        d[keys[-1]] = value

def dictpaths(indict, inpath=''):
    """
    :type indict: dict
    :param indict: input nested dictionary
    :type inpath: str
    :param inpath: parent path to the current place of execution (is a recursive function. So leave this to its 
        default.)
    
    Given a (nested) dictionary, enumerate all keypaths in a flat list.
    """

    if type(indict) != dict:
        return {inpath: indict}
    else:
        outdict = {}

        for key in indict:
            paths = dictpaths(indict[key], inpath + '/' + key)

            if type(paths) == dict:
                for pkey in paths:
                    outdict[pkey] = paths[pkey]
            else:
                for ele in paths:
                    for ekey in ele:
                        outdict[ekey] = ele[ekey]

        return outdict

def pathcombos(paths, data):
    """
    :type paths: list
    :param paths: list of str keypaths.
    :type data: dict
    :param data: original config dictionary with lists to which the keypaths refer.
    
    Given a nested dictionary where some values are lists, return a list of flat dictionaries that are combinations of
    all lists. Output dicts are of form {keypath: value} where the keypath is the full path to the nested dictionary
    key that has an enumerable value and value is value for the individual combination.
    """

    keys = [key for key in paths if key.split('/')[-1] == 'iterate']

    listkeys = [['/'.join(key.split('/')[:-1])] * len(paths[key]) for key in keys]
    listdata = [paths[key] for key in keys]

    # O_o
    combokeys = [a for a in product(*listkeys)]
    combodata = [a for a in product(*listdata)]
    combodict = [{k: v for k, v in zip(a, b)} for a, b in zip(combokeys, combodata)]

    return combodict


def dictlist(combos, data):
    """
    :type combos: dict
    :param combos: dictionary of combinations of the iterated parameters.
    :type data: dict
    :param data: original dictionary to copy combinations' values into.
    
    Given a list of dictionaries containing keypath: value pairs from pathcombos, return a list of dictionaries that
    are modified copies of an input dictionary (data), where each dictionary has the values corresponding to the
    keypaths replaced by their desired values.
    """

    dicts = []

    for combo in combos:
        newdict = deepcopy(data)
        setkeypath(newdict, combo)
        dicts.append(newdict)

    return dicts

def parseconfig(d):
    """
    :type d: dict
    :param d: input configuration dictionary
    
    Shortcut to automatically generate a list of dictionaries given an input config dictionary.
    """

    paths = dictpaths(d)
    combos = pathcombos(paths, d)
    return dictlist(combos, d)
