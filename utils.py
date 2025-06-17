import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from db import get_transactions
from datetime import datetime
from collections import defaultdict

# ---- Load trained fraud detection model and scaler
def load_model():
    try:
        with open("model/fraud_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("model/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        return model, scaler
    except Exception as e:
        raise RuntimeError(f"Model loading failed: {e}")

# ---- Predict if a transaction is fraudulent
def predict_fraud(model, scaler, trans):
    try:
        df = pd.DataFrame([{
            "amount": trans["amount"],
            "avg_daily_tx": trans.get("avg_daily_tx", 0.0),
            "time_hour": datetime.now().hour
        }])
        features_scaled = scaler.transform(df)
        prediction = model.predict(features_scaled)
        return prediction[0] == 1  # True = fraud
    except Exception as e:
        raise ValueError(f"Fraud prediction failed: {e}")

# ---- Compute average daily transaction amount for a user
def get_avg_daily_tx(username):
    try:
        tx = get_transactions(username)
        daily_totals = defaultdict(list)

        for t in tx:
            if t[2] == "Transfer":
                date = t[5].split(" ")[0]  # Extract date (YYYY-MM-DD)
                daily_totals[date].append(float(t[3]))

        if not daily_totals:
            return 0.0

        avg = np.mean([sum(amts) for amts in daily_totals.values()])
        return round(avg, 2)
    except Exception as e:
        print(f"⚠️ Error computing average daily transaction: {e}")
        return 0.0
