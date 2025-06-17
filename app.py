import streamlit as st
from db import *
from utils import load_model, predict_fraud
from datetime import datetime

# Initialize DB and ML model
init_db()
model, scaler = load_model()

# App Title
st.markdown("""
    <h1 style='text-align: center; color: #4B8BBE;'>FraudSniff 🕵️‍♂️</h1>
    <hr style='margin-top: -10px; margin-bottom: 30px;'>
""", unsafe_allow_html=True)

# Session state setup
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Sidebar menu
menu = ["Login", "Register"] if not st.session_state.logged_in else ["Dashboard", "Logout"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------- LOGIN -------------------
if choice == "Login":
    st.title("Login")
    u = st.text_input("Username").strip().lower()
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_user(u, p):
            st.session_state.logged_in = True
            st.session_state.username = u
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ------------------- REGISTER -------------------
elif choice == "Register":
    st.title("Register")
    u = st.text_input("New Username").strip().lower()
    p = st.text_input("New Password", type="password")
    e = st.text_input("Email Address").strip().lower()
    if st.button("Register"):
        if not u or not p or not e:
            st.error("Username, password and email cannot be empty!")
        else:
            try:
                create_user(u, p, e)
                st.success("Account created successfully!")
                st.info("Go to Login to access your account.")
            except Exception as ex:
                st.error(f"Username already exists or database error: {ex}")

# ------------------- DASHBOARD -------------------
elif choice == "Dashboard":
    username = st.session_state.username
    st.title(f"Welcome, {username} 👋")
    bal = get_balance(username)
    st.subheader(f"💰 Balance: ₹{bal:.2f}")

    # ----------- Deposit -----------
    with st.form("deposit_form"):
        amt = st.number_input("Deposit Amount", min_value=0.0)
        if st.form_submit_button("Deposit"):
            update_balance(username, amt)
            log_transaction(username, "Deposit", amt)
            st.success(f"Deposited ₹{amt:.2f}")
            st.rerun()

    # ----------- Withdraw -----------
    with st.form("withdraw_form"):
        w_amt = st.number_input("Withdraw Amount", min_value=0.0)
        if st.form_submit_button("Withdraw"):
            if bal >= w_amt:
                update_balance(username, -w_amt)
                log_transaction(username, "Withdraw", w_amt)
                st.success(f"Withdrew ₹{w_amt:.2f}")
                st.rerun()
            else:
                st.error("❌ Insufficient balance")

    # ----------- Transfer -----------
    with st.form("transfer_form"):
        t_user = st.text_input("Transfer To").strip().lower()
        t_amt = st.number_input("Transfer Amount", min_value=0.0)

        if st.form_submit_button("Transfer"):
            if t_user == username:
                st.error("⚠️ Cannot transfer to self")
                st.stop()

            try:
                t_bal = get_balance(t_user)
            except:
                st.error("❌ Target user does not exist")
                st.stop()

            if bal >= t_amt:
                # Simulate potential fraud
                features = {
                    "amount": t_amt,
                    "oldbalanceOrg": bal,
                    "newbalanceOrig": bal,  # suspicious: balance unchanged
                    "oldbalanceDest": t_bal,
                    "newbalanceDest": t_bal + t_amt
                }

                flag = predict_fraud(model, scaler, features)

                if flag:
                    st.warning("⚠️ Suspicious transfer detected! Transaction blocked.")
                    st.stop()

                # Proceed with actual deduction
                update_balance(username, -t_amt)
                update_balance(t_user, t_amt)
                log_transaction(username, "Transfer", t_amt, t_user)
                st.success(f"Transferred ₹{t_amt:.2f} to {t_user}")
                st.rerun()
            else:
                st.error("❌ Insufficient funds")

    # ----------- Transaction History -----------
    st.subheader("📜 Transaction History")
    hist = get_transactions(username)
    if not hist:
        st.info("No transactions yet.")
    else:
        for h in hist[::-1]:
            date_str = h[5].split(".")[0] if h[5] else "Unknown date"
            st.info(f"[{date_str}] {h[2]} ₹{h[3]:.2f} {'to ' + h[4] if h[4] else ''}")

# ------------------- LOGOUT -------------------
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.rerun()
