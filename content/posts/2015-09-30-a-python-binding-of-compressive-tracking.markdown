Title: A Python binding of Compressive Tracking
Date: 2015-09-30
Tags: cv, python
Category: Machine learning


Recently I read an interesting paper ["Real-time Compressive Tracking"](http://www4.comp.polyu.edu.hk/~cslzhang/CT/eccv_ct_camera.pdf) which applied [compressive sensing](https://en.wikipedia.org/wiki/Compressed_sensing) on object tracking to dramatically reduce the calculations and showed remarkable results.
Kaihua Zhang (the author) kindly had released the source code(both Matlab and C++ versions) of the algorithm on his [webpage](http://www4.comp.polyu.edu.hk/~cslzhang/CT/CT.htm).

### A python binding

Personally I prefer to test algorithms with python,
hence, I have tried to build a python binding of compressive tracking and tested it on my Mac.

Some results are as below:


- Kitesurf

    {% youtube 7fYTloE1KCc %}

- Bolt

    {% youtube XeH4oDwVZj8 %}

and the source code can be found from [this link](https://github.com/tsaith/pyct).

### More details

This section will describe the main steps how I wrapped the C++ version of compressive tracking as the python binding and is not important in the aspect of usage.
In case you are interested in the procedures,
please keep reading.

The class `CompressiveTracker` in `compressive_tracker.cpp` provides two public methods `init(Mat& _frame, Rect& _objectBox)` and `processFrame(Mat& _frame, Rect& _objectBox)`,
where `_frame` and `_objectBox` are the video frame and object box, respectively.

I added two public methods `init_wrap(vector<vector<uint8> > &_frame, vector<int> &_object_box)` and `process_frame_wrap(vector<vector<uint8> > &_frame, vector<int> &_object_box)` to wrap the methods `init` and `processFrame`, which expect `vector` array arguments instead of `Mat` or `Rect` ones.

Next, the cython files `wrap.pxd` and `wrap.pyx` were created to wrap the C++ class `CompressiveTracker` into the Python class `CyCompressiveTracker`.
Besides, `setup.py` was added for compilation.

Finally, `run.py` is the testing code which will load the python binding for object tracking.

Frankly speaking, the existences of `init_wrap` and `process_frame_wrap` come from that I don't know how to use cython to directly convert `numpy` array into `Mat` or `Rect` instances of OpenCv.
I will grateful if someone can show me how to do that : )



