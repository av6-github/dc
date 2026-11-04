import numpy as np


# 1. BILINGUAL DICTIONARY
data = {
    "love": "प्यार",
    "pain": "दर्द",
    "emotion": "भावना",
    "dichotomy": "विरोधाभास",
    "hate": "नफरत",
    "happiness": "खुशी",
    "sadness": "उदासी",
    "joy": "आनंद",
    "jealousy": "ईर्ष्या",
    "victory": "विजय"
}


# 2. TEXT TO BINARY
def text_to_binary(text, max_length):

    binary = []

    for byte in text.encode("utf-8"):
        binary.extend([int(x) for x in format(byte, "08b")])

    binary = binary[:max_length]

    while len(binary) < max_length:
        binary.append(0)

    return np.array(binary)


# 3. FIND MAXIMUM VECTOR LENGTHS
max_eng_length = max(
    len(word.encode("utf-8")) * 8 for word in data.keys()
)

max_hindi_length = max(
    len(word.encode("utf-8")) * 8 for word in data.values()
)


# 4. ENCODE WORDS
english_vectors = {}
hindi_vectors = {}

for eng, hindi in data.items():

    english_vectors[eng] = text_to_binary(eng, max_eng_length)

    hindi_vectors[hindi] = text_to_binary(hindi, max_hindi_length)


# 5. BINARY TO BIPOLAR
def binary_to_bipolar(vector):

    return np.where(vector == 0, -1, 1)


english_bipolar = {}
hindi_bipolar = {}

for eng, hindi in data.items():

    english_bipolar[eng] = binary_to_bipolar(english_vectors[eng])

    hindi_bipolar[hindi] = binary_to_bipolar(hindi_vectors[hindi])


# 6. INITIALIZE WEIGHT MATRIX
W = np.zeros((max_eng_length, max_hindi_length))


# 7. HEBBIAN LEARNING
for eng, hindi in data.items():

    X = english_bipolar[eng]

    Y = hindi_bipolar[hindi]

    W += np.outer(X, Y)


print("Training completed.")
print("Weight Matrix Shape:", W.shape)


# 8. BIPOLAR TO BINARY
def bipolar_to_binary(vector):

    return np.where(vector == -1, 0, 1)


# 9. FORWARD RECALL: ENGLISH TO HINDI
def recall_hindi(english_word):

    X = english_bipolar[english_word]

    Y = np.dot(X, W)

    Y = np.where(Y >= 0, 1, -1)

    return Y


# 10. FIND CLOSEST HINDI WORD
def find_hindi_translation(recalled_vector):

    recalled_binary = bipolar_to_binary(recalled_vector)

    best_word = None
    best_score = -1

    for hindi, vector in hindi_vectors.items():

        score = np.sum(recalled_binary == vector)

        if score > best_score:

            best_score = score

            best_word = hindi

    return best_word


# 11. BACKWARD RECALL: HINDI TO ENGLISH
def recall_english(hindi_word):

    Y = hindi_bipolar[hindi_word]

    X = np.dot(Y, W.T)

    X = np.where(X >= 0, 1, -1)

    return X


# 12. FIND CLOSEST ENGLISH WORD
def find_english_translation(recalled_vector):

    recalled_binary = bipolar_to_binary(recalled_vector)

    best_word = None
    best_score = -1

    for eng, vector in english_vectors.items():

        score = np.sum(recalled_binary == vector)

        if score > best_score:

            best_score = score

            best_word = eng

    return best_word


# 13. TEST FORWARD RECALL
for eng, hindi in data.items():

    recalled = recall_hindi(eng)

    result = find_hindi_translation(recalled)

    print("English:", eng)
    print("Expected:", hindi)
    print("Recalled:", result)


# 14. TEST BACKWARD RECALL
for eng, hindi in data.items():

    recalled = recall_english(hindi)

    result = find_english_translation(recalled)

    print("Hindi:", hindi)
    print("Expected:", eng)
    print("Recalled:", result)


# 15. CALCULATE ACCURACY
correct_forward = 0
correct_backward = 0

for eng, hindi in data.items():

    if find_hindi_translation(recall_hindi(eng)) == hindi:
        correct_forward += 1

    if find_english_translation(recall_english(hindi)) == eng:
        correct_backward += 1


print("\nEnglish to Hindi Accuracy:",
      correct_forward / len(data) * 100, "%")

print("Hindi to English Accuracy:",
      correct_backward / len(data) * 100, "%")


# 16. ADD NOISE
def add_noise(vector, noise_percent):

    noisy_vector = vector.copy()

    number_of_bits = len(vector)

    number_of_noisy_bits = int(
        number_of_bits * noise_percent / 100
    )

    positions = np.random.choice(
        number_of_bits,
        number_of_noisy_bits,
        replace=False
    )

    noisy_vector[positions] = 1 - noisy_vector[positions]

    return noisy_vector


# 17. TEST ROBUSTNESS AT DIFFERENT NOISE LEVELS
noise_levels = [0, 10, 20, 30, 40]

trials = 10

for noise in noise_levels:

    correct = 0
    total = 0

    for _ in range(trials):

        for eng, hindi in data.items():

            original = english_vectors[eng]

            noisy = add_noise(original, noise)

            noisy_bipolar = binary_to_bipolar(noisy)

            recalled = np.dot(noisy_bipolar, W)

            recalled = np.where(recalled >= 0, 1, -1)

            result = find_hindi_translation(recalled)

            if result == hindi:
                correct += 1

            total += 1

    print("\nNoise:", noise, "%")

    print("Robustness Accuracy:", correct / total * 100, "%")


# 18. TEST SYNONYMS
synonyms = {
    "affection": "प्यार",
    "suffering": "दर्द",
    "feeling": "भावना",
    "antipathy": "नफरत",
    "gladness": "खुशी",
    "sorrow": "उदासी",
    "delight": "आनंद",
    "envy": "ईर्ष्या",
    "triumph": "विजय"
}

correct = 0

for word, expected_hindi in synonyms.items():

    X = text_to_binary(word, max_eng_length)

    X = binary_to_bipolar(X)

    Y = np.dot(X, W)

    Y = np.where(Y >= 0, 1, -1)

    result = find_hindi_translation(Y)

    print("\nSynonym:", word)
    print("Expected:", expected_hindi)
    print("Recalled:", result)

    if result == expected_hindi:
        correct += 1


print("\nSynonym Accuracy:",
      correct / len(synonyms) * 100, "%")


# 19. ONE-BIT ERROR TESTING
def add_one_bit_error(vector):

    noisy_vector = vector.copy()

    position = np.random.randint(0, len(vector))

    noisy_vector[position] = 1 - noisy_vector[position]

    return noisy_vector


trials = 100

forward_correct = 0
backward_correct = 0

forward_total = 0
backward_total = 0


for _ in range(trials):

    # Forward: English to Hindi
    for eng, hindi in data.items():

        noisy = add_one_bit_error(english_vectors[eng])

        noisy = binary_to_bipolar(noisy)

        Y = np.dot(noisy, W)

        Y = np.where(Y >= 0, 1, -1)

        result = find_hindi_translation(Y)

        if result == hindi:
            forward_correct += 1

        forward_total += 1

    # Backward: Hindi to English
    for eng, hindi in data.items():

        noisy = add_one_bit_error(hindi_vectors[hindi])

        noisy = binary_to_bipolar(noisy)

        X = np.dot(noisy, W.T)

        X = np.where(X >= 0, 1, -1)

        result = find_english_translation(X)

        if result == eng:
            backward_correct += 1

        backward_total += 1


print("\nONE-BIT ERROR ROBUSTNESS")

print("Forward Accuracy:",
      forward_correct / forward_total * 100, "%")

print("Backward Accuracy:",
      backward_correct / backward_total * 100, "%")


print("\nBAM Implementation Completed")