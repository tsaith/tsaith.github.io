Title: Implement multilayer perceptron for digit recognition
Date: 2015-12-23 14:02:41
Tags: cv
Category: Machine learning
Status:

This post will demonstrate how to implement multilayer perceptron for digit recognition.

The detailed derivations of algorithm can be found from [this script](https://drive.google.com/file/d/0B6IJ6j3ytMuqQlFHODB0b2tMY0U/view?usp=sharing).

### Main workflow

* Preparing training/validation/testing datasets.
* Set the weight decay / numerical parameters.
* Check if the gradients of the loss function are correct.
* Training model.
* Estimate the accuracy of predictions.

### Ipython notebook

{% notebook dnn_mlp_mnist.ipynb %}

### Multilayer perceptron

[gist:id=a592bbdec4688887e88a]

In case you are interested in all codes related in this demonstration, please check the [repository](https://github.com/tsaith/dnn_play).
