import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Set the page configuration first
st.set_page_config(page_title="Netflix Dataset Analysis", page_icon="📺", layout="wide")

# Helper functions for the Netflix dataset
def create_daily_added_df(df, period):
    """Aggregate data by daily, monthly, or yearly additions of titles."""
    if period == "Harian":
        daily_added_df = df.resample(rule='D', on='date_added').agg({
            "show_id": "nunique"
        })
    elif period == "Bulanan":
        daily_added_df = df.resample(rule='M', on='date_added').agg({
            "show_id": "nunique"
        })
    elif period == "Tahunan":
        daily_added_df = df.resample(rule='Y', on='date_added').agg({
            "show_id": "nunique"
        })
    daily_added_df = daily_added_df.reset_index()
    daily_added_df.rename(columns={
        "show_id": "title_count"
    }, inplace=True)
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

def create_top_rating_df(df):
    df['rating'] = df['rating'].str.split(', ')
    exploded_rating = df.explode('rating')
    top_rating = (
        exploded_rating.groupby('rating')['title']
        .nunique()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={'title': 'rating_count'})
    )
    return top_rating

# Set default theme and colors
px.defaults.template = "plotly_dark"  # Theme
px.defaults.color_discrete_sequence = ["#E50914", "#221F1F", "#B1B1B1"]  # Netflix theme colors

# Streamlit App
# Sidebar Information
st.sidebar.image("netflix_logo.png", use_column_width=True)  # Add Netflix logo
st.sidebar.write("# Filter Data")
# st.sidebar.title("About This Dashboard")
# st.sidebar.write(
#     """
#     **Netflix Dataset Analysis Dashboard**  
#     Dashboard ini dibuat untuk menganalisis dataset Netflix secara interaktif.  
#     Anda dapat mengeksplorasi tren, kontribusi berdasarkan negara, genre, dan informasi lainnya yang terkait dengan film di platform Netflix.

#     **Fitur Utama:**  
#     - Analisis jumlah film berdasarkan periode waktu (harian, bulanan, tahunan).  
#     - Tren perkembangan film berdasarkan tahun rilis.  
#     - Sutradara, negara, genre, dan rating teratas.  
#     - Daftar film dan durasi berdasarkan negara.
#     """
# )

# Title
st.image("logo_netflix.png", use_column_width=False, width=200)  # Add Netflix logo 
st.title("Netflix Dataset Analysis")
st.write("Jelajahi kumpulan data Netflix secara interaktif untuk mengungkap tren dan wawasan.")

# Tabs Creation
tab1, tab2, tab3 = st.tabs(["📋 Informasi Data", "📊 Dashboard Data", "👥 Our Team"])

# Load data
df = pd.read_csv("cleaned_netflix_data.csv")

# Convert date_added to datetime
df['date_added'] = pd.to_datetime(df['date_added'])

# Filter by Country (Global Filter)
country_filter = st.sidebar.selectbox("Pilih Negara", ["Semua"] + df['country'].dropna().unique().tolist())
selected_country_title = f" di {country_filter}" if country_filter != "Semua" else ""

if country_filter != "Semua":
    df = df[df['country'].str.contains(country_filter, na=False)]

with tab1:
    st.write("## Tentang Dashboard ini")
    st.write(
        """
        **Netflix Dataset Analysis Dashboard**\n
        Dashboard ini dibuat untuk menganalisis dataset Netflix secara interaktif.
        Anda dapat mengeksplorasi tren, kontribusi berdasarkan negara, genre, dan informasi lainnya yang terkait dengan film di platform Netflix.
        
        **Fitur Utama:**  
        - Analisis jumlah film berdasarkan periode waktu (harian, bulanan, tahunan).  
        - Tren perkembangan film berdasarkan tahun rilis.  
        - Sutradara, negara, genre, dan rating teratas.  
        - Daftar film dan durasi berdasarkan negara.
        """
    )
    st.write("---")  # Separator
    st.markdown("""
        | No.| Tujuan Visualisasi | Jenis Visualisasi | Deskripsi |
        |----|--------------------|-------------------|-----------|
        | 1. | Menampilkan pola atau tren penambahan film berdasarkan periode waktu  | Trend Line | Menunjukkan jumlah film yang ditambahkan ke Netflix dalam rentang waktu yang dipilih (harian, bulanan, atau tahunan). |
        | 2. | Menampilkan tren produksi film berdasarkan tahun rilisnya | Trend Line   | Membantu memahami apakah ada peningkatan atau penurunan produksi film dari tahun ke tahun. |
        | 3. | Menampilkan daftar Sutradara dengan jumlah film terbanyak di Netflix | Bar Chart  | Menunjukkan siapa saja Sutradara paling produktif atau yang memiliki kontribusi besar di platform Netflix. |
        | 4. | Menampilkan daftar Negara dengan jumlah film terbanyak di Netflix | Bar Chart  | Menunjukkan Negara mana yang paling produktif atau yang memiliki kontribusi besar di platform Netflix. |
        | 5. | Menampilkan daftar Genre dengan jumlah film terbanyak di Netflix | Bar Chart  | Menunjukkan Genre apa saja yang paling banyak pada platform Netflix. |
        | 6. | Menampilkan daftar Rating dengan jumlah film terbanyak di Netflix | Bar Chart  | Menunjukkan Rating mana saja yang paling umum pada platform Netflix. |
        | 7. | Menampilkan informasi daftar judul film dan durasinya yang diproduksi oleh negara tertentu | Tabel Data  | Tabel ini menampilkan film beserta durasinya, diurutkan dari yang durasinya paling lama. |
    """)

with tab2:

    # # Total films
    # total_films = df['title'].nunique()
    # st.metric("🎥 Total Film", f"{total_films} film")

    # # Durasi Film Terpanjang
    # if 'duration(min)' in df.columns:
    #     longest_film = df.sort_values(by='duration(min)', ascending=False).iloc[0]
    #     st.metric("⏳ Film Terpanjang", f"{longest_film['title']}", f"{longest_film['duration(min)']} menit")

    # # Top director
    # top_directors_df = create_top_directors_df(df)
    # top_director = top_directors_df.iloc[0]
    # st.metric("🎬 Top Sutradara", f"{top_director['director']}", f"{top_director['film_count']} film")

    # # Top genre
    # top_genres_df = create_top_genres_df(df)
    # top_genre = top_genres_df.iloc[0]
    # st.metric("📂 Top Genre", f"{top_genre['listed_in']}", f"{top_genre['genre_count']} film")

    # # Top rating
    # top_rating_df = create_top_rating_df(df)
    # top_rating = top_rating_df.iloc[0]
    # st.metric("⭐ Top Rating", f"{top_rating['rating']}", f"{top_rating['rating_count']} film")

    # st.write("---")  # Separator

    st.markdown("## Visualisasi Data")

    # Section 1: Judul film harian, bulanan dan tahunan yang ditambahkan
    st.header("Penambahan Film Pada Platform Netflix Berdasarkan Periode Waktu")
    period = st.radio("Pilih Periode Waktu:", ["Harian", "Bulanan", "Tahunan"], horizontal=True)
    daily_added_df = create_daily_added_df(df, period)
    fig1 = px.line(
        daily_added_df,
        x="date_added",
        y="title_count",
        title=f"📈 Penambahan Film Periode Waktu: ({period}){selected_country_title}",
        text="title_count"
    )
    fig1.update_traces(textposition="top center")
    st.plotly_chart(fig1)

    # Section 2: Produksi film berdasarkan tahun rilis
    st.header("Produksi film berdasarkan tahun rilis")
    unique_titles_df = df.drop_duplicates(subset='title')
    release_year_df = (
        unique_titles_df.groupby("release_year")["title"]
        .count()
        .reset_index()
        .rename(columns={"title": "title_count"})
    )
    fig5 = px.line(
        release_year_df,
        x="release_year",
        y="title_count",
        title=f"📈 Produksi film berdasarkan tahun rilis{selected_country_title}",
        text="title_count"
    )
    fig5.update_traces(textposition="top center")
    st.plotly_chart(fig5)

    col1, col2 = st.columns(2)

    with col1:
        # Section 3: Top Sutradara
        st.header("Sutradara Terbaik Berdasarkan Judul yang Disutradarai")
        top_directors_df = create_top_directors_df(df)
        fig2 = px.bar(
            top_directors_df.head(10),
            x="film_count",
            y="director",
            orientation="h",
            title=f"🌟 Top 10 Directors{selected_country_title}",
            text="film_count"
        )
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2)

    with col2:
        # Section 4: Top Negara
        st.header("Negara Teratas Berdasarkan Judul yang Diproduksi")
        top_countries_df = create_top_countries_df(df)
        fig3 = px.bar(
            top_countries_df.head(10),
            x="film_count",
            y="country",
            orientation="h",
            title=f"🌟 Top 10 Countries{selected_country_title}",
            text="film_count"
        )
        fig3.update_traces(textposition="outside")
        st.plotly_chart(fig3)

    col1, col2 = st.columns(2)

    with col1:
        # Section 5: Top Genre
        st.header("Genre Teratas Berdasarkan Judul Film")
        top_genres_df = create_top_genres_df(df)
        fig4 = px.bar(
            top_genres_df.head(10),
            x="genre_count",
            y="listed_in",
            orientation="h",
            title=f"🌟 Top 10 Genres{selected_country_title}",
            text="genre_count"
        )
        fig4.update_traces(textposition="outside")
        st.plotly_chart(fig4)

    with col2:
        # Section 6: Jumlah Film Berdasarkan Rating
        st.header("Jumlah Film Berdasarkan Rating")
        top_rating_df = create_top_rating_df(df)
        fig6 = px.bar(
            top_rating_df.head(10),
            x="rating_count",
            y="rating",
            orientation="h",
            title=f"🌟 Top 10 Ratings{selected_country_title}",
            text="rating_count"
        )
        fig6.update_traces(textposition="outside")
        st.plotly_chart(fig6)


    # Section 7: Daftar Film dan Durasi Berdasarkan Negara
    st.header(f"Daftar Film dan Durasi Berdasarkan Negara{selected_country_title}")
    if country_filter != "All":
    # Hilangkan duplikasi berdasarkan kolom 'title'
        film_list = (
            df[['title', 'duration(min)']]
            .dropna()
            .drop_duplicates(subset='title')
            .sort_values(by='duration(min)', ascending=False)
        )
    # Reset index dan hapus indeks pojok kiri
        st.dataframe(film_list.reset_index(drop=True), use_container_width=True)


with tab3:
    st.write("## Kelompok Bug Busters")
    st.write("""
    - Muhammad Rizki Arya Rifai 
    - Alhafidz William Adzantha 
    - Muhammad Naufal Firdaus 
    - Alfian Nursahbani 
    """)