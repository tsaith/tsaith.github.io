Title: Derive and implement softmax layer
Date: 2016-02-14
Tags: cv
Category: Machine learning
Status:

### Loss

Assuming there are $K$ classes,
the loss of softmax can be written as

$$
J = \sum_{i=1}^{N} J^{(i)} = -\frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{K} t_j^{(i)} \ln P_j^{(i)}
$$

where

$$
t_j = 1 \{ y = j \} =
\left \{
\begin{aligned}
  1 \quad \text{for} \quad y = j     \\
  0 \quad \text{for} \quad y \neq j
\end{aligned}
\right.
$$

$$
P_j = \frac{ e^{x_j} }{ \sum_{l=1}^{K} e^{x_l}} \quad \text{the probability for the } j \text {th class.}
$$

$x_j$ is the score for the $j$th class;
$y$ stands for the correct class label.

### Derivative

$$
\frac{ \partial J^{(i)} }{ \partial x_k } =
-\frac{1}{N} \sum_{j=1}^{K} t_j^{(i)} \frac{ \partial }{ \partial x_k } \ln P_j^{(i)} =
\frac{1}{N} ( P_k^{(i)} - t_k^{(i)} )
$$


### Numerical trick

To avoid the numerical problem when the numerator/denominator of $P_j$ is too large,
we prefer to calculate $P_j$ as follows.

$$
P_j = \frac{ e^{x_j} }{ \sum_{l=1}^{K} e^{x_l}}
= \frac{ e^{x_j - x_{\text{max}}} }{ \sum_{l=1}^{K} e^{x_l - x_{\text{max}}}}
$$

$$
x_{\text{max}} = max(x)
$$

### Code example

    #!python
    def softmax_loss(x, y):
      """
      Computes the loss and gradient for softmax classification.
      x: Input data, of shape (N, K)
         where x[i, j] is the score for the jth class
         for the ith input.
      y: Vector of labels, of shape (N,)
         where y[i] is the label for x[i] and 0 <= y[i] < K

      Returns
      ----
      loss: Scalar giving the loss
      dx: Gradient of the loss with respect to x
      """
      N = x.shape[0]
      x_max = np.max(x, axis=1, keepdims=True)
      proba = np.exp(x - x_max)
      proba /= np.sum(proba, axis=1, keepdims=True)
      loss = -np.sum(np.log(proba[range(N), y])) / N
      dx = proba.copy()
      dx[range(N), y] -= 1
      dx /= N

      return loss, dx
