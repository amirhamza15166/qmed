"""
Q-MedAI - Clean QSVC pipeline for 3-disease symptom classification
====================================================================
Fixes the overfitting problem seen in the original run
(Train=100%, Test=100%, CV mean=91.87%, std=2.54%).

That result is a classic overfitting fingerprint: a 100%/100% train-test
score with a noticeably lower and noisier cross-validation score means the
model memorized one lucky split instead of learning a generalizable
pattern. This script fixes it by:

  1. Using far fewer, low-dimensional features (PCA -> N_QUBITS components)
     so the quantum kernel isn't handed enough capacity to memorize.
  2. Using a shallow feature map (reps=1) - fewer reps = less kernel
     expressivity = less overfitting risk.
  3. Balancing classes (equal samples per disease) so accuracy isn't
     inflated by an easy majority class.
  4. Tuning the QSVC regularization parameter C with GridSearchCV +
     StratifiedKFold instead of picking C blindly.
  5. Reporting Train / Test / CV together and printing an automatic
     verdict, so "overfit vs underfit vs good fit" is never guesswork.

Run this in an environment with qiskit + qiskit-machine-learning installed
(e.g. Google Colab, Kaggle, or locally via:
    pip install qiskit qiskit-machine-learning scikit-learn pandas
).
"""

import re
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
)
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

from qiskit.circuit.library import ZZFeatureMap
from qiskit.primitives import Sampler
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import QSVC

# ============================================================
# 1. CONFIG - change these to pick your 3 diseases
# ============================================================
TRAIN_CSV = "symptom-disease-train-dataset.csv"   # path to train csv
TEST_CSV  = "symptom-disease-test-dataset.csv"     # path to test csv (optional, can be None)
MAPPING_JSON = "mapping.json"                      # disease name -> label id

# Pick exactly 3 diseases that have decent sample counts in the dataset.
# (You can check counts with train_df['label'].value_counts() first.)
SELECTED_DISEASES = ["Migraine", "Common Cold", "Urinary Tract Infection"]

SAMPLES_PER_CLASS = 60      # balanced sample count per disease (keeps quantum kernel fast + avoids class-imbalance inflation)
TFIDF_MAX_FEATURES = 40     # raw text features before PCA
N_QUBITS = 4                # PCA components / qubits -> keep LOW to avoid overfitting + keep runtime sane
FEATURE_MAP_REPS = 1        # shallow map = less overfitting
TEST_SIZE = 0.30            # generous held-out test set (small test sets give unreliable 100% scores)
CV_FOLDS = 5
RANDOM_STATE = 42

# ============================================================
# 2. LOAD + CLEAN DATA
# ============================================================
def clean_text(t: str) -> str:
    t = str(t)
    t = t.replace("_", " ")                 # symptom_word -> symptom word
    t = re.sub(r"[^a-zA-Z,\s]", " ", t)      # strip punctuation/numbers/junk
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t

import json
with open(MAPPING_JSON) as f:
    name_to_id = json.load(f)
id_to_name = {v: k for k, v in name_to_id.items()}

train_df = pd.read_csv(TRAIN_CSV)
frames = [train_df]
if TEST_CSV:
    frames.append(pd.read_csv(TEST_CSV))
full_df = pd.concat(frames, ignore_index=True)

selected_ids = [name_to_id[d] for d in SELECTED_DISEASES]
df = full_df[full_df["label"].isin(selected_ids)].copy()
df["text"] = df["text"].apply(clean_text)
df = df[df["text"].str.len() > 0]
df["disease"] = df["label"].map(id_to_name)

print("Samples available per selected disease (before balancing):")
print(df["disease"].value_counts())

# ---- balance classes: same number of samples per class ----
min_available = df["disease"].value_counts().min()
n_per_class = min(SAMPLES_PER_CLASS, min_available)
if n_per_class < 20:
    print(f"\nWARNING: only {n_per_class} samples/class available. "
          f"Pick diseases with more data for a stable 95-98% target.")

balanced = (
    df.groupby("disease", group_keys=False)
    .apply(lambda g: g.sample(n=n_per_class, random_state=RANDOM_STATE))
)
print(f"\nUsing {n_per_class} samples per class -> total {len(balanced)} rows")

# ============================================================
# 3. FEATURES: TF-IDF -> scale -> PCA (to N_QUBITS)
# ============================================================
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(balanced["disease"])

tfidf = TfidfVectorizer(max_features=TFIDF_MAX_FEATURES, stop_words="english")
X_tfidf = tfidf.fit_transform(balanced["text"]).toarray()

# split BEFORE fitting scaler/PCA to avoid leakage from test into train
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_raw)
X_test_scaled = scaler.transform(X_test_raw)

pca = PCA(n_components=N_QUBITS, random_state=RANDOM_STATE)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)
explained_variance = pca.explained_variance_ratio_.sum() * 100

# scale PCA output into a sane angle range for the feature map
angle_scaler = MinMaxScaler(feature_range=(0, np.pi))
X_train_final = angle_scaler.fit_transform(X_train_pca)
X_test_final = angle_scaler.transform(X_test_pca)

print(f"\nPCA explained variance with {N_QUBITS} components: {explained_variance:.2f}%")
if explained_variance < 50:
    print("WARNING: low explained variance -> consider raising N_QUBITS a bit, "
          "or the quantum kernel is working with too little signal (underfitting risk).")

# ============================================================
# 4. QUANTUM KERNEL + QSVC (with C tuned via cross-validation)
# ============================================================
feature_map = ZZFeatureMap(feature_dimension=N_QUBITS, reps=FEATURE_MAP_REPS)
sampler = Sampler()
quantum_kernel = FidelityQuantumKernel(feature_map=feature_map)

# tune C with CV instead of guessing - this is what actually controls
# overfitting (low C = more regularization) vs underfitting (too low C)
param_grid = {"C": [0.1, 0.5, 1.0, 2.0, 5.0]}
cv_splitter = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

base_qsvc = QSVC(quantum_kernel=quantum_kernel)
grid = GridSearchCV(base_qsvc, param_grid, cv=cv_splitter, scoring="accuracy", n_jobs=1)
grid.fit(X_train_final, y_train)

best_qsvc = grid.best_estimator_
print(f"\nBest C from CV grid search: {grid.best_params_['C']}")

# ============================================================
# 5. EVALUATE: TRAIN / TEST / CV TOGETHER
# ============================================================
train_pred = best_qsvc.predict(X_train_final)
test_pred = best_qsvc.predict(X_test_final)

train_accuracy = accuracy_score(y_train, train_pred)
test_accuracy = accuracy_score(y_test, test_pred)

cv_scores = cross_val_score(best_qsvc, X_train_final, y_train, cv=cv_splitter, scoring="accuracy")
cv_mean = cv_scores.mean()
cv_std = cv_scores.std()

precision = precision_score(y_test, test_pred, average="weighted", zero_division=0)
recall = recall_score(y_test, test_pred, average="weighted", zero_division=0)
f1 = f1_score(y_test, test_pred, average="weighted", zero_division=0)

# The gap that actually matters: test vs CV (not test vs train on a
# single lucky split). This is what your original code was missing.
generalization_gap = abs(train_accuracy - cv_mean)
test_cv_gap = abs(test_accuracy - cv_mean)

print("\n" + "=" * 80)
print("              Q-MedAI - FINAL QSVC RESULTS (3 diseases)")
print("=" * 80)
print("\nMODEL PERFORMANCE")
print("-" * 80)
print(f"Training Accuracy      : {train_accuracy * 100:.2f}%")
print(f"Test Accuracy          : {test_accuracy * 100:.2f}%")
print(f"Cross-Validation Mean  : {cv_mean * 100:.2f}%")
print(f"CV Standard Deviation  : {cv_std * 100:.2f}%")
print("\nCLASSIFICATION METRICS")
print("-" * 80)
print(f"Precision              : {precision * 100:.2f}%")
print(f"Recall                 : {recall * 100:.2f}%")
print(f"F1-Score                : {f1 * 100:.2f}%")
print("\nGENERALIZATION CHECK")
print("-" * 80)
print(f"Train vs CV gap         : {generalization_gap * 100:.2f}%")
print(f"Test vs CV gap          : {test_cv_gap * 100:.2f}%")

print("\nMODEL INFORMATION")
print("-" * 80)
print(f"Number of Diseases     : {len(label_encoder.classes_)}")
print(f"Quantum Features/Qubits: {N_QUBITS}")
print(f"PCA Explained Variance : {explained_variance:.2f}%")
print("\nDISEASES")
print("-" * 80)
for i, disease in enumerate(label_encoder.classes_, start=1):
    print(f"{i}. {disease}")

# ============================================================
# 6. AUTOMATIC VERDICT - overfit / underfit / good fit
# ============================================================
print("\n" + "=" * 80)
print("VERDICT")
print("-" * 80)
if train_accuracy > 0.97 and generalization_gap > 0.07:
    print("OVERFITTING: training accuracy is near-perfect but CV accuracy "
          "drops well below it. Reduce N_QUBITS, reduce FEATURE_MAP_REPS, "
          "lower C, or add more training data per class.")
elif cv_mean < 0.80 and train_accuracy < 0.85:
    print("UNDERFITTING: both training and CV accuracy are low. Try more "
          "TFIDF_MAX_FEATURES, a couple more N_QUBITS, or FEATURE_MAP_REPS=2.")
elif 0.95 <= cv_mean <= 0.98 and generalization_gap < 0.05:
    print("GOOD FIT: CV accuracy is in target range (95-98%) and consistent "
          "with training accuracy. This is a healthy, non-overfit model.")
else:
    print(f"BORDERLINE: CV mean = {cv_mean*100:.2f}%, gap = {generalization_gap*100:.2f}%. "
          "Not a clear overfit/underfit, but tune N_QUBITS/C/samples-per-class "
          "to land CV accuracy inside 95-98% with a gap under ~5%.")

print("\nConfusion Matrix (test set):")
print(confusion_matrix(y_test, test_pred))
print("\nClassification Report (test set):")
print(classification_report(y_test, test_pred, target_names=label_encoder.classes_, zero_division=0))
print("=" * 80)
