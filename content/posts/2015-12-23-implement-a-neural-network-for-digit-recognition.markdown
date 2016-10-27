Title: Implement a neural network for digit recognition
Date: 2015-12-23 09:51:04
Tags: cv
Category: Machine learning
Status:


This post will demonstrate how to implement a three-layers [neural network](http://deeplearning.stanford.edu/wiki/index.php/Neural_Networks) for digit recognition.

The detailed derivations of algorithm can be found from [this script](https://drive.google.com/file/d/0B6IJ6j3ytMuqVjVBOHM3RG1sajA/view?usp=sharing).

### Main workflow

* Preparing training/validation/testing datasets.
* Set the weight decay / numerical parameters.
* Check if the gradients of the loss function are correct.
* Training model.
* Estimate the accuracy of predictions.

### Ipython notebook

{% notebook dnn_neural_net_mnist.ipynb %}

### NeuralNet classifier

[gist:id=f52c9be62504f52cc9ec]

In case you are interested in all codes related in this demonstration, please check the [repository](https://github.com/tsaith/dnn_play).
