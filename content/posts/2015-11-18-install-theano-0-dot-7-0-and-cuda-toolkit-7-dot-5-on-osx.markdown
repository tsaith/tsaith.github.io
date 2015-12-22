Title: Install Theano and CUDA Toolkit 7.5 on OSX
Date: 2015-11-18
Tags: python
Category: Machine learning


This post describes the steps I used to install [Theano](http://deeplearning.net/software/theano/tutorial/) on my Mac (OSX 10.9.5) with NVIDIA GeForce GTX 660M graphics card.

### Install Theano

Please use `pip` to install Theano as below
```
$ pip install Theano
```

Then, create the `~/.theanorc` with content as
```
[global]
mode=FAST_RUN
floatX = float32
device = gpu

[nvcc]
fastmath = True
```

### Install CUDA Toolkit

Download the package of CUDA Toolkit 7.5 from the official [link](https://developer.nvidia.com/cuda-downloads).

### Install cuDNN

Next, we have to register on NVIDIA to be able to download [cuDNN](https://developer.nvidia.com/cudnn),
which is a GPU-accelerated library of primitives for deep neural networks.

After downloading,
please uncompress the package and copy the header file and libraries to `include` and `lib` under the root directory of CUDA Toolkit (e.g. /usr/local/cuda), respectively.
```
$ tar xzf cudnn-7.0-osx-x64-v3.0-prod.tgz
$ cd cuda
$ sudo cp include/cudnn.h /usr/local/cuda/include/
$ sudo cp lib/libcudnn* /usr/local/cuda/lib/
```

### Add environment variables

Add the following environment variables to `~/.bash_profile`.

```
# Theano
export CUDA_ROOT="/usr/local/cuda"
export THEANO_FLAGS="mode=FAST_RUN,device=gpu,floatX=float32"

# CUDA
export LD_LIBRARY_PATH="$CUDA_ROOT/lib:$LD_LIBRARY_PATH"
export PATH="$CUDA_ROOT/bin:$PATH"
```

You may want to execute `source ~/.bash_profile` to validate the settings right away.

### Testing

Now, we can run a test code to see if the Theano works as expected.

{% codeblock test.py %}
from theano import function, config, shared, sandbox
import theano.tensor as T
import numpy
import time

vlen = 10 * 30 * 768  # 10 x #cores x # threads per core
iters = 1000

rng = numpy.random.RandomState(22)
x = shared(numpy.asarray(rng.rand(vlen), config.floatX))
f = function([], T.exp(x))
print(f.maker.fgraph.toposort())
t0 = time.time()
for i in range(iters):
    r = f()
t1 = time.time()
print("Looping %d times took %f seconds" % (iters, t1 - t0))
print("Result is %s" % (r,))
if numpy.any([isinstance(x.op, T.Elemwise) for x in f.maker.fgraph.toposort()]):
    print('Used the cpu')
else:
    print('Used the gpu')
{% endcodeblock %}

Let's run this code on CPU and GPU, separately.

CPU case:
```
$ THEANO_FLAGS='device=cpu' python test.py
[Elemwise{exp,no_inplace}(<TensorType(float32, vector)>)]
Looping 1000 times took 14.474722 seconds
Result is [ 1.23178029  1.61879337  1.52278066 ...,  2.20771813  2.29967761
  1.62323284]
Used the cpu
```

GPU case:
```
$ THEANO_FLAGS='device=gpu' python test.py
Using gpu device 0: GeForce GTX 660M (CNMeM is disabled)
[GpuElemwise{exp,no_inplace}(<CudaNdarrayType(float32, vector)>), HostFromGpu(GpuElemwise{exp,no_inplace}.0)]
Looping 1000 times took 0.517552 seconds
Result is [ 1.23178029  1.61879349  1.52278066 ...,  2.20771813  2.29967761
  1.62323296]
Used the gpu
```
Please note that Theano will have to compile the python code to generate C++/CUDA code when executing with GPU for the first time. Thus, the results shown above came from the execution of the second time.

Finally, it can be observed that the runtime is greatly reduced when GPU is used : )


