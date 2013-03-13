I tend to use YAML to create config files for various sciency algorithms I use/make, converting them into python
dictionaries and using `**` keyword argument unpacking. I also tend to test these algorithms against varying tunings of
parameters, often combinatorically. Here's some code to indicate, in a (nested) dictionary, over which parameters you
want to iterate and generate a bunch of copies of the original dictionary.

# pybatchdict.

Simple tool for using dictionaries to configure options for batch processes. Given any dictionary, each key can be a
nested dictionary with a key "@var" that takes on a list of values, where "var" is any identifier, including the empty
string. Values iterated by the same identifier will be part of the same group, and so should have the same number of
elements, similar to `zip()`. pybatchdict can then generate a list of dictionaries of combinations of those values.
Uses `itertools.product` Here's a quick example:

```python
>>> from pybatchdict import *
>>> config = {
... 'a': {'@1': [1, 2, 3]},
...	'b': {'@1': [4, 5, 6]},
...	'c': {'@': [7, 8]},
... 'd': 9
... }
>>> parseconfig(config)
[{'a': 1, 'b': 4, 'c': 7, 'd': 9},
{'a': 1, 'b': 4, 'c': 8, 'd': 9},
{'a': 2, 'b': 5, 'c': 7, 'd': 9},
{'a': 2, 'b': 5, 'c': 8, 'd': 9},
{'a': 3, 'b': 6, 'c': 7, 'd': 9},
{'a': 3, 'b': 6, 'c': 8, 'd': 9}]
```

Also works fine with dictionaries with no variable arguments:

```python
>>> config = {'a': {'b': 0, 'c': 1}}
>>> parseconfig(config)
[{'a': {'c': 1, 'b': 0}}]
```

Works well with [PyYAML](http://pyyaml.org/wiki/PyYAML) (or anything else, like XML, that can easily be converted to a
nested dictionary) and `**` dictionary keyword argument unpacking :D 

Other methods for nested dictionaries.
======================================

I also use a couple handy methods for dealing with nested dictionaries, namely `setkeypath` and `getkeypath`.
pybatchdict refers to a path to a key in a nested dictionary as a keypath that uses "/" as a delimiter. For example, 
`{'a' : {'b' : 0, 'c' : 1}}` has keypaths '/a', '/a/b', and '/a/c'.

```python
>>> from pybatchdict import *
>>> config = {'a': {'b': 0, 'c': 1}}
>>> getkeypath(config, '/a')
{'c': 1, 'b': 0}
>>> getkeypath(config, '/a/b')
0
>>> getkeypath(config, '/a/c')
1
>>> setkeypath(config, '/a/b', 'hi')
>>> config
{'a': {'c': 1, 'b': 'hi'}}
```

Warning.
========

There is probably already a much better way of doing all this using some other Python module. Let 
me know!

TODO.
=====

1. Tests? Ain't nobody got time for that.
