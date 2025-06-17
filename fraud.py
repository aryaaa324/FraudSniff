import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ----------------- LOAD DATA -----------------

CSV_PATH = r"C://Users//91971//banking_system//transactions.csv"
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"❌ File not found: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)
print("📄 Sample Data:")
print(df.head())

# ----------------- DATA VALIDATION -----------------

if 'is_fraud' not in df.columns:
    raise ValueError("❌ Missing 'is_fraud' column in dataset!")

df.fillna(0, inplace=True)

# ----------------- FEATURE ENGINEERING -----------------

# Time-based feature
if 'timestamp' in df.columns:
    df['time_hour'] = pd.to_datetime(df['timestamp']).dt.hour
else:
    df['time_hour'] = 12  # default fallback hour

# Moving average transaction (you may replace this with real user history in production)
if 'avg_daily_tx' not in df.columns:
    df['avg_daily_tx'] = df['amount'].rolling(window=3, min_periods=1).mean()

# Final features used in model
features = ['amount', 'avg_daily_tx', 'time_hour']
if not all(col in df.columns for col in features):
    raise ValueError("❌ One or more required features are missing!")

X = df[features]
y = df['is_fraud']

# ----------------- SPLIT DATA -----------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ----------------- SCALING -----------------

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ----------------- MODEL TRAINING -----------------

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# ----------------- EVALUATION -----------------

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n🎯 Accuracy: {accuracy:.4f}")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\n🔍 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ----------------- SAVE MODEL -----------------

MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

with open(os.path.join(MODEL_DIR, "fraud_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(MODEL_DIR, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

print("\n✅ Fraud model and scaler saved successfully to 'model/' folder.")
