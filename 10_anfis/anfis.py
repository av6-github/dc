import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from itertools import product
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load dataset
data = pd.read_csv("energy.csv")

inputs = ["Temperature", "Humidity", "Occupancy", "Appliances", "HourOfDay"]
target = "EnergyConsumption"

data = data[inputs + [target]].apply(pd.to_numeric, errors="coerce").dropna()

X = data[inputs].values.astype(np.float32)
y = data[target].values.astype(np.float32).reshape(-1, 1)

# Split and scale
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)

# ANFIS Model
class ANFIS(nn.Module):

    def __init__(self, n_inputs=5, n_mfs=2):
        super().__init__()

        self.n_inputs = n_inputs
        self.n_mfs = n_mfs

        self.centers = nn.Parameter(
            torch.tensor([-0.7, 0.7]).repeat(n_inputs, 1)
        )

        self.log_sigmas = nn.Parameter(
            torch.full((n_inputs, n_mfs), np.log(0.9))
        )

        self.rules = torch.tensor(
            list(product(range(n_mfs), repeat=n_inputs))
        )

        self.n_rules = len(self.rules)

    # Layer 1: Gaussian membership functions
    def membership(self, x):
        sigma = torch.exp(self.log_sigmas) + 1e-6

        return torch.exp(
            -0.5 * ((x.unsqueeze(2) - self.centers) / sigma) ** 2
        )

    # Layer 2 and 3: Firing strengths and normalization
    def design_matrix(self, x):
        m = self.membership(x)

        selected = m[:, torch.arange(self.n_inputs), self.rules]
        firing = torch.prod(selected, dim=2)

        normalized = firing / (firing.sum(dim=1, keepdim=True) + 1e-8)

        # Layer 4: Linear Sugeno consequents
        x = torch.cat([x, torch.ones(x.shape[0], 1)], dim=1)

        return (normalized.unsqueeze(2) * x.unsqueeze(1)).reshape(
            x.shape[0], -1
        )

    # Layer 5: Final output
    def forward(self, x, consequent):
        return self.design_matrix(x) @ consequent


model = ANFIS()

optimizer = torch.optim.Adam(
    [model.centers, model.log_sigmas], lr=0.003
)

# Hybrid Learning: Least Squares + Gradient Descent
for epoch in range(250):

    # Step 1: Least Squares estimates consequent parameters
    with torch.no_grad():
        A = model.design_matrix(X_train).numpy()

    consequent = np.linalg.lstsq(A, y_train.numpy(), rcond=None)[0]
    consequent = torch.tensor(consequent, dtype=torch.float32)

    # Step 2: Gradient Descent updates membership parameters
    optimizer.zero_grad()

    prediction = model(X_train, consequent)
    loss = torch.mean((prediction - y_train) ** 2)

    loss.backward()
    optimizer.step()

    if (epoch + 1) % 50 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# Testing
with torch.no_grad():
    A_test = model.design_matrix(X_test)
    y_pred = (A_test @ consequent).numpy().flatten()

y_actual = y_test.flatten()

print("\nANFIS Evaluation")
print("RMSE:", np.sqrt(mean_squared_error(y_actual, y_pred)))
print("MAE:", mean_absolute_error(y_actual, y_pred))
print("R2 Score:", r2_score(y_actual, y_pred))

print("\nNumber of Rules:", model.n_rules)
print("Membership Function Centers:\n", model.centers.detach().numpy())
print("Membership Function Widths:\n", torch.exp(model.log_sigmas).detach().numpy())