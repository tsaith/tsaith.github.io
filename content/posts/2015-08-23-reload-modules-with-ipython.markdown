Title: Automatically reload modules in IPython
Date: 2015-08-23
Tags: python
Category: Machine learning


IPython provides an extension [autoreload](https://ipython.org/ipython-doc/dev/config/extensions/autoreload.html) to reload the modules automatically.
This is especially useful because we don't want to manually reload modules for testing when developing new functions.

Just execute the following lines within IPython, all modules will be automatically reloaded before executing your code.

```python
%load_ext autoreload
%autoreload 2
```
