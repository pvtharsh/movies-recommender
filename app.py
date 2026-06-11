import pickle
import streamlit as st
import requests

st.set_page_config(page_title="CineVerse", page_icon="🎬", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600;700&family=Cinzel+Decorative:wght@700;900&display=swap');

* { font-family: 'Rajdhani', sans-serif; }
.stApp { background-color: #141414; }

.navbar {
    background: rgba(0,0,0,0.95);
    padding: 14px 48px;
    display: flex;
    align-items: center;
    gap: 32px;
    margin-bottom: 0;
    border-bottom: 1px solid #222;
}
.logo-wrap { display: flex; align-items: center; gap: 10px; }
.logo-icon {
    width: 38px; height: 38px;
    background: #E50914;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 14px; font-weight: 900;
    color: white;
}
.logo-text {
    font-family: 'Orbitron', sans-serif;
    font-size: 20px; font-weight: 900;
    color: white; letter-spacing: 3px;
}
.logo-text span { color: #E50914; }
.nav-links { display: flex; gap: 24px; }
.nav-links a {
    color: #e5e5e5; text-decoration: none;
    font-size: 13px; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
}
.hero {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a0d2e 40%, #0d1a3a 100%);
    padding: 64px 40px 48px;
    text-align: center;
}
.hero-eyebrow {
    font-size: 16px; letter-spacing: 6px;
    color: #E50914; text-transform: uppercase;
    margin-bottom: 16px; font-weight: 600;
}
.hero-title {
    font-family: 'Cinzel Decorative', cursive;
    font-size: 64px; font-weight: 900;
    letter-spacing: 8px; margin-bottom: 12px;
    color: white;
}
.hero-title span { color: #E50914; }
.hero-subtitle {
    font-size: 13px; letter-spacing: 4px;
    color: #aaaaaa; text-transform: uppercase;
    margin-bottom: 0;
}
.section-title {
    font-family: 'Orbitron', sans-serif;
    color: white; font-size: 16px;
    font-weight: 700; letter-spacing: 2px;
    border-left: 4px solid #E50914;
    padding-left: 12px; margin: 32px 0 16px 0;
}
.movie-name {
    color: #e5e5e5; font-size: 12px;
    font-weight: 700; text-align: center;
    margin-top: 6px; letter-spacing: 0.5px;
}
.stSelectbox > div > div {
    background: rgba(30,30,30,0.9) !important;
    border: 1.5px solid #E50914 !important;
    border-radius: 8px !important;
    color: white !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
}
.stButton > button {
    background: #E50914 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 48px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #b20710 !important;
    transform: scale(1.02) !important;
}
.stImage img {
    border-radius: 8px !important;
    transition: transform 0.3s ease !important;
    width: 100% !important;
}
.stImage img:hover {
    transform: scale(1.05) translateY(-4px) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding-top: 0 !important; }
</style>

<div class="navbar">
    <div class="logo-wrap">
        <div class="logo-icon">CV</div>
        <div class="logo-text">CINE<span>VERSE</span></div>
    </div>
    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">Top Rated</a>
        <a href="#">Genres</a>
        <a href="#">About</a>
    </div>
</div>

<div class="hero">
    <div class="hero-eyebrow">✦ Powered by Machine Learning ✦</div>
    <div class="hero-title">CINE<span>VERSE</span></div>
    <div class="hero-subtitle">Discover Your Next Favorite Movie</div>
</div>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=3fa83035dbcf11896708ba3c773ea23b&language=en-US".format(movie_id)
        data = requests.get(url, timeout=5).json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    names, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        posters.append(fetch_poster(movie_id))
        names.append(movies.iloc[i[0]].title)
    return names, posters


@st.cache_data
def load_data():
    movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))
    return movies, similarity


movies, similarity = load_data()
movie_list = movies['title'].values

col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    selected_movie = st.selectbox('🎬 Search a Movie', movie_list)

col_x, col_y, col_z = st.columns([1.5, 1, 1.5])
with col_y:
    show_btn = st.button('▶  GET RECOMMENDATIONS')

if show_btn:
    names, posters = recommend(selected_movie)
    st.markdown('<div class="section-title">TOP PICKS FOR YOU</div>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    for col, name, poster in zip([col1,col2,col3,col4,col5], names, posters):
        with col:
            st.image(poster)
            st.markdown(f'<p class="movie-name">{name}</p>', unsafe_allow_html=True)

st.markdown("""
<div style="background:#0a0a0a; border-top:1px solid #222; padding:24px; text-align:center; margin-top:60px;">
    <div style="font-family:'Cinzel Decorative',cursive; font-size:16px; font-weight:900; letter-spacing:4px; margin-bottom:8px;">
        CINE<span style="color:#E50914;">VERSE</span>
    </div>
    <div style="color:#aaa; font-size:12px; letter-spacing:1px;">
        © 2024 CineVerse &nbsp;|&nbsp; Developed by <span style="color:#E50914;">Harsh</span> &nbsp;|&nbsp; All Rights Reserved
    </div>
</div>
""", unsafe_allow_html=True)