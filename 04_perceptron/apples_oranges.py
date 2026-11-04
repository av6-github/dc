import numpy as np

# APPLE = 1
# ORANGE = 0

# Features:
# Shape:   Round = 1, Elliptical = 0
# Texture: Smooth = 1, Rough = 0
# Weight:  Heavy = 1, Light = 0


# Training Dataset
X = np.repeat(np.array([
    [1, 1, 1],  # Apple
    [1, 1, 0],  # Apple
    [1, 0, 1],  # Apple
    [0, 1, 1],  # Apple

    [0, 0, 0],  # Orange
    [0, 0, 1],  # Orange
    [0, 1, 0],  # Orange
    [1, 0, 0]   # Orange
]), 3, axis=0)

target = np.array(
    [1]*12 + [0]*12
)


# Binary Step Activation Function
def binary_step(x):
    return 1 if x >= 0 else 0


# Initialize weights and bias
w1 = 1
w2 = 1
w3 = 1

b = -1

alpha = 1


# TRAINING
for epoch in range(10):

    print("\nEpoch:", epoch + 1)

    error_count = 0

    for i in range(len(X)):

        x1 = X[i][0]
        x2 = X[i][1]
        x3 = X[i][2]

        # Weighted sum
        net = x1*w1 + x2*w2 + x3*w3 + b

        # Prediction
        output = binary_step(net)

        # Calculate error
        error = target[i] - output

        print("Input:", x1, x2, x3,
              "Output:", output,
              "Error:", error)

        # Update weights
        w1 = w1 + alpha * error * x1
        w2 = w2 + alpha * error * x2
        w3 = w3 + alpha * error * x3

        # Update bias
        b = b + alpha * error

        if error != 0:
            error_count += 1

    print("Weights:", w1, w2, w3)
    print("Bias:", b)

    # Check convergence
    if error_count == 0:
        print("Model converged")
        break


# TESTING ON TRAINING DATA
print("\nTraining Data Predictions:")

for i in range(len(X)):

    net = X[i][0]*w1 + X[i][1]*w2 + X[i][2]*w3 + b

    output = binary_step(net)

    print("Input:", X[i],
          "Actual:", target[i],
          "Predicted:", output)


# UNSEEN TEST DATA
X_test = np.array([
    [1, 1, 1],
    [0, 0, 0],
    [1, 0, 1],
    [0, 1, 0]
])

# Actual labels
y_test = np.array([1, 0, 1, 0])


# TESTING
print("\nTesting on Unseen Data:")

for i in range(len(X_test)):

    net = (X_test[i][0]*w1 +
           X_test[i][1]*w2 +
           X_test[i][2]*w3 + b)

    output = binary_step(net)

    if output == 1:
        fruit = "Apple"
    else:
        fruit = "Orange"

    print("Input:", X_test[i],
          "Actual:", y_test[i],
          "Predicted:", output,
          "Fruit:", fruit)