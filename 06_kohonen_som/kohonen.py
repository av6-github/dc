import numpy as np
import pandas as pd

from minisom import MiniSom
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score


# 1. LOAD DATASET
df = pd.read_csv("Heart_failure_clinical_records_dataset.csv")


# 2. SEPARATE FEATURES AND TARGET
X = df.drop("DEATH_EVENT", axis=1)
y = df["DEATH_EVENT"]


# 3. HANDLE MISSING VALUES
X = X.fillna(X.median())


# 4. FEATURE SCALING
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# 5. INITIALIZE SOM
som = MiniSom(
    x=10, y=10,
    input_len=X_scaled.shape[1],
    sigma=1.5,
    learning_rate=0.5,
    random_seed=42
)

som.random_weights_init(X_scaled)


# 6. TRAIN SOM
som.train_random(X_scaled, 20000)


# 7. FIND BEST MATCHING UNITS (BMU)
bmu_coordinates = np.array([
    som.winner(sample) for sample in X_scaled
])


# 8. GROUP PATIENTS BY WINNING NEURON
neuron_patients = {}

for i, bmu in enumerate(bmu_coordinates):
    neuron = tuple(bmu)
    neuron_patients.setdefault(neuron, []).append(i)

occupied_neurons = list(neuron_patients.keys())


# 9. EXTRACT WEIGHTS OF OCCUPIED NEURONS
weights = np.array([
    som.get_weights()[r, c] for r, c in occupied_neurons
])


# 10. APPLY K-MEANS CLUSTERING
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
neuron_clusters = kmeans.fit_predict(weights)


# 11. MAP NEURONS TO CLUSTERS
neuron_to_cluster = dict(zip(occupied_neurons, neuron_clusters))


# 12. ASSIGN CLUSTERS TO PATIENTS
patient_clusters = np.array([
    neuron_to_cluster[tuple(bmu)] for bmu in bmu_coordinates
])

df["SOM_CLUSTER"] = patient_clusters


# 13. COMPARE CLUSTERS WITH DEATH EVENTS
print("\nCluster vs Death Events:")
print(pd.crosstab(df["SOM_CLUSTER"], df["DEATH_EVENT"]))


# 14. CALCULATE CLUSTER RISK
cluster_risk = df.groupby("SOM_CLUSTER")["DEATH_EVENT"].agg(
    Patients="count",
    Deaths="sum",
    Death_Rate="mean"
)

cluster_risk["Death_Rate"] *= 100

print("\nCluster Risk Profile:")
print(cluster_risk)


# 15. EVALUATE CLUSTERING
print("\nSilhouette Score:",
      silhouette_score(X_scaled, patient_clusters))

print("Davies-Bouldin Index:",
      davies_bouldin_score(X_scaled, patient_clusters))


# 16. FINAL RESULTS
print("\n========== SOM RESULTS ==========")

print("Number of patients:", len(df))
print("Number of features:", X.shape[1])
print("SOM Grid: 10 x 10")
print("Occupied neurons:", len(occupied_neurons))
print("Number of clusters:", len(np.unique(patient_clusters)))

print("\nPatients in each cluster:")
print(df["SOM_CLUSTER"].value_counts().sort_index())