import numpy as np
import pandas as pd


# 1. UNIVERSE OF DISCOURSE
aqi = np.linspace(0, 500, 501)


# 2. TRAPEZOIDAL MEMBERSHIP FUNCTION
def trapezoidal_mf(x, a, b, c, d):

    x = np.asarray(x, dtype=float)

    membership = np.zeros_like(x)

    if b > a:
        mask = (x > a) & (x < b)

        membership[mask] = (x[mask] - a) / (b - a)

    mask = (x >= b) & (x <= c)

    membership[mask] = 1.0

    if d > c:
        mask = (x > c) & (x < d)

        membership[mask] = (d - x[mask]) / (d - c)

    return membership


# 3. DEFINE FUZZY AQI SETS

G = trapezoidal_mf(aqi, 0, 0, 30, 60)

M = trapezoidal_mf(aqi, 30, 70, 120, 170)

P = trapezoidal_mf(aqi, 100, 160, 220, 280)

S = trapezoidal_mf(aqi, 180, 250, 500, 500)


# 4. TEST AQI VALUES

sample_aqi = [40, 120, 250]

results = []

for value in sample_aqi:

    g = trapezoidal_mf([value], 0, 0, 30, 60)[0]

    m = trapezoidal_mf([value], 30, 70, 120, 170)[0]

    p = trapezoidal_mf([value], 100, 160, 220, 280)[0]

    s = trapezoidal_mf([value], 180, 250, 500, 500)[0]

    results.append([value, g, m, p, s])


aqi_table = pd.DataFrame(
    results,
    columns=["AQI", "Good", "Moderate", "Poor", "Severe"]
)

print("\nAQI MEMBERSHIP VALUES")
print(aqi_table)


# 5. DEFINE HEALTH EFFECT SETS

health_labels = [
    "Healthy",
    "Mild Symptoms",
    "Serious Symptoms"
]

H = np.array([1.0, 0.0, 0.0])

MS = np.array([0.0, 1.0, 0.0])

SS = np.array([0.0, 0.0, 1.0])


# 6. FUZZY HEALTH PROFILE

B = np.array([1.0, 0.6, 0.2])

print("\nHEALTH MEMBERSHIP VALUES")

for label, value in zip(health_labels, B):

    print(label, ":", value)


# 7. FUZZY OPERATIONS

fuzzy_union = np.maximum(G, M)

fuzzy_intersection = np.minimum(G, M)

bounded_sum = np.minimum(G + M, 1)

bounded_difference = np.maximum(G - M, 0)


print("\nFUZZY OPERATIONS COMPLETED")


# 8. DEFINE SET A

A = np.array([1.0, 0.7, 0.3, 0.0])

A_labels = ["Good", "Moderate", "Poor", "Severe"]


# 9. DEFINE SET B

B = np.array([1.0, 0.6, 0.2])

B_labels = [
    "Healthy",
    "Mild Symptoms",
    "Serious Symptoms"
]


# 10. FUZZY CARTESIAN PRODUCT

cartesian_product = np.zeros((len(A), len(B)))

for i in range(len(A)):

    for j in range(len(B)):

        cartesian_product[i, j] = min(A[i], B[j])


print("\nFUZZY CARTESIAN PRODUCT")

print(pd.DataFrame(
    cartesian_product,
    index=A_labels,
    columns=B_labels
))


# 11. FUZZY RELATION MATRIX

R = np.array([

    [1.0, 0.1, 0.0],

    [0.4, 1.0, 0.2],

    [0.1, 0.8, 0.8],

    [0.0, 0.3, 1.0]

])


print("\nFUZZY RELATION MATRIX")

print(pd.DataFrame(
    R,
    index=A_labels,
    columns=B_labels
))


# 12. DESIRED HEALTH CONDITION

C = np.array([1.0, 0.5, 0.0])


# 13. MAX-MIN COMPOSITION

def max_min_composition(C, R):

    result = np.zeros(R.shape[0])

    for i in range(R.shape[0]):

        values = []

        for j in range(R.shape[1]):

            value = min(C[j], R[i, j])

            values.append(value)

        result[i] = max(values)

    return result


max_min_result = max_min_composition(C, R)


# 14. MAX-PRODUCT COMPOSITION

def max_product_composition(C, R):

    result = np.zeros(R.shape[0])

    for i in range(R.shape[0]):

        values = []

        for j in range(R.shape[1]):

            value = C[j] * R[i, j]

            values.append(value)

        result[i] = max(values)

    return result


max_product_result = max_product_composition(C, R)


# 15. COMPARE COMPOSITIONS

comparison = pd.DataFrame({

    "AQI Category": A_labels,

    "Max-Min": max_min_result,

    "Max-Product": max_product_result

})

print("\nCOMPOSITION COMPARISON")

print(comparison)


# 16. FUNCTION TO GET AQI MEMBERSHIPS

def get_aqi_memberships(value):

    return {

        "Good": float(trapezoidal_mf(
            [value], 0, 0, 30, 60
        )[0]),

        "Moderate": float(trapezoidal_mf(
            [value], 30, 70, 120, 170
        )[0]),

        "Poor": float(trapezoidal_mf(
            [value], 100, 160, 220, 280
        )[0]),

        "Severe": float(trapezoidal_mf(
            [value], 180, 250, 500, 500
        )[0])

    }


# 17. TEST AQI VALUES

test_values = [40, 120, 250]

health_interpretation = {

    "Good": "Mostly Healthy",

    "Moderate": "Mild Symptoms",

    "Poor": "Mild to Serious Symptoms",

    "Severe": "Likely Serious Symptoms"

}


print("\nAQI HEALTH ANALYSIS")

for value in test_values:

    memberships = get_aqi_memberships(value)

    dominant_category = max(
        memberships,
        key=memberships.get
    )

    interpretation = health_interpretation[
        dominant_category
    ]

    print("\nAQI:", value)

    print("Memberships:", memberships)

    print("Dominant Category:", dominant_category)

    print("Health Effect:", interpretation)


print("\nEXPERIMENT COMPLETED SUCCESSFULLY")