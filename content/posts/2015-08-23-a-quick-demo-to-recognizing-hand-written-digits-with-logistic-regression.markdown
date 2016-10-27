Title: A quick demo to recognizing hand-written digits with logistic regression
Date: 2015-08-23
Tags: cv, python
Category: Machine learning


This article will quickly demonstrate how to use the [Logistic regression](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression) to recognize hand-written digits.

The [scikit-learn](http://scikit-learn.org/stable/index.html) package is required in the example shown later. If you haven't installed it, please executing
```
pip install scikit-learn
```
and make sure that your IPython is ready to go.

In this example, we want to fit a model of logistic regression with training data and labels.
After that, the model can be used to predict the label corresponding to each instance of testing data.

```python
%matplotlib inline
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model

digits = datasets.load_digits()
train_set_x = digits.data[:-10, :]      # Training set x
train_set_y = digits.target[:-10]       # Training set y (labels)
test_set_x = digits.data[-10:, :]       # Test set x
test_set_y = digits.target[-10:]        # Test set y (labels)
test_set_images = digits.images[-10:]   # Test set images

clf = linear_model.LogisticRegression() # Logistic regression
clf.fit(train_set_x, train_set_y)       # Fitting model

predicted_y = clf.predict(test_set_x)
print("Predicted y = ", predicted_y) # Predicted labels
print("Test set  y = ", test_set_y)  # Expected labels

plt.imshow(test_set_images[-1], cmap=plt.cm.gray) # Show the last image in the test set
```

and the output is as

{% img https://farm1.staticflickr.com/634/20189529253_c63a2b993d_c.jpg %}

As observed, the predicted labels are consistent with the expected ones.
The last label is 8 as we see.
