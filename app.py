import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Precision Aviation Engine", layout="wide")

st.title("Serverless Precision Aviation Pipeline")
st.caption("Real-Time Fertilizer Ballistics & Variable Rate Material Flow Actuation")

st.sidebar.header("Avionics Configuration")
selected_zone = st.sidebar.selectbox("Target Topography", ["Canterbury Plains (High Wind)", "Waikato River Catchment (Runoff Risk)", "Southland Pastoral Hill Country"])
weather_shock = st.sidebar.slider("Simulate Wind Shear & Turbulence Severity", 1.0, 5.0, 3.5)
run_simulation = st.sidebar.button("Initialize Edge Ballistics Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Flight Telemetry -> XGBoost Edge Inference -> Flow Actuation")

if run_simulation:
    st.subheader(f"Active Flight Operation: {selected_zone}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_wind = col1.empty()
    metric_flow = col2.empty()
    metric_runoff = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(3131)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    wind_speeds = []
    flow_rates = []
    
    base_wind = 15.0 
    base_flow = 100.0
    
    for i in range(100):
        if i < 30:
            current_wind = base_wind + np.random.uniform(-2.0, 2.0)
            current_flow = base_flow + np.random.uniform(-1.0, 1.0)
            runoff_risk = np.random.uniform(5.0, 15.0)
            status = "OPTIMAL TRAJECTORY"
        elif i >= 30 and i < 70:
            current_wind = base_wind + (i - 30) * (1.5 * weather_shock) + np.random.uniform(-5.0, 5.0)
            current_flow = max(10.0, base_flow - (current_wind * 1.2)) + np.random.uniform(-5.0, 5.0)
            runoff_risk = np.random.uniform(70.0, 95.0)
            status = "BALLISTIC CORRECTION ACTIVE"
        else:
            current_wind = current_wind - np.random.uniform(2.0, 8.0)
            current_wind = max(base_wind, current_wind)
            current_flow = min(base_flow, current_flow + np.random.uniform(5.0, 15.0))
            runoff_risk = np.random.uniform(15.0, 30.0) 
            status = "FLOW RESTORED"
            
        wind_speeds.append(current_wind)
        flow_rates.append(current_flow)
        
        metric_wind.metric("Avionic Wind Shear (Knots)", f"{current_wind:.1f} kts", f"{(current_wind - base_wind):.1f} kts")
        metric_flow.metric("Hopper Material Flow Rate (kg/s)", f"{current_flow:.1f} kg/s", "Edge Controlled")
        metric_runoff.metric("Predicted Chemical Runoff Risk", f"{runoff_risk:.1f}%")
        
        if status == "BALLISTIC CORRECTION ACTIVE":
            metric_status.metric("Edge Computing Status", status, "Restricting Flow")
        elif status == "FLOW RESTORED":
            metric_status.metric("Edge Computing Status", status, "Normalizing")
        else:
            metric_status.metric("Edge Computing Status", status, "Target Locked")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=wind_speeds, mode='lines', name='Wind Speed (Knots)', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=flow_rates, mode='lines', name='Material Flow Rate (kg/s)', yaxis='y2', line=dict(color='green', dash='dot')))
        
        fig.update_layout(
            title="Agricultural Aviation: Exogenous Wind Shear vs Machine Learning Actuation",
            xaxis=dict(title="High-Frequency Flight Timeline"),
            yaxis=dict(title="Wind Speed (Knots)", range=[0, max(60, current_wind + 10)]),
            yaxis2=dict(title="Flow Rate (kg/s)", overlaying='y', side='right', range=[0, 120]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "BALLISTIC CORRECTION ACTIVE" and i == 30:
            log_placeholder.error(f"AERODYNAMIC ALERT: Severe crosswind anomaly detected at {time_steps[i].strftime('%H:%M:%S')}. Edge machine learning engine dynamically restricting variable-rate hopper to prevent fertilizer drift into adjacent waterways.")
        elif status == "FLOW RESTORED" and i == 70:
            log_placeholder.success(f"ORCHESTRATION SUCCESS: Wind shear stabilizing. Predictive ballistics engine autonomously restoring baseline material flow rate.")
        elif status == "OPTIMAL TRAJECTORY" and i % 5 == 0:
            log_placeholder.info(f"Log: Flight telemetry tick {i} ingested via edge node. Fertilizer ballistics matching digital topographical target.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless edge-computing pipeline successfully optimized material flow and completely mitigated the agricultural runoff risk.")
else:
    st.info("Click 'Initialize Edge Ballistics Engine' in the sidebar to simulate high-velocity aviation data processing.")