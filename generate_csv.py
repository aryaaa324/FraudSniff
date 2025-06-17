import pandas as pd
import numpy as np
import random

def generate_fake_data(n=200):
    usernames = [f"user{i}" for i in range(1, 11)]
    transaction_types = ["Deposit", "Withdraw", "Transfer"]

    data = []
    for _ in range(n):
        username = random.choice(usernames)
        trans_type = random.choice(transaction_types)
        amount = round(random.uniform(100, 50000), 2)
        target = random.choice(usernames) if trans_type == "Transfer" else None

        # Simple fraud logic
        is_large = 1 if amount > 30000 else 0
        is_self_transfer = 1 if trans_type == "Transfer" and target == username else 0
        is_fraud = 1 if (trans_type == "Withdraw" and amount > 30000) or is_self_transfer else 0

        data.append([
            username, trans_type, amount, target, is_large, is_self_transfer, is_fraud
        ])

    df = pd.DataFrame(data, columns=[
        "username", "type", "amount", "target", "is_large_txn", "is_self_transfer", "is_fraud"
    ])
    return df

# Generate and save
df = generate_fake_data(200)
df.to_csv("transactions.csv", index=False)
print("✅ transactions.csv with 200 rows has been generated!")
