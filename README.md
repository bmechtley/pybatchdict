pybatchdict.
==============

Simple tool for using dictionaries to configure options for batch processes. UGiven any 
dictionary, each key can be a nested dictionary with a key "#var" that takes on a list of values. 
pybatchdict can then generate a list of dictionaries of combinations of those values. Uses `itertools.product` Here's a quick example:

```python
>>> from pybatchdict import *
>>> dictionary = {
... 'a': {'#var': [1, 2]},
...	'b': ':D',
...	'c': {'#var': [3, 4]},
... }
>>> parseconfig(dictionary)
[{'a': 1, 'b': ':D', 'c': 3},
{'a': 2, 'b': ':D', 'c': 3},
{'a': 1, 'b': ':D', 'c': 4},
{'a': 2, 'b': ':D', 'c': 4}]
```

Works well with [PyYAML](http://pyyaml.org/wiki/PyYAML) (or anything else, like XML, that can easily be converted to a nested dictionary) and `**` dictionary keyword argument unpacking :D 

Other methods for nested dictionaries.
======================================

pybatchdict also has a couple handy methods for dealing with nested dictionaries, namely 
`setkeypath` and `getkeypath`. pybatchdict refers to a path to a key in a nested dictionary as a 
keypath that uses "/" as a delimiter. For example, `{'a' : {'b' : 0, 'c' : 1}}` has keypaths '/a/b' 
and '/a/c'.

```python
>>> from pybatchdict import *
>>> dictionary = {'a': {'b': 0, 'c': 1}}
>>> dictionary
{'a': {'b': 0, 'c': 1}}
>>> setkeypath(dictionary, '/a/b', 'hi')
>>> dictionary
{'a': {'b': 'hi', 'c': 1}}
>>> getkeypath(dictionary, '/a/c')
1
```

Warning.
========

There is probably already a much better way of doing all this using some other Python module. Let me know!

TODO.
=====

1. Documentation that is not stream-of-consciousness.
1. Use multiple #var (e.g. #var-a, #var-b) tags to indicate that arguments should be zipped pairwise rather than iterated combinatorically.
1. Allow non-string keywords. Not sure if this actually matters since the normal use case is to use YAML/XML config files.
1. Tests? Ain't nobody got time for that.
