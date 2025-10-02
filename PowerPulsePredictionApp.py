import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import pickle
import emoji
from datetime import datetime

# Load the trained Linear Regression model
with open('linear_regression_model.pkl', 'rb') as file:
    lr_model = pickle.load(file)

# Load the standard scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


## Streamlit App
st.title('Power Pulse - Household Energy Price Prediction')

# User Input

Global_reactive_power = st.number_input('Global_reactive_power',min_value=0.0, max_value=5.0,step=0.1)
st.write("Selected Global Reactive Power : ",Global_reactive_power)
Voltage = st.number_input('Enter Voltage(V)', min_value=0.0,max_value=500.0,step=0.1,value=230.0,format="%.2f")
st.write("Selected Voltage : ", Voltage)
Global_intensity = st.number_input('Enter Global Intensity ', min_value=0.0,max_value=100.0,step=0.1,value=50.0,format="%.2f")
st.write("Selected Global intensity : ", Global_intensity)
Sub_metering_1 = st.slider("Sub_metering_1(Wh)", min_value=0.0, max_value=100.0, step=1.0, value=10.0)
Sub_metering_2 = st.slider("Sub_metering_2(Wh)", min_value=0.0, max_value=100.0, step=1.0, value=15.0)
Sub_metering_3 = st.slider("Sub_metering_3(Wh)", min_value=0.0, max_value=100.0, step=1.0, value=20.0)
st.write("=====  Selected Sub-Metering values  =====")
st.write(f"Sub_metering_1: {Sub_metering_1} Wh")
st.write(f"Sub_metering_2: {Sub_metering_2} Wh")
st.write(f"Sub_metering_3: {Sub_metering_3} Wh")
Peak_Hour = st.selectbox("Select Hour (0-23)", list(range(24)))
if Peak_Hour in [18,19,20,21]:
    Peak_Hour =1
    st.write("Is It Peak Hour? : ","YES") 
else:
    Peak_Hour =10
    st.write("Is It Peak Hour? : ","NO") 

selected_date = st.date_input("Select Date", value=datetime.today())


selected_time = st.time_input("Select Time", value=datetime.now().time())


Year = selected_date.year
Month = selected_date.month
Date = selected_date.day
Hour = selected_time.hour
Min = selected_time.minute

st.write(f"Date: {selected_date}, Time: {selected_time}")

Rolling_1h_GlobalPower = st.number_input('Rolling_1h_GlobalPower',min_value=0.0, max_value=5.0,step=0.1)
Rolling_1h_GlobalReactivePower = st.number_input('Rolling_1h_GlobalReactivePower',min_value=0.0, max_value=5.0,step=0.1)
Rolling_1h_Voltage = st.number_input('Enter Rolling_1h_Voltage(V)', min_value=0.0,max_value=500.0,step=0.1,value=230.0,format="%.2f")
Rolling_1h_Global_intensity =  st.number_input('Enter Rolling_1h_Global_intensity ', min_value=0.0,max_value=100.0,step=0.1,value=50.0,format="%.2f",key="global_intensity_1")
input_data = pd.DataFrame({
    'Date':[Date],
    'Global_reactive_power':[Global_reactive_power],
    'Voltage':[Voltage],
    'Global_intensity':[Global_intensity],
    'Sub_metering_1':[Sub_metering_1],
    'Sub_metering_2':[Sub_metering_2],
    'Sub_metering_3':[Sub_metering_3],     
    'Month':[Month],
    'Year':[Year],
    'Hour':[Hour],
    'Min':[Min],
    'Peak_Hour':[Peak_Hour],   
    'Rolling_1h_GlobalPower':[Rolling_1h_GlobalPower],
    'Rolling_1h_GlobalReactivePower':[Rolling_1h_GlobalReactivePower],
    'Rolling_1h_Voltage':[Rolling_1h_Voltage],
    'Rolling_1h_Global_intensity':[Rolling_1h_Global_intensity]
})

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Predict House Hold energy Price
prediction_array = lr_model.predict(input_data_scaled)
prediction = prediction_array[0] 

st.markdown(
    f"""
    <div style="
        background-color:#f0f8ff;
        padding:20px;
        border-radius:15px;
        text-align:center;
        font-size:30px;
        color:#1f77b4;
        font-weight:bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    ">
        Predicted Global Active Power<br>
        {prediction:.2f} Wh
    </div>
    """,
    unsafe_allow_html=True
)



