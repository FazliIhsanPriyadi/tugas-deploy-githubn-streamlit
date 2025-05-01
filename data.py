import streamlit as st
import plotly.express as px
import pandas as pd

# Load data
def load_data():
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

# Filter data berdasarkan tahun dan lokasi
def filter_data(df, year=None, locations=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if locations and "Semua Provinsi" not in locations:
        df = df[df['Location'].isin(locations)]
    return df

# Pilihan tahun di sidebar
def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else str(x)
    )

# Pilihan lokasi di sidebar dengan multiselect
def select_location(df):
    locations = ["Semua Provinsi"] + sorted(df['Location'].unique())
    selected_locations = st.sidebar.multiselect(
        "Pilih Provinsi",
        options=locations,
        default=["Semua Provinsi"]
    )
    return selected_locations

# Tampilkan data tabel
def show_data(df):
    selected_columns = ['Date', 'Location', 'New Cases', 'New Deaths', 'New Recovered',
                        'Total Cases', 'Total Deaths', 'Total Recovered']
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 Indonesia 🇮🇩🔴⚪")
    st.dataframe(df_selected.head(20))

# Fungsi total
def total_case(df):
    return df['Total Cases'].sum()

def total_death(df):
    return df['Total Deaths'].sum()

def total_recovery(df):
    return df['Total Recovered'].sum()

# Tampilkan metrik
def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="🦠 Total Kasus", value=f"{kasus/1000:.1f}K")
    col2.metric(label="💀 Total Kematian", value=f"{kematian/1000:.1f}K")
    col3.metric(label="💚 Total Sembuh", value=f"{sembuh/1000:.1f}K")

# Pie chart: Kematian vs Sembuh
def pie_chart1(df):
    total_mati = total_death(df)
    total_sembuh = total_recovery(df)

    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_mati, total_sembuh]
    }

    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#ff6459', '#4de89f']
    )

    st.plotly_chart(fig, use_container_width=True)

# Bar chart: 5 provinsi kematian tertinggi
def bar_chart1(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# Bar chart: 5 provinsi kesembuhan tertinggi
def bar_chart2(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Recovered')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='greens',
        title='5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# Map chart sebaran kasus
def map_chart(df, year=None):
    df['Date'] = pd.to_datetime(df['Date'])

    if year:
        df = df[df['Date'].dt.year == year]

    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])

    if df_map.empty:
        st.info("⚠️ Tidak ada data untuk ditampilkan di peta.")
        return

    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118},
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)