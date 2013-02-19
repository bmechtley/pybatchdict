pybatchdict.
==============

Simple tool for using dictionaries to configure options for batch processes. Given any 
dictionary, each key can be a nested dictionary with a key "#var" that takes on a list of values. 
pybatchdict can then generate a list of dictionaries of combinations of those values. Here's a 
quick example:

	>>> from pybatchdict import *
	>>> dictionary = {
	... 'a': {'#var': [1, 2]},
	...	'b': 'hello',
	...	'c': '#var': [3, 4]},
	... }
	>>> parseconfig(dictionary)
	[{'a': 1, 'c': 3, 'b': 'hello'}, {'a': 1, 'c': 4, 'b': 'hello'}, {'a': 2, 'c': 3, 'b': 'hello'}, {'a': 2, 'c': 4, 'b': 'hello'}]	


Other methods for nested dictionaries.
======================================

pybatchdict also has a couple handy methods for dealing with nested dictionaries, namely 
setkeypath and getkeypath. pybatchdict refers to a path to a key in a nested dictionary as a 
keypath that uses "/" as a delimiter. For example, {'a' : {'b' : 0, 'c' : 1}} has keypath '/a/b' 
and '/a/c'.

Warning.
========

There is probably already a much better way of doing all this using some other Python module. Let me know!