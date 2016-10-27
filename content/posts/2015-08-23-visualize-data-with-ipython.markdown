Title: Visualize data with IPython
Date: 2015-08-23
Tags: python
Category: Machine learning


This post will show how to visualize data with ipython.

### matplotlib

- install: `pip install matplotlib`

With [matplotlib](http://matplotlib.org/),
we are able to make inline plots by setting

```python
%matplotlib inline
import matplotlib.pyplot as plt
```

e.g.

{% img https://farm6.staticflickr.com/5769/20180189424_94f41513fe_c.jpg %}

### mpld3

- install: `pip install matplotlib`

With [mpld3](http://mpld3.github.io/), it is handy to zoom in/out or shift the plot through the lower left icons.

To use mpld3, the following lines are required.
```python
import mpld3
mpld3.enable_notebook()
```

e.g.

{% img https://farm6.staticflickr.com/5750/20802774815_feb20ff153_c.jpg %}
