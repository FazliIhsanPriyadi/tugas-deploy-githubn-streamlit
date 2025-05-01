import streamlit as st
from data import *

# Judul halaman
def judul():
    st.title("😀 Dashboard Covid-19 Indonesia")
    st.markdown(
        "Selamat datang di dashboard interaktif untuk menganalisis data **Covid-19** di Indonesia 🇮🇩."
    )

st.sidebar.title("🧭 Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])

# Load dan filter data
df = load_data()
year = select_year()
locations = select_location(df)
df_filtered = filter_data(df, year, locations)

# Halaman HOME
if menu == "Home":
    judul()
    kolom(df_filtered)
    pie_chart1(df_filtered)
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered, year)

# Halaman DATA
elif menu == "Halaman Data":
    judul()
    show_data(df_filtered)