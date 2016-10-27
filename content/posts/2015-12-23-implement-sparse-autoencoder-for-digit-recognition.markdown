Title: Implement sparse autoencoder for digit recognition
Date: 2015-12-23 14:34:56
Tags: cv
Category: Machine learning
Status:

Here, we will see how to implement [sparse autoencoder](http://deeplearning.stanford.edu/wiki/index.php/Autoencoders_and_Sparsity) for digit recognition.
Such autoencoder can be employed to extract useful features to represent the raw data.

The detailed derivations of algorithm can be found from [this script](https://drive.google.com/file/d/0B6IJ6j3ytMuqVXJSTDFCb0doS3M/view?usp=sharing).

### Main workflow

* Preparing training/validation/testing datasets.
* Set the hyperparameters and numerical parameters.
* Check if the gradients of the loss function are correct.
* Training model.
* Observe the behavior of weights learned.

### Ipython notebook

{% notebook dnn_sparse_autoencoder_mnist.ipynb %}

### Sparse autoencoder

[gist:id=36efe5fc788fab08a595]

In case you are interested in all codes related in this demonstration, please check the [repository](https://github.com/tsaith/dnn_play).
