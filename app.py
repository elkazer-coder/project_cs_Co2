import streamlit as st
import pandas as pd

# ---- PAGE SETUP ----
st.set_page_config(page_title="Car Trip CO₂ Calculator", page_icon="🚗", layout="centered")
st.title("🚗 Car Trip CO₂ Calculator")
st.write("Select your car and trip distance to estimate your CO₂ emissions and fuel usage.")

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
st.header("Estimated Impact")

# Final filter based on all four selections
final_row = df[
    (df['Make'] == selected_make) &
    (df['Fuel_Type1'] == selected_fuel) &
    (df['Model'] == selected_model) &
    (df['Year'] == selected_year)
]

if not final_row.empty:
    row = final_row.iloc[0]
    co2_g_per_mile = row['Co2__Tailpipe_For_Fuel_Type1']
    mpg = row.get('Combined_Mpg_For_Fuel_Type1', None)
    ghg_score = row.get('GHG_Score', None)

    # CO₂ calculation
    if co2_g_per_mile > 0:
        co2_g_per_km = co2_g_per_mile / 1.60934
        total_emissions_grams = co2_g_per_km * distance_km
        total_emissions_kg = total_emissions_grams / 1000
    else:
        co2_g_per_km = total_emissions_kg = None

    # Fuel consumption estimation
    if mpg and mpg > 0:
        l_per_100km = 235.21 / mpg
        fuel_for_trip = (l_per_100km * distance_km) / 100
    else:
        l_per_100km = fuel_for_trip = None

    st.success(f"{selected_make} {selected_model} ({selected_year}) - {selected_fuel}")
    
    if total_emissions_kg is not None:
        st.metric("💨 CO₂ Emissions", f"{total_emissions_kg:.2f} kg for {distance_km} km")
    else:
        st.warning("⚠️ No CO₂ data available")

    if fuel_for_trip is not None:
        st.metric("⛽ Fuel used", f"{fuel_for_trip:.2f} liters for {distance_km} km")
    else:
        st.warning("⚠️ MPG data missing — cannot calculate fuel usage.")

    # GHG Score with color
    if pd.notna(ghg_score) and ghg_score > 0:
        if ghg_score >= 8:
            color = "#2ECC71"  # green
        elif ghg_score >= 5:
            color = "#F39C12"  # orange
        else:
            color = "#E74C3C"  # red

        st.markdown(
            f"<div style='padding: 10px; background-color: {color}; border-radius: 8px; color: white; font-size: 18px;'>"
            f"🌿 GHG Score: <strong>{int(ghg_score)}</strong> (out of 10)"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("GHG score not available.")
else:
    st.info("No matching vehicle found. Please adjust your selection.")




# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
