import streamlit as st
import pandas as pd

# ---- PAGE SETUP ----
st.set_page_config(page_title="Car Trip CO₂ Calculator", page_icon="🚗", layout="centered")
st.title("🚗 Car Trip CO₂ Calculator")
st.write("Select your car and enter the distance to estimate your trip's carbon emissions.")

# ---- LOAD DATA ----
df = pd.read_csv("all-vehicles-model@public.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Drop rows missing critical fields
df = df.dropna(subset=["Make", "Fuel_Type1", "Model", "Co2__Tailpipe_For_Fuel_Type1"])

# ---- SIDEBAR: CAR SELECTION ----
st.sidebar.header("Select Your Vehicle")

# Step 1: Make
makes = sorted(df['Make'].unique())
selected_make = st.sidebar.selectbox("Make", makes)

# Step 2: Fuel Type
filtered_df = df[df['Make'] == selected_make]
fuel_types = sorted(filtered_df['Fuel_Type1'].dropna().unique())
selected_fuel = st.sidebar.selectbox("Fuel Type", fuel_types)

# Step 3: Model
filtered_df = filtered_df[filtered_df['Fuel_Type1'] == selected_fuel]
models = sorted(filtered_df['Model'].dropna().unique())
selected_model = st.sidebar.selectbox("Model", models)

# Step 4: Description (if needed, or you can skip)
filtered_df = filtered_df[filtered_df['Model'] == selected_model]
# If there are multiple versions, we use the full row
selected_car = filtered_df.iloc[0] if not filtered_df.empty else None

# Step 5: Trip Distance
distance_km = st.sidebar.number_input("Enter trip distance (in km)", min_value=1)

# ---- MAIN SECTION ----
st.header("Estimated Emissions")

if selected_car is not None:
    co2_g_per_mile = selected_car['Co2__Tailpipe_For_Fuel_Type1']
    if co2_g_per_mile > 0:
        co2_g_per_km = co2_g_per_mile / 1.60934
        total_emissions_grams = co2_g_per_km * distance_km
        total_emissions_kg = total_emissions_grams / 1000

        st.success(f"🌍 Estimated emissions for a {distance_km} km trip:")
        st.metric(label="CO₂ Emitted", value=f"{total_emissions_kg:.2f} kg")
    else:
        st.warning("No CO₂ data available for this vehicle.")
else:
    st.info("Please complete your vehicle selection.")




# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
