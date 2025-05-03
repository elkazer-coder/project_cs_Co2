import streamlit as st
import pandas as pd

# ---- PAGE SETUP ----
st.set_page_config(page_title="Car Selection", page_icon="🚗", layout="centered")
st.title("🚗 Select Your Car")
st.write("Choose your car step by step.")

# ---- LOAD DATA ----
df = pd.read_csv("Euro_6_latest.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Drop rows with missing key fields
df = df.dropna(subset=['Manufacturer', 'Fuel_Type', 'Model', 'Description'])

# ---- SIDEBAR: Full Selection ----
st.sidebar.header("Select Your Vehicle")

# Step 1: Manufacturer
manufacturers = sorted(df['Manufacturer'].unique())
selected_manufacturer = st.sidebar.selectbox("Step 1: Manufacturer", manufacturers)

# Step 2: Fuel Type (filtered by brand)
filtered_df = df[df['Manufacturer'] == selected_manufacturer]
fuel_types = sorted(filtered_df['Fuel_Type'].unique())
selected_fuel = st.sidebar.selectbox("Step 2: Fuel Type", fuel_types)

# Step 3: Model (filtered by brand + fuel)
filtered_df = filtered_df[filtered_df['Fuel_Type'] == selected_fuel]
models = sorted(filtered_df['Model'].unique())
selected_model = st.sidebar.selectbox("Step 3: Model", models)

# Step 4: Description (filtered by brand + fuel + model)
filtered_df = filtered_df[filtered_df['Model'] == selected_model]
descriptions = sorted(filtered_df['Description'].unique())
selected_description = st.sidebar.selectbox("Step 4: Description", descriptions)



# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
