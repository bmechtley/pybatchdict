from itertools import product
from copy import deepcopy

def getkeypath(d, keypath, default={}):
    '''Given an input (nested) dictionary and a keypath to a particular key, 
    return the key's value in the dictionary.
    d: dict
        input dictionary
    keypath: str
        path to the key delimited by /. For example, to access key 'b' in 
        {'a': {'b': 0}}, the path is '/a/b'.
    default: anything, optional
        default value to return if the key does not exist in the dictonary.'''

    v = d
    
    keys = keypath.split('/')
    
    for i, key in enumerate(keys):
        v = v.get(key, {} if i < (len(keys) - 1) else default)
    
    return v

def setkeypath(d, keypath, value=None):
    '''Given an input dictionary and the path to a particular key, set the
     key's value in the dictionary.
    d: dict
        input dictionary
    keypath: str or dict
        str: path to the key delimited by /. For example, to access key 'b' in 
        {'a' : {'b' : 0}}, the path is '/a/b'.
        dict: dictionary of form {keypath: value} where each key corresponds to
        a unique keypath within the nested dictionary.
    value: anything, optional
        value to assign the key in the dictionary. Required if keypath is a 
        str rather than a dictionary.'''

    if type(keypath) == dict:
        for k, v in keypath.items():
            setkeypath(d, k, v)
    else:
        keys = [k for k in keypath.split('/') if len(k)]
        
        for key in keys[:-1]:
            d = d[key]
        
        d[keys[-1]] = value

def dictpaths(indict, inpath=''):
    '''Given a (nested) dictionary, enumerate all keypaths in a flat list.
    indict: dict
        input nested dictionary
    inpath: str
        parent path to the current place of execution (is a recursive 
        function, so leave this to its default.)'''
    
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

def pathcombos(paths):
    '''Given a nested dictionary where some values are lists, return a list of 
    flat dictionaries that are combinations of all lists. Output dicts are of
    form {keypath: value} where the keypath is the full path to the nested 
    dictionary key that has an enumerable value and value is value for the 
    individual combination.

    paths: list
        list of str keypaths'''

    keys = [key for key in paths if key.split('/')[-1] == 'iterate']

    listkeys = [
        ['/'.join(key.split('/')[:-1])] * len(paths[key]) 
        for key in keys
    ]

    listdata = [paths[key] for key in keys]

    # O_o
    combokeys = [a for a in product(*listkeys)]
    combodata = [a for a in product(*listdata)]
    
    return [
        {k: v for k, v in zip(a, b)} 
        for a, b in zip(combokeys, combodata)
    ]

def dictlist(combos, data):
    '''Given a list of dictionaries containing keypath: value pairs from 
    pathcombos, return a list of dictionaries that are modified copies of an 
    input dictionary (data), where each dictionary has the values 
    corresponding to the keypaths replaced by their desired values.'''

    dicts = []

    for combo in combos:
        newdict = deepcopy(data)
        setkeypath(newdict, combo)
        dicts.append(newdict)

    return dicts

def parseconfig(d):
    '''Shortcut to automatically generate a list of dictionaries given an 
    input config dictionary.
    d: dict
        input config dictionary'''

    paths = dictpaths(d)
    combos = pathcombos(paths)
    return dictlist(combos, d)
