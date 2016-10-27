Title: Derive and implement multiclass SVM layer
Date: 2016-02-14
Tags: cv
Category: Machine learning
Status:

### Loss

Assuming there are $K$ classes,
the loss of multiclass SVM can be written as

$$
J = \sum_{i=1}^{N} J^{(i)} = \frac{1}{N} \sum_{i=1}^{N} \sum_{j \neq y^{(i)}}^K max(0, x_j^{(i)} - x_{y^{(i)}}^{(i)} + \Delta)
$$


where $x_j$ is the score for the $j$th class.
$y$ stands for the correct label.
$\Delta$ is a fixed margin which is usually chosen as one.

### Derivative
$$
\frac{ \partial J^{(i)} }{ \partial x_k } =
\frac{ \partial }{ \partial x_k } \frac{1}{N} \sum_{j \neq y^{(i)}}^K max(0, x_j^{(i)} - x_{y^{(i)}}^{(i)} + \Delta)
$$

Let $D_j^{(i)} = x_j^{(i)} - x_{y^{(i)}}^{(i)} + \Delta$, which represents the score difference (containing a shift of margin) for the $j$th class.

If $k \neq y^{(i)}$,

$$
\frac{ \partial J^{(i)} }{ \partial x_k } =
\left \{
  \begin{aligned}
    1 / N & \text{ when } D_k^{(i)} > 0  \\
    0     & \text{ when } D_k^{(i)} \leq 0
  \end{aligned}
\right.
$$

If $k = y^{(i)}$,

$$
\frac{ \partial J^{(i)} }{ \partial x_k } = - N_p / N
$$
where $N_p$ is the number of positive differences.


### Code example

    #!python
    def svm_loss(x, y):
      """
      Computes the loss and gradient using for multiclass SVM classification.
      x: Input data, of shape (N, K)
      where x[i, j] is the score for the jth class for the ith input.
      y: Vector of labels, of shape (N,)
      where y[i] is the label for x[i] and 0 <= y[i] < K

      Returns
      ----
      loss: Scalar giving the loss
      dx: Gradient of the loss with respect to x
      """

      N = x.shape[0]
      delta = 1.0 # A fixed margin
      correct_scores = x[np.arange(N), y]

      diffs = np.maximum(0, x - correct_scores[:, np.newaxis] + delta)
      diffs[np.arange(N), y] = 0
      loss = np.sum(diffs) / N

      num_pos = np.sum(diffs > 0, axis=1) # Number of positive differences
      dx = np.zeros_like(x)
      dx[diffs > 0] = 1
      dx[np.arange(N), y] -= num_pos
      dx /= N

      return loss, dx
