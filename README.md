Here is your cleaned and **Markdown-formatted `README.md`** for GitHub with proper syntax, indentation, and code blocks:

---

# 💸 FraudSniff – Smart Banking Fraud Detection System

![Streamlit App](https://img.shields.io/badge/Built%20With-Streamlit-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Machine Learning](https://img.shields.io/badge/ML-RandomForest-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**FraudSniff** is a secure, interactive banking system that performs real-time fraud detection using a trained machine learning model.  
It includes OTP-based transaction verification and stores all user data in an SQLite database.  
A lightweight Streamlit-based Banking Simulation App that enables users to deposit, withdraw, and transfer funds while detecting fraudulent transactions using a trained Machine Learning model.

---

## 🔐 Features

- 🧠 **Machine Learning Fraud Detection**: Predicts fraudulent transactions using Random Forest Classifier.
- 🔄 **OTP Email Verification**: Secure transfers with 6-digit OTP emailed to the user.
- 🧾 **Transaction History**: View past transfers and deposits.
- 👥 **Multi-user Support**: Login and manage accounts securely.
- 💾 **SQLite Integration**: Persistent storage of user data and transactions.

---

## 🏗️ Tech Stack

| Component         | Technology              |
|------------------|--------------------------|
| Frontend         | Streamlit                |
| Backend          | Python (Flask-style logic) |
| ML Model         | RandomForest (scikit-learn) |
| Database         | SQLite                   |
| Email Service    | SMTP via Gmail           |
| Deployment Ready | ✅ Yes                    |

---

## 📁 Folder Structure

```

banking\_system/
├── app.py                # Main Streamlit app
├── db.py                 # DB helper functions
├── train\_model.py        # ML model training script
├── utils.py              # Fraud detection, OTP, etc.
├── transactions.csv      # Sample dataset for training
├── model/
│   ├── fraud\_model.pkl   # Trained ML model
│   └── scaler.pkl        # Feature scaler
└── bank.db               # SQLite database

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/yourusername/fraudsniff-banking-system.git
cd fraudsniff-banking-system
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Email for OTP

In `utils.py`, update the following lines with your Gmail and **App Password**:

```python
sender_email = "your_email@gmail.com"
password = "your_app_password"
```

⚠️ **Important**: If you have 2FA enabled, generate an [App Password](https://support.google.com/accounts/answer/185833).

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 🧪 Training Your Own Model (Optional)

To retrain the fraud detection model with your own data:

```bash
python train_model.py
```

Make sure your `transactions.csv` includes:

* `amount`
* `timestamp`
* `avg_daily_tx` *(optional, can be derived)*
* `is_fraud` *(0 or 1)*

---

## 🔍 Sample Fraud Detection Logic

The model uses:

* Transaction `amount`
* User's `avg_daily_tx` over past few days
* `hour` of transaction

Prediction is made using:

```python
model.predict(scaler.transform([[amount, avg_daily_tx, hour]]))
```

---

## ✅ Demo Screenshots

| Login Page                 | Transfer with OTP        | Suspicious Detection       |
| -------------------------- | ------------------------ | -------------------------- |
| ![](screenshots/login.png) | ![](screenshots/otp.png) | ![](screenshots/fraud.png) |

*(Add images to a `/screenshots` folder in your repo)*

---

## 📌 TODO / Future Work

* ✅ Add transaction reversal on fraud detection
* 🔒 Password hashing for better security
* 📈 Real-time dashboard with fraud stats
* 📊 Improve ML accuracy using XGBoost or SMOTE

---


