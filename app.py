import streamlit as st
import pandas as pd
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
st.title("Mi app de películas")

if not firebase_admin._apps:
    cred = credentials.Certificate("movies-dashboard-90974-firebase-adminsdk-fbsvc-165b996a5d.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

def load_movies():
    docs = db.collection("movies").stream()
    movies = []
    for doc in docs:
     movies.append(doc.to_dict())
    return pd.DataFrame(movies)
    movies_df = load_movies()
    movies_df.head()
    st.title("Movies Dashboard")
if st.sidebar.checkbox("Mostrar todos los filmes"):
    st.header("Listado completo de filmes")
    st.dataframe(movies_df)
    st.sidebar.subheader("Buscar película")
    movie_name = st.sidebar.text_input("Ingrese parte del título")

if st.sidebar.button("Buscar"):
    result = movies_df[movies_df["name"].str.contains(
    movie_name,
    case=False,
    na=False ) ]
    st.subheader("Resultados")
    st.dataframe(result)

def search_by_director(director):return movies_df[ movies_df["director"] == director ]
st.sidebar.subheader("Filtrar por director")
directors = sorted(movies_df["director"].unique())
selected_director = st.sidebar.selectbox( "Director",  directors)

if st.sidebar.button("Filtrar director"):
    result = search_by_director( selected_director  )
    st.write(   f"Total encontrados: {len(result)}"  )
    st.dataframe(result)
    st.sidebar.subheader( "Nuevo filme")

with st.sidebar.form("movie_form"):
    company = st.text_input("Company")
    director = st.text_input("Director")
    genre = st.text_input("Genre")
    name = st.text_input("Movie Name")
    submit = st.form_submit_button(  "Guardar" )

if submit:
    db.collection("movies").add({
            "company": company,
            "director": director,
            "genre": genre,
            "name": name  })
st.success( "Película agregada"  )
