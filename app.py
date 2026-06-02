import streamlit as st
import pandas as pd
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
st.title("Mi app de películas")

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


