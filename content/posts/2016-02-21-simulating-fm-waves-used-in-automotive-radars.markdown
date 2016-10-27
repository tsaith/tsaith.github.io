Title: Simulating FM waves used in automotive radars
Date: 2016-02-21
Tags: radar
Category: Signal processing
Status:

Let's express the wave function as

$$
y(t) = A cos(\phi(t) + \phi_0)
$$

where $A$ is the wave amplitude.
$\phi(t) = 2\pi \int_0^{t} f(t') dt'$ is the time-dependent phase angle.
$f(t')$ stands for the instantaneous frequency varying with time.
$\phi_0$ means the initial phase.

From the above equation, we know that the role of $f(t')$ is to determine how the sinusoidal waves are modulated in frequency domain.

The following code example will demonstrate waves with different frequency-modulation.

### Code example

{% notebook simulating_fm_waves_used_in_automotive_radars.ipynb %}
