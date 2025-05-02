import streamlit as st

# ---- PAGE SETUP ----
st.set_page_config(page_title="Car Journey CO₂ Emission Calculator", page_icon="🚗", layout="centered")

st.title("🚗 Car Journey CO₂ Emission Calculator")
st.write("Select your car below to estimate emissions for your trip.")

#Vehicle Data Structure (dictionnary)
vehicles = {
    "Toyota": {
        "Petrol": ["Corolla", "Yaris"],
        "Hybrid": ["Prius", "C-HR"]
    },
    "BMW": {
        "Diesel": ["320d", "530d"],
        "Electric": ["i3", "iX"]
    },
    "Renault": {
        "Petrol": ["Clio", "Megane"],
        "Electric": ["Zoe"]
    }
}

# ---- SIDEBAR ----
st.sidebar.header("Choose your vehicle")

# Select brand
brands = list(vehicles.keys())
selected_brand = st.sidebar.selectbox("Select car brand", brands)

# Select type based on brand
if selected_brand:
    types = list(vehicles[selected_brand].keys())
    selected_type = st.sidebar.selectbox("Select vehicle type (fuel)", types)
else:
    selected_type = None

# Select model based on brand and type
if selected_brand and selected_type:
    models = vehicles[selected_brand][selected_type]
    selected_model = st.sidebar.selectbox("Select vehicle model", models)
else:
    selected_model = None

# Select year after model
if selected_model:
    years = list(range(1990, 2026))  
    selected_year = st.sidebar.selectbox("Select year of the car", years)
else:
    selected_year = None

# ---- MAIN SECTION ----
st.header("Vehicle Summary")

if selected_model and selected_year:
    st.success(f"You selected a **{selected_brand} {selected_model}** ({selected_year}) using **{selected_type}**.")
else:
    st.info("Please complete all selections to continue.")



# ---- FOOTER ----
st.markdown("""---""")
st.caption("Data sources: OpenRouteService, Carbon Interface API, Kaggle CO₂ dataset.")
