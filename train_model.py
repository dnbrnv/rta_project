import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

from ucimlrepo import fetch_ucirepo
from sklearn.linear_model import LinearRegression
import pandas as pd
import joblib

# Load dataset from UCI
dataset = fetch_ucirepo(id=374)

# Input: external conditions
X = dataset.data.features[['T_out', 'RH_out', 'Windspeed']]

# Target: average indoor temperature across all rooms
room_columns = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
y = dataset.data.features[room_columns].mean(axis=1)

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model to file
joblib.dump(model, 'model.pkl')
print("Model trained on average indoor temperature and saved as model.pkl")
