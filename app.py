import streamlit as st
import pandas as pd

# ---- PAGE SETUP ----
st.set_page_config(
    page_title="Car Journey CO₂ Emission Calculator",  # Sets the page title
    page_icon="🚗",  # Icon shown in the browser tab
    layout="centered"  # Centers the app layout
)

st.title("🚗 Car Journey CO₂ Emission Calculator")  # Main title at the top of the page
st.write("Select your vehicle to estimate CO₂ emissions.")  # Description

# ---- DATA LOADING ----
df = pd.read_csv("Euro_6_latest.csv")  # to read the CSV file 

# Remove rows with missing key data to avoid errors in dropdowns
df = df.dropna(subset=['Manufacturer', 'Fuel Type', 'Model', 'CO2'])

# ---- SIDEBAR FILTERS ----
st.sidebar.header("Select your vehicle")  # Sidebar section title

# Dropdown 1: Manufacturer (car brand)
brands = sorted(df['Manufacturer'].unique())  # Get unique brands from the CSV
selected_brand = st.sidebar.selectbox("Manufacturer", brands)  # Let user choose a brand

# Dropdown 2: Fuel Type (Petrol, Diesel, Electric, etc.) - filtered by brand
types = sorted(df[df['Manufacturer'] == selected_brand]['Fuel Type'].unique())
selected_type = st.sidebar.selectbox("Fuel Type", types)

# Dropdown 3: Model - filtered by brand and fuel type
models = sorted(df[
    (df['Manufacturer'] == selected_brand) &
    (df['Fuel Type'] == selected_type)
]['Model'].unique())
selected_model = st.sidebar.selectbox("Model", models)

# Dropdown 4: Transmission type - filtered by previous selections
transmissions = sorted(df[
    (df['Manufacturer'] == selected_brand) &
    (df['Fuel Type'] == selected_type) &
    (df['Model'] == selected_model)
]['Transmission'].dropna().unique())
selected_transmission = st.sidebar.selectbox("Transmission", transmissions)

# Dropdown 5: Euro Standard - filtered by brand + fuel type + model + transmission
euro_standards = df[
    (df['Manufacturer'] == selected_brand) &
    (df['Fuel Type'] == selected_type) &
    (df['Model'] == selected_model) &
    (df['Transmission'] == selected_transmission)
]['Euro Standard'].dropna().unique()
selected_euro = st.sidebar.selectbox("Euro Standard", euro_standards)

# ---- MAIN OUTPUT ----
st.header("Selected Vehicle Summary")  # Section title

# Filter the DataFrame to show the exact selected row(s)
filtered_df = df[
    (df['Manufacturer'] == selected_brand) &
    (df['Fuel Type'] == selected_type) &
    (df['Model'] == selected_model) &
    (df['Transmission'] == selected_transmission) &
    (df['Euro Standard'] == selected_euro)
]

# If a matching row exists, show its info
if not filtered_df.empty:
    st.success(f"You selected: **{selected_brand} {selected_model}** "
               f"({selected_type}, {selected_transmission}, Euro {selected_euro})")  # Summary text
    st.write("Here is your vehicle's technical data:")  # Explanation
    st.dataframe(filtered_df)  # Shows the full row(s) in a table
    st.info(f"💨 Average CO₂ emissions: **{filtered_df['CO2'].mean():.1f} g/km**")  # Shows mean CO₂
else:
    st.warning("No data found for the selected combination.")  # Shown if the selection returns nothing




# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
