import streamlit as st
import pandas as pd

# ---- PAGE SETUP ----
st.set_page_config(page_title="Car Journey CO₂ Emission Calculator", page_icon="🚗", layout="centered")

st.title("🚗 Car Journey CO₂ Emission Calculator")
st.write("Select your vehicle to estimate CO₂ emissions.")

try:
    # ---- LOAD DATA ----
    df = pd.read_csv("Euro_6_latest.csv", encoding="ISO-8859-1")  # read the file with correct encoding

    # Clean up column names
    df.columns = df.columns.str.strip()                # remove leading/trailing spaces
    df.columns = df.columns.str.replace(" ", "_")      # replace spaces with underscores
    df.columns = df.columns.str.replace("–", "-")      # normalize special dashes

    # Rename CO₂ column to CO2 for easier handling
    if "CO₂" in df.columns:
        df = df.rename(columns={"CO₂": "CO2"})

    # Show column names for verification (can be removed later)
    st.write("✅ Loaded CSV columns:")
    st.write(df.columns.tolist())

    # Drop rows with missing values in key columns
    required_columns = ['Manufacturer', 'Fuel_Type', 'Model', 'CO2']
    df = df.dropna(subset=required_columns)

    # ---- SIDEBAR FILTERS ----
    st.sidebar.header("Select your vehicle")

    # Step 1: Brand
    brands = sorted(df['Manufacturer'].unique())
    selected_brand = st.sidebar.selectbox("Manufacturer", brands)

    # Step 2: Fuel Type
    types = sorted(df[df['Manufacturer'] == selected_brand]['Fuel_Type'].unique())
    selected_type = st.sidebar.selectbox("Fuel Type", types)

    # Step 3: Model
    models = sorted(df[
        (df['Manufacturer'] == selected_brand) &
        (df['Fuel_Type'] == selected_type)
    ]['Model'].unique())
    selected_model = st.sidebar.selectbox("Model", models)

    # Step 4: Transmission
    transmissions = sorted(df[
        (df['Manufacturer'] == selected_brand) &
        (df['Fuel_Type'] == selected_type) &
        (df['Model'] == selected_model)
    ]['Transmission'].dropna().unique())
    selected_transmission = st.sidebar.selectbox("Transmission", transmissions)

    # Step 5: Euro Standard
    euro_standards = df[
        (df['Manufacturer'] == selected_brand) &
        (df['Fuel_Type'] == selected_type) &
        (df['Model'] == selected_model) &
        (df['Transmission'] == selected_transmission)
    ]['Euro_Standard'].dropna().unique()
    selected_euro = st.sidebar.selectbox("Euro Standard", euro_standards)

    # ---- MAIN OUTPUT ----
    st.header("Selected Vehicle Summary")

    filtered_df = df[
        (df['Manufacturer'] == selected_brand) &
        (df['Fuel_Type'] == selected_type) &
        (df['Model'] == selected_model) &
        (df['Transmission'] == selected_transmission) &
        (df['Euro_Standard'] == selected_euro)
    ]

    if not filtered_df.empty:
        st.success(f"You selected: **{selected_brand} {selected_model}** "
                   f"({selected_type}, {selected_transmission}, Euro {selected_euro})")
        st.write("Here is your vehicle's data:")
        st.dataframe(filtered_df)
        st.info(f"💨 Average CO₂ emissions: **{filtered_df['CO2'].mean():.1f} g/km**")
    else:
        st.warning("No matching data found.")

except Exception as e:
    st.error("❌ Failed to load or process the CSV file.")
    st.exception(e)






# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
