Title: Install OpenCV 3 for Python 3 on OSX
Date: 2015-08-31
Tags: cv
Category: Machine learning


First, install OpenCV 3 with homebrew as
```
brew install opencv3 --with-python3 --with-contrib
```
with `--with-contrib` flag,
[opencv_contrib](https://github.com/itseez/opencv_contrib) packages containing algorithms that are either patented or in experimental development will also be installed.

Second, set the environment variable `PYTHONPATH` to include the path of `cv2.so` which is a python binding to OpenCV.

There are several ways to set `PYTHONPATH`, one way is to add the following line to `~/.profile`.

```
export PYTHONPATH=$PYTHONPATH:/usr/local/Cellar/opencv3/3.0.0/lib/python3.4/site-packages
```
Please note that the name of python directry depends on which python version you use, in my case is `python3.4`.

Be sure to execute `source ~/.profile` or restart your terminal to update `PYTHONPATH`.

Now, let's check if our python 3 can import the module of OpenCV in the terminal.
```
$ python3
Python 3.4.3 (default, Jun 10 2015, 19:57:30)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__
'3.0.0'
```


