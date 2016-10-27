Title: Detect peaks with CFAR algorithm
Date: 2016-03-15
Tags: radar
Category: Signal processing
Status:

In this post, we will introduce the cell-averaging [CFAR](https://en.wikipedia.org/wiki/Constant_false_alarm_rate)(Constant False Alarm) algorithm to detect peaks of signals.

### Theory

{% img https://farm2.staticflickr.com/1652/25170561054_2e4c18a434_z.jpg %}

[[This picture is copied from Matlab doc]](http://www.mathworks.com/help/phased/examples/constant-false-alarm-rate-cfar-detection.html)

In this figure, the CUT (Cell Under Test) is to be tested if its value is greater than threshold level or not.
The threshold level is calculated from the estimated noise power of the training cells.
The guard cells are used to avoid corrupting this estimate with power from the CUT itself,
cells immediately adjacent to the CUT are normally ignored.

Assuming $x_j$ is the value of the $j$th test cell,
we declare that the test cell has a peak if
$x_j$ is greater than the value of adjacent cells and
$x_j > T$, where T is the threshold.

$$
T = \alpha P_n
$$

$$
\alpha = N (P_{fa}^{-1/N} - 1)
$$

$$
P_n = \frac{1}{N} \sum_{m=1}^{N} x_m
$$

where $\alpha$ is the threshold factor,
$P_n$ stands for the noise power of training cells,
$N$ is the number of training cells and
$P_{fa}$ means the false alarm rate.

Form the equations above,
we can observe that lower false alarm rate will lead to higher threshold level.

### Code example

This example demonstrates how to implement cell-averaging CFAR with python.

{% notebook cfar.ipynb %}

---
References

[1] [Constant false alarm rate](https://en.wikipedia.org/wiki/Constant_false_alarm_rate)

[2] [Constant False Alarm Rate (CFAR) Detection](http://www.mathworks.com/help/phased/examples/constant-false-alarm-rate-cfar-detection.html)
