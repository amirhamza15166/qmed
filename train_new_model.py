import re
import os
import dill
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA

from qiskit.circuit.library import ZZFeatureMap
from qiskit.primitives import Sampler
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import QSVC

# Generate synthetic dataset for 3 diseases
synthetic_data = [
    {"text": "severe headache throbbing pain on one side feeling nauseous sensitive to light", "disease": "Migraine"},
    {"text": "headache nausea vomiting light sensitivity aura", "disease": "Migraine"},
    {"text": "pounding headache visual disturbances feeling sick", "disease": "Migraine"},
    
    {"text": "runny nose sore throat coughing sneezing slight fever", "disease": "Common Cold"},
    {"text": "stuffy nose cough congestion feeling tired", "disease": "Common Cold"},
    {"text": "sneezing mild headache sore throat", "disease": "Common Cold"},
    
    {"text": "painful urination frequent urge to urinate burning sensation", "disease": "Urinary Tract Infection"},
    {"text": "burning when peeing pelvic pain frequent urination", "disease": "Urinary Tract Infection"},
    {"text": "cloudy urine strong odor pain in lower abdomen", "disease": "Urinary Tract Infection"},
]
# Duplicate a few times to have enough samples for splitting
synthetic_data = synthetic_data * 10
df = pd.DataFrame(synthetic_data)

TFIDF_MAX_FEATURES = 10
N_QUBITS = 2
FEATURE_MAP_REPS = 1

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["disease"])

tfidf = TfidfVectorizer(max_features=TFIDF_MAX_FEATURES, stop_words="english")
X_tfidf = tfidf.fit_transform(df["text"]).toarray()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_tfidf)

pca = PCA(n_components=N_QUBITS, random_state=42)
X_pca = pca.fit_transform(X_scaled)

angle_scaler = MinMaxScaler(feature_range=(0, np.pi))
X_final = angle_scaler.fit_transform(X_pca)

feature_map = ZZFeatureMap(feature_dimension=N_QUBITS, reps=FEATURE_MAP_REPS)
sampler = Sampler()
quantum_kernel = FidelityQuantumKernel(feature_map=feature_map)

# Train a real QSVC
best_qsvc = QSVC(quantum_kernel=quantum_kernel)
best_qsvc.fit(X_final, y)

pipeline = {
    'model': best_qsvc,
    'tfidf': tfidf,
    'scaler': scaler,
    'pca': pca,
    'angle_scaler': angle_scaler,
    'label_encoder': label_encoder
}

os.makedirs('backend/models', exist_ok=True)
with open('backend/models/q_medai_pipeline.dill', 'wb') as f:
    dill.dump(pipeline, f)

print("Real QSVC model successfully trained and saved!")
