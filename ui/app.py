import streamlit as st
import requests
import matplotlib.pyplot as plt

# -------------------------------
# CONFIG
# -------------------------------
API_URL = "http://127.0.0.1:8000/simulate"

st.set_page_config(page_title="Delivery Risk Engine", layout="wide")

# -------------------------------
# TITLE
# -------------------------------
st.title("🚚 Probabilistic Delivery Risk Engine")
st.markdown("Simulate delivery times using Monte Carlo + Stochastic Modeling")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("⚙️ Simulation Settings")

runs = st.sidebar.slider("Simulation Runs", 1000, 20000, 10000)
sla = st.sidebar.slider("SLA (minutes)", 10, 100, 40)

traffic = st.sidebar.selectbox("Traffic Level", ["low", "normal", "high"])
mode = st.sidebar.selectbox("Mode", ["independent", "random_walk", "markov"])

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Stage Configuration")

pickup_mean = st.sidebar.number_input("Pickup Mean", 1, 30, 5)
pickup_std = st.sidebar.number_input("Pickup Std", 0, 10, 2)

transit_mean = st.sidebar.number_input("Transit Mean", 5, 100, 20)
transit_std = st.sidebar.number_input("Transit Std", 0, 20, 5)

drop_mean = st.sidebar.number_input("Drop Mean", 1, 30, 10)
drop_std = st.sidebar.number_input("Drop Std", 0, 10, 3)

# -------------------------------
# BUILD REQUEST
# -------------------------------
payload = {
    "stages": [
        {"name": "pickup", "mean": pickup_mean, "std": pickup_std},
        {"name": "transit", "mean": transit_mean, "std": transit_std},
        {"name": "drop", "mean": drop_mean, "std": drop_std}
    ],
    "runs": runs,
    "sla": sla,
    "mode": mode,
    "traffic_level": traffic
}

# -------------------------------
# RUN SIMULATION
# -------------------------------
if st.button("🚀 Run Simulation"):

    with st.spinner("Running Monte Carlo simulation..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code != 200:
        st.error("API Error")
        st.stop()

    data = response.json()

    # -------------------------------
    # DISPLAY METRICS
    # -------------------------------
    st.subheader("📊 Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("⏱ Expected Time", f"{data['expected_time']} min")
    col2.metric("📉 P95 Time", f"{data['p95_time']} min")
    col3.metric("⚠️ Delay Probability", f"{data['delay_probability'] * 100:.2f}%")
    col4.metric("🚦 Risk Level", data["risk_level"])

    # -------------------------------
    # COLOR ALERT
    # -------------------------------
    if data["risk_level"] == "HIGH":
        st.error("⚠️ High Risk of Delay!")
    elif data["risk_level"] == "MEDIUM":
        st.warning("⚠️ Moderate Risk")
    else:
        st.success("✅ Low Risk")

    # -------------------------------
    # HISTOGRAM (OPTIONAL IMPROVEMENT)
    # -------------------------------
    st.subheader("📈 Distribution (Simulated)")

    # Call backend again for raw results (optional improvement)
    # For now we simulate locally (simple approach)

    import numpy as np

    simulated = np.random.normal(
        data["expected_time"],
        5,
        runs
    )

    fig, ax = plt.subplots()
    ax.hist(simulated, bins=40, color="skyblue", edgecolor="black")
    st.pyplot(fig)  # I added this line so the UI actually renders your chart!
