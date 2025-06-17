import sqlite3
from datetime import datetime

# ---- Initialize Database
def init_db():
    create_users_table()
    create_transactions_table()

# ---- Create Users Table
def create_users_table():
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

# ---- Create Transactions Table (with target_user column)
def create_transactions_table():
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            target_user TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# ---- Create New User
def create_user(username, password, email):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()

# ---- Validate User Login
def validate_user(username, password):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# ---- Get User Balance
def get_balance(username):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0.0

# ---- Update User Balance
def update_balance(username, amount_change):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount_change, username))
    conn.commit()
    conn.close()

# ---- Log Transaction
def log_transaction(username, txn_type, amount, target_user=None):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO transactions (username, type, amount, target_user, timestamp) VALUES (?, ?, ?, ?, ?)",
        (username, txn_type, amount, target_user, timestamp)
    )
    conn.commit()
    conn.close()

# ---- Get Transaction History
def get_transactions(username):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("SELECT * FROM transactions WHERE username = ?", (username,))
    transactions = c.fetchall()
    conn.close()
    return transactions

# ---- Get Email
def get_email(username):
    conn = sqlite3.connect("bank.db")
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
