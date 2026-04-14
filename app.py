import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="CreditRiskAI", layout="wide")

st.title("🛡️ CreditRiskAI - Intelligent Loan Delinquency Management Agent")
st.markdown("**Level 6 Advanced Agentic AI • Reasoning • Memory • Tools • Reflection**")

# ====================== LOAD DATA (Fixed) ======================
@st.cache_data
def load_data():
    """Robust dataset loader"""
    # Your current local path
    local_path = r"C:\Users\HP\Projects\Gen AI Powered Data Analytics\Final_Dataset_with_Agent_Level5_Tools.xlsx"
    
    # GitHub / Streamlit Cloud paths
    cloud_paths = [
        "Datasets/Processed/Final_Dataset_with_Agent_Level5_Tools.xlsx",
        "data/processed/Final_Dataset_with_Agent_Level5_Tools.xlsx",
        "Final_Dataset_with_Agent_Level5_Tools.xlsx"
    ]
    
    # Try local path first
    if os.path.exists(local_path):
        try:
            df = pd.read_excel(local_path)
            st.success(f"✅ Loaded from local path: {len(df)} records")
            return df
        except:
            pass
    
    # Try cloud paths
    for path in cloud_paths:
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                st.success(f"✅ Loaded from: {path} ({len(df)} records)")
                return df
            except:
                pass
    
    st.error("❌ Dataset file not found! Please check the file location.")
    st.info("Expected file: Final_Dataset_with_Agent_Level5_Tools.xlsx")
    st.stop()

df = load_data()

# ====================== LOAD MEMORY ======================
memory_file = 'logs/customer_memory_level6.json'
if os.path.exists(memory_file):
    with open(memory_file, 'r') as f:
        customer_memory = json.load(f)
else:
    customer_memory = {}

# ====================== RISK SCORING ======================
def calculate_risk_score(row):
    score = 0
    if row['Missed_Payments'] >= 4: score += 50
    elif row['Missed_Payments'] >= 2: score += 25
    if row['Credit_Utilization'] > 0.70: score += 30
    elif row['Credit_Utilization'] > 0.50: score += 15
    if row['Credit_Score'] < 500: score += 15
    elif row['Credit_Score'] < 600: score += 8
    return min(score, 100)

# ====================== TOOLS ======================
def send_sms_reminder(customer):
    st.success(f"📱 SMS Sent to {customer['Customer_ID']}")
    return "SMS_SENT"

def offer_payment_plan(customer):
    st.success(f"📧 Payment Plan Offered to {customer['Customer_ID']}")
    return "PAYMENT_PLAN_OFFERED"

def escalate_to_human(customer):
    st.error(f"👤 Escalated {customer['Customer_ID']} to Human Collections Team")
    return "ESCALATED_TO_HUMAN"

# ====================== SIDEBAR ======================
st.sidebar.header("🔍 Customer Search")
search_query = st.sidebar.text_input("Search Customer ID", "")

if search_query:
    filtered_df = df[df['Customer_ID'].str.contains(search_query, case=False)]
else:
    filtered_df = df

selected_customer_id = st.sidebar.selectbox(
    "Select Customer", 
    options=filtered_df['Customer_ID'].tolist()
)

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🤖 Run Agent", "📜 History", "🔄 Compare Customers"])

with tab1:
    st.subheader("Agent Performance Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", len(df))
    col2.metric("Customers in Memory", len(customer_memory))
    col3.metric("High Risk (ESCALATE)", len(df[df['Missed_Payments'] >= 5]))
    col4.metric("Avg Risk Score", f"{df.apply(calculate_risk_score, axis=1).mean():.1f}")

with tab2:
    st.subheader(f"Run Agent on {selected_customer_id}")
    customer = df[df['Customer_ID'] == selected_customer_id].iloc[0]
    
    if st.button("🚀 Run Agent Now", type="primary"):
        risk_score = calculate_risk_score(customer)
        
        if risk_score >= 80:
            decision = "ESCALATE"
            reason = "Critical risk detected. Immediate human intervention required."
        elif risk_score >= 60:
            decision = "PAYMENT_PLAN"
            reason = "High risk but recoverable. Structured payment plan is recommended."
        elif risk_score >= 35:
            decision = "SMS_REMINDER"
            reason = "Moderate risk. A personalized reminder should help resolve this."
        else:
            decision = "MONITOR"
            reason = "Low immediate risk. Continue monitoring."

        st.info(f"**Reasoning:** {reason}")
        
        if decision == "SMS_REMINDER":
            send_sms_reminder(customer)
        elif decision == "PAYMENT_PLAN":
            offer_payment_plan(customer)
        elif decision == "ESCALATE":
            escalate_to_human(customer)
        else:
            st.info("🔍 Monitoring - No immediate action needed.")

        st.success(f"**Final Action: {decision}**")

with tab3:
    st.subheader(f"Full History for {selected_customer_id}")
    history = customer_memory.get(selected_customer_id, {"interactions": []})
    if history["interactions"]:
        st.dataframe(pd.DataFrame(history["interactions"]), use_container_width=True)
    else:
        st.info("No previous interactions found.")

with tab4:
    st.subheader("🔄 Side-by-Side Comparison")
    col1, col2 = st.columns(2)
    with col1:
        cust1 = st.selectbox("Customer 1", df['Customer_ID'].tolist(), key="cust1")
    with col2:
        cust2 = st.selectbox("Customer 2", df['Customer_ID'].tolist(), key="cust2")
    
    if st.button("Compare"):
        c1 = df[df['Customer_ID'] == cust1].iloc[0]
        c2 = df[df['Customer_ID'] == cust2].iloc[0]
        colA, colB = st.columns(2)
        with colA:
            st.write(f"**{cust1}**")
            st.metric("Risk Score", calculate_risk_score(c1))
        with colB:
            st.write(f"**{cust2}**")
            st.metric("Risk Score", calculate_risk_score(c2))

st.caption("Built as part of Tata iQ GenAI Powered Data Analytics Job Simulation")