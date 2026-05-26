import streamlit as st
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="PyGeotherm Permitting Tool", layout="centered")

st.title("🌋 PyGeotherm: Regulatory Permitting Tool")
st.markdown("Calculate the 95% safe advective thermal plume boundary for shallow geothermal well placement.")

# 2. Sidebar for User Inputs
st.sidebar.header("Site Parameters")
st.sidebar.markdown("---")

# Grouping by Sobol Sensitivity (Geology first!)
st.sidebar.subheader("Geological Parameters (84% Variance)")
K = st.sidebar.slider("Conductivity (K) [m/day]", 1.0, 50.0, 25.0)
grad = st.sidebar.slider("Regional Gradient (∇h)", 0.001, 0.005, 0.003, step=0.0001, format="%.4f")

st.sidebar.subheader("Operational Parameters (5% Variance)")
Q = st.sidebar.slider("Injection Rate (Q) [m³/day]", 10.0, 100.0, 50.0)

# The Global Geography Fix: Ask for Delta T instead of Absolute T
delta_T = st.sidebar.slider("Temperature Difference (ΔT) [°C]", 1.0, 10.0, 5.0)
st.sidebar.caption("ΔT = Injection Temp - Ambient Groundwater Temp")

# 3. The Math Engine (Equation 13 + Optimization)
# Map the user's ΔT back to the LHS matrix baseline (15°C)
T_calc = delta_T + 15.0

# 3. The Math Engine (Equation 13 + Optimization)
raw_radius = ((((T_calc - 3.5191402) * 10.238261) + Q) * grad) * (K / 0.015464533)
raw_radius = max(raw_radius, 0.0)

optimal_buffer = 333.3
safe_radius = raw_radius + optimal_buffer

# 4. Display Results
st.subheader("Plume Projection Results")
col1, col2 = st.columns(2)

# Use Streamlit's built-in metric UI for a clean dashboard look
col1.metric(label="Raw AI Prediction", value=f"{raw_radius:.1f} m", delta="Unbuffered", delta_color="off")
col2.metric(label="Regulatory Boundary", value=f"{safe_radius:.1f} m", delta="+333.3 m Safety Buffer")

st.success(f"✅ The recommended 95% safe regulatory exclusion zone for this well is **{safe_radius:.1f} meters**.")

st.caption("Methodology derived from Latin Hypercube MODFLOW 6 simulations and constrained optimization algorithms.")
