import streamlit as st
import pandas as pd

# ---- PAGE SETUP ----
st.set_page_config(page_title="Car Trip CO₂ Calculator", page_icon="🚗", layout="centered")
st.title("🚗 Car Trip CO₂ Calculator")
st.write("Select your car and trip distance to estimate your CO₂ emissions.")

# ---- LOAD DATA ----
df = pd.read_csv("all-vehicles-model@public.csv", sep=";", encoding="ISO-8859-1", engine="python")
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Drop rows missing critical fields
df = df.dropna(subset=["Make", "Fuel_Type1", "Model", "Year", "Co2__Tailpipe_For_Fuel_Type1"])

# ---- SIDEBAR: FULL CAR SELECTION ----
st.sidebar.header("Select Your Vehicle")

# Step 1: Make
makes = sorted(df['Make'].dropna().unique())
selected_make = st.sidebar.selectbox("Make", makes)

# Step 2: Fuel Type
filtered_df = df[df['Make'] == selected_make]
fuel_types = sorted(filtered_df['Fuel_Type1'].dropna().unique())
selected_fuel = st.sidebar.selectbox("Fuel Type", fuel_types)

# Step 3: Model
filtered_df = filtered_df[filtered_df['Fuel_Type1'] == selected_fuel]
models = sorted(filtered_df['Model'].dropna().unique())
selected_model = st.sidebar.selectbox("Model", models)

# Step 4: Year
filtered_df = filtered_df[filtered_df['Model'] == selected_model]
years = sorted(filtered_df['Year'].dropna().unique(), reverse=True)
selected_year = st.sidebar.selectbox("Year", years)

# Step 5: Trip Distance
distance_km = st.sidebar.number_input("Trip Distance (km)", min_value=1)

# ---- MAIN DISPLAY ----
st.header("Estimated Emissions")

# Final filter based on all four selections
final_row = df[
    (df['Make'] == selected_make) &
    (df['Fuel_Type1'] == selected_fuel) &
    (df['Model'] == selected_model) &
    (df['Year'] == selected_year)
]

if not final_row.empty:
    co2_g_per_mile = final_row.iloc[0]['Co2__Tailpipe_For_Fuel_Type1']
    if co2_g_per_mile > 0:
        co2_g_per_km = co2_g_per_mile / 1.60934
        total_emissions_grams = co2_g_per_km * distance_km
        total_emissions_kg = total_emissions_grams / 1000

        st.success(f"{selected_make} {selected_model} ({selected_year}) - {selected_fuel}")
        st.metric("Estimated CO₂ Emissions", f"{total_emissions_kg:.2f} kg for {distance_km} km")
    else:
        st.warning("CO₂ data not available for this vehicle.")
else:
    st.info("No matching vehicle found. Please adjust your selection.")



# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
