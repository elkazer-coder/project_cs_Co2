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

# ---- SIDEBAR: Manufacturer ----
st.sidebar.header("Step 1: Choose Manufacturer")
manufacturers = sorted(df['Manufacturer'].unique())
selected_manufacturer = st.sidebar.selectbox("Manufacturer", manufacturers)

# ---- MAIN PAGE: Steps 2–4 ----
st.header("Continue selecting your car")

# Step 2: Fuel Type
filtered_df = df[df['Manufacturer'] == selected_manufacturer]
fuel_types = sorted(filtered_df['Fuel_Type'].unique())
selected_fuel = st.selectbox("Step 2: Choose Fuel Type", fuel_types)

# Step 3: Model
filtered_df = filtered_df[filtered_df['Fuel_Type'] == selected_fuel]
models = sorted(filtered_df['Model'].unique())
selected_model = st.selectbox("Step 3: Choose Model", models)

# Step 4: Description
filtered_df = filtered_df[filtered_df['Model'] == selected_model]
descriptions = sorted(filtered_df['Description'].unique())
selected_description = st.selectbox("Step 4: Choose Description", descriptions)


# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
