import pandas as pd
import plotly.express as px
import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Netflix Dataset Analysis", page_icon="📺", layout="wide")

# Helper functions for the Netflix dataset
def create_daily_added_df(df, period):
    """Aggregate data by daily, monthly, or yearly additions of titles."""
    if period == "Harian":
        daily_added_df = df.resample(rule='D', on='date_added').agg({"show_id": "nunique"})
    elif period == "Bulanan":
        daily_added_df = df.resample(rule='M', on='date_added').agg({"show_id": "nunique"})
    elif period == "Tahunan":
        daily_added_df = df.resample(rule='Y', on='date_added').agg({"show_id": "nunique"})
    daily_added_df = daily_added_df.reset_index()
    daily_added_df.rename(columns={"show_id": "title_count"}, inplace=True)
    return daily_added_df

def create_top_directors_df(df):
    df['director'] = df['director'].str.split(', ')
    exploded_directors = df.explode('director')
    top_directors = (
        exploded_directors.groupby('director')['title']
        .nunique()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={'title': 'film_count'})
    )
    return top_directors

def create_top_countries_df(df):
    df['country'] = df['country'].str.split(', ')
    exploded_countries = df.explode('country')
    top_countries = (
        exploded_countries.groupby('country')['title']
        .nunique()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={'title': 'film_count'})
    )
    return top_countries

def create_top_genres_df(df):
    df['listed_in'] = df['listed_in'].str.split(', ')
    exploded_genres = df.explode('listed_in')
    top_genres = (
        exploded_genres.groupby('listed_in')['title']
        .nunique()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={'title': 'genre_count'})
    )
    return top_genres

# Set default theme and colors
px.defaults.template = "plotly_dark"  # Theme
px.defaults.color_discrete_sequence = ["#E50914", "#221F1F", "#B1B1B1"]  # Netflix theme colors

# Streamlit App
st.title("Netflix Dataset Analysis")
st.write("Jelajahi kumpulan data Netflix secara interaktif untuk mengungkap tren dan wawasan.")
st.write("---")  # Separator

# Sidebar Information
st.sidebar.image("netflix_logo.png", use_column_width=True)  # Add Netflix logo
st.sidebar.title("About This Dashboard")
st.sidebar.write(
    """
    **Netflix Dataset Analysis Dashboard**  
    Dashboard ini dibuat untuk menganalisis dataset Netflix secara interaktif.  
    Anda dapat mengeksplorasi tren, kontribusi berdasarkan negara, genre, dan informasi lainnya yang terkait dengan film di platform Netflix.

    **Fitur Utama:**  
    - Analisis jumlah film berdasarkan periode waktu (harian, bulanan, tahunan).  
    - Tren perkembangan film berdasarkan tahun rilis.  
    - Sutradara, negara, genre, dan rating teratas.  
    - Daftar film dan durasi berdasarkan negara.
    """
)

# Load data
df = pd.read_csv("cleaned_netflix_data.csv")
df['date_added'] = pd.to_datetime(df['date_added'])

# Filter by Country
country_filter = st.sidebar.selectbox("Pilih Negara", ["Semua"] + df['country'].dropna().unique().tolist())
selected_country_title = f" di {country_filter}" if country_filter != "Semua" else ""

if country_filter != "Semua":
    df = df[df['country'].str.contains(country_filter, na=False)]

# Section 1: Film yang Ditambahkan Berdasarkan Periode Waktu
st.header("Penambahan Film Pada Platform Netflix Berdasarkan Periode Waktu")
period = st.radio("Pilih Periode Waktu:", ["Harian", "Bulanan", "Tahunan"], horizontal=True)
daily_added_df = create_daily_added_df(df, period)
fig1 = px.line(
    daily_added_df,
    x="date_added",
    y="title_count",
    title=f"Penambahan Film Periode Waktu: ({period}){selected_country_title}",
    text="title_count"
)
fig1.update_traces(textposition="top center")
st.plotly_chart(fig1)

# Section 2: Top Sutradara
st.header("Sutradara Terbaik Berdasarkan Judul yang Disutradarai")
top_directors_df = create_top_directors_df(df)
fig2 = px.bar(
    top_directors_df.head(10),
    x="film_count",
    y="director",
    orientation="h",
    title=f"Top 10 Directors{selected_country_title}",
    text="film_count"
)
fig2.update_traces(textposition="outside")
st.plotly_chart(fig2)

# Section 3: Top Negara
st.header("Negara Teratas Berdasarkan Judul yang Diproduksi")
top_countries_df = create_top_countries_df(df)
fig3 = px.bar(
    top_countries_df.head(10),
    x="film_count",
    y="country",
    orientation="h",
    title=f"Top 10 Countries{selected_country_title}",
    text="film_count"
)
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3)

# Section 4: Top Genre
st.header("Genre Teratas Berdasarkan Judul Film")
top_genres_df = create_top_genres_df(df)
fig4 = px.bar(
    top_genres_df.head(10),
    x="genre_count",
    y="listed_in",
    orientation="h",
    title=f"Top 10 Genres{selected_country_title}",
    text="genre_count"
)
fig4.update_traces(textposition="outside")
st.plotly_chart(fig4)

# Section 5: Distribusi Durasi Film
st.header("Distribusi Durasi Film di Netflix")
fig5 = px.histogram(
    df,
    x="duration(min)",
    nbins=20,
    title="Distribusi Durasi Film di Netflix",
    color_discrete_sequence=["#E50914"]
)
st.plotly_chart(fig5)

# Section 6: Peta Dunia Berdasarkan Produksi Film
st.header("Distribusi Negara Berdasarkan Jumlah Film di Netflix")
top_countries_df = create_top_countries_df(df)
fig6 = px.choropleth(
    top_countries_df,
    locations="country",
    locationmode="country names",
    color="film_count",
    title="Peta Dunia Berdasarkan Produksi Film",
    color_continuous_scale="reds"
)
st.plotly_chart(fig6)
