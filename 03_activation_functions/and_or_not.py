import numpy as np

# Binary Step Activation
def step(x):
    return 1 if x >= 0 else 0


# Perceptron Training
def train(X, target):
    w = np.zeros(X.shape[1])
    b = 0

    for epoch in range(100):
        errors = 0

        for x, t in zip(X, target):
            output = step(np.dot(x, w) + b)
            error = t - output

            w += error * x
            b += error
            errors += error != 0

        if errors == 0:
            break

    return w, b


# Testing
def test(X, target, w, b, name):
    print("\n", name)

    for x, t in zip(X, target):
        output = step(np.dot(x, w) + b)
        print(x, "Actual:", t, "Predicted:", output)


# Input combinations
X = np.array([[0,0], [0,1], [1,0], [1,1]])

# AND GATE
and_target = np.array([0,0,0,1])
w_and, b_and = train(X, and_target)
test(X, and_target, w_and, b_and, "AND GATE")


# OR GATE
or_target = np.array([0,1,1,1])
w_or, b_or = train(X, or_target)
test(X, or_target, w_or, b_or, "OR GATE")


# NOT GATE
X_not = np.array([[0], [1]])
not_target = np.array([1,0])

w_not, b_not = train(X_not, not_target)
test(X_not, not_target, w_not, b_not, "NOT GATE")


# XOR GATE USING MULTI-LAYER PERCEPTRON

x1 = X[:, 0]
x2 = X[:, 1]

# NOT outputs
x1_bar = np.array([step(x*w_not[0] + b_not) for x in x1])
x2_bar = np.array([step(x*w_not[0] + b_not) for x in x2])

# Hidden Layer 1: X1 AND NOT X2
z1_input = np.column_stack((x1, x2_bar))
z1_target = np.array([0,0,1,0])

w1, b1 = train(z1_input, z1_target)

# Hidden Layer 2: NOT X1 AND X2
z2_input = np.column_stack((x1_bar, x2))
z2_target = np.array([0,1,0,0])

w2, b2 = train(z2_input, z2_target)

# Hidden layer outputs
z1 = np.array([step(x @ w1 + b1) for x in z1_input])
z2 = np.array([step(x @ w2 + b2) for x in z2_input])

# Output Layer: OR
Z = np.column_stack((z1, z2))
xor_target = np.array([0,1,1,0])

w_xor, b_xor = train(Z, xor_target)

# Final XOR Testing
test(Z, xor_target, w_xor, b_xor, "XOR GATE")