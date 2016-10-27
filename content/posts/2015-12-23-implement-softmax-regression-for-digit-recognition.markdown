Title: Implement softmax regression for digit recognition
Date: 2015-12-23 13:15:05
Tags: cv
Category: Machine learning
Status:


This post will demonstrate how to implement [softmax regression](http://deeplearning.stanford.edu/wiki/index.php/Softmax_Regression) for digit recognition.

The detailed derivations of algorithm can be found from [this script](https://drive.google.com/file/d/0B6IJ6j3ytMuqWHEzMUNFSllWWWM/view?usp=sharing).

### Main workflow

* Preparing training/validation/testing datasets.
* Set the weight decay / numerical parameters.
* Check if the gradients of the loss function are correct.
* Training model.
* Estimate the accuracy of predictions.

### Ipython notebook

{% notebook dnn_softmax_mnist.ipynb %}

### Softmax classifier

[gist:id=290471a7ef508850139a]

In case you are interested in all codes related in this demonstration, please check the [repository](https://github.com/tsaith/dnn_play).
