Title: Implement stacked multilayer perceptron for digit recognition
Date: 2015-12-23 17:44:51
Tags: cv
Category: Machine learning
Status:

This post will demonstrate how to implement stacked multilayer perceptron for digit recognition.

Here, we consider a [multilayer perceptron](implement-multilayer-perceptron-for-digit-recognition) with four layers and employ the technology of [sparse autoencoder](implement-sparse-autoencoder-for-digit-recognition) to determine the initial values of weighting parameters for the first three layers.

### Main workflow

* Preparing training/validation/testing datasets.
* Set the hyperparameters and numerical parameters.
* Determining the initial values for each layer.
* Fine-tuning the model.
* Estimate the accuracy of predictions.

### Ipython notebook

{% notebook dnn_stacked_mlp_mnist.ipynb %}

### Sparse autoencoder

[gist:id=36efe5fc788fab08a595]

### Multilayer perceptron

[gist:id=a592bbdec4688887e88a]

In case you are interested in all codes related in this demonstration, please check the [repository](https://github.com/tsaith/dnn_play).
