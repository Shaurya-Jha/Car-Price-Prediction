from pandas.core.internals.construction import ma
import streamlit as st
import requests

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚘",
    layout='centered'
)

# change if your endpoint differs
API_URL = (
    # "https://car-prediction-lpfl.onrender.com/predict"
    # or 
    "http://127.0.0.1:8000/predict"
)

st.title("🚘 Car Price Prediction")
st.caption('This UI sends data to FastAPI backend and shows predicted selling price.')

# INPUTS (make sure this matches with dataset columns exactly)
car_name = st.text_input("Car_Name (eg. Swift, Ritz SX4", value="Swift")

year = st.number_input("Year", min_value=1990, max_value=2026, value=2014, step=1)

present_price = st.number_input("Present_Price (in lakhs)", min_value=0.0, value=5.59, step=0.1)

kms_drive = st.number_input("Kms_Drive", min_value=0, max_value=40000, step=500)

fuel_type = st.selectbox("Fuel_Type", ['Petrol', 'Diesel', 'CNG'])

seller_type = st.selectbox("Seller_Type", ['Dealer', 'Individual'])

transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])

# owner is numeric in the dataset (0,1,3). Map UI labels to int
owner_label = st.selectbox(
    "Owner",
    ["0 (First Owner", "1 (Second Owner)", "3 (Third Owner)"]
)

owner = int(owner_label.split()[0])

payload = {
    "Car_Name": str(car_name),
    "Year": str(year),
    "Present_Price": float(present_price),
    "Kms_Driven": int(kms_drive),
    "Fuel_Type": str(fuel_type),
    "Seller_Type": str(seller_type),
    "Transmission": str(transmission),
    "Owner": int(owner),
}

st.write("### Payload being sent: ")
st.json(payload)

if st.button("Predict Price 💰"):
    try:
        res = requests.post(API_URL, json=payload, timeout=20)

        if res.status_code == 200:
            data = res.json()

            # adjust keys based on your api response
            # common patterns: {'prediction': 3.45} or {'predicted_price': 3.45}
            pred = data.get("prediction", data.get("predicted_price", None))

            if pred is None:
                st.warning(
                    "API responsed but prediction key not found. Full response below: "
                )
                st.json(data)
            else:
                st.success(f"Predicted Selling Price: **Rs {pred:.2f} lakhs**")
        else:
            st.error(f"API error: {res.status_code}")
            st.code(res.text)
    except requests.exceptions.RequestException as e:
        st.error("Could not connect to the API. Is server running?...")
        st.code(str(e))