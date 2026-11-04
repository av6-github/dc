import numpy as np
from tensorflow.keras.datasets import mnist


# 1. LOAD MNIST DATASET
(X_train, y_train), (X_test, y_test) = mnist.load_data()


# 2. SELECT DIGITS
digits = [0, 3, 6, 9]

mask = np.isin(y_train, digits)

X = X_train[mask]
y = y_train[mask]


# 3. BINARY ENCODING
X_binary = np.where(X > 127, 1, -1)


# 4. SELECT ONE PATTERN PER DIGIT
patterns = []
labels = []

for digit in digits:
    for i in range(len(X)):
        if y[i] == digit:
            patterns.append(X_binary[i].flatten())
            labels.append(y[i])
            break

patterns = np.array(patterns)
labels = np.array(labels)


# 5. HEBBIAN LEARNING
n = patterns.shape[1]

W = np.zeros((n, n))

for pattern in patterns:
    W += np.outer(pattern, pattern)

W = W / n

np.fill_diagonal(W, 0)


# 6. ADD NOISE
def add_noise(pattern, noise_level=0.20):

    noisy = pattern.copy()

    number_of_pixels = int(noise_level * len(pattern))

    pixels = np.random.choice(
        len(pattern),
        number_of_pixels,
        replace=False
    )

    noisy[pixels] *= -1

    return noisy


# 7. RECALL STORED PATTERN
def recall(pattern, W, iterations=10):

    state = pattern.copy()

    for _ in range(iterations):

        for i in range(len(state)):

            value = np.dot(W[i], state)

            if value >= 0:
                state[i] = 1
            else:
                state[i] = -1

    return state


# 8. TEST SINGLE PATTERN
original = patterns[0]

noisy = add_noise(original, 0.20)

recalled = recall(noisy, W)

accuracy = np.mean(original == recalled)

print("Single Pattern Recall Accuracy:", accuracy * 100, "%")


# 9. TEST ALL STORED PATTERNS
def predict_digit(recalled):

    similarities = []

    for pattern in patterns:

        similarity = np.mean(recalled == pattern)

        similarities.append(similarity)

    predicted_index = np.argmax(similarities)

    return labels[predicted_index]


correct = 0

for i in range(len(patterns)):

    original = patterns[i]

    noisy = add_noise(original, 0.20)

    recalled = recall(noisy, W)

    predicted_digit = predict_digit(recalled)

    if predicted_digit == labels[i]:
        correct += 1


print("Correctly recalled:", correct)
print("Total patterns:", len(patterns))

print("Recall Accuracy:", correct / len(patterns) * 100, "%")


# 10. TEST DIFFERENT NOISE LEVELS
noise_levels = [0.10, 0.20, 0.30, 0.40, 0.50]

tests_per_digit = 20

for noise in noise_levels:

    correct = 0
    total = 0

    for i in range(len(patterns)):

        for _ in range(tests_per_digit):

            original = patterns[i]

            noisy = add_noise(original, noise)

            recalled = recall(noisy, W)

            predicted_digit = predict_digit(recalled)

            if predicted_digit == labels[i]:
                correct += 1

            total += 1

    accuracy = correct / total

    print("\nNoise:", noise * 100, "%")
    print("Correct:", correct)
    print("Total:", total)
    print("Recall Accuracy:", accuracy * 100, "%")


print("\nHopfield Network Implementation Completed")