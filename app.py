import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import json

# -------------------------
# CONEXIÓN A FIREBASE
# -------------------------
#if not firebase_admin._apps:
 #   cred_dict = json.loads(st.secrets["firebase"])
 #   cred = credentials.Certificate(cred_dict)
 #   firebase_admin.initialize_app(cred)

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)


db = firestore.client()

#st.write("Intentando leer Firestore...")
#docs = db.collection("movies").limit(5).stream()
#docs_list = list(docs)
#st.write("Docs encontrados:", len(docs_list))
#st.write(docs_list)


# -------------------------
# FUNCION PARA CARGAR DATOS
# -------------------------

st.title("Aplicación de películas")

def load_movies():
    docs = db.collection("movies").stream()
    movies = []
    
    for doc in docs:
         movies.append(doc.to_dict())
        
    return pd.DataFrame(movies)

movies_df = load_movies()

# DEBUG (no me sale)

#st.write("Total películas:", len(movies_df))
#st.dataframe(movies_df)

# -------------------------
# SIDEBAR
# -------------------------
# movies_df.head()

st.sidebar.title("Filtros")
st.sidebar.subheader("Buscar película")
movie_name = st.sidebar.text_input("Ingrese parte del título de la Película")

# -------------------------
# BUSQUEDA
# -------------------------

if st.sidebar.button("Buscar"):
    result = movies_df[movies_df["name"].str.contains(movie_name, case=False, na=False ) ]
    st.subheader("Resultados")
    st.dataframe(result)
else:
    st.warning("Escribe un nombre para buscar")

st.dataframe(movies_df.head())

# Mostrar todos
if st.sidebar.checkbox("Mostrar todas las películas"):
    st.header("Listado completo de películas")
    st.dataframe(movies_df)

# Filtrar por director

def search_by_director(director):
    return movies_df[movies_df["director"] == director]
 
st.sidebar.subheader("Filtrar por director")

if movies_df is not None and not movies_df.empty and "director" in movies_df.columns:
 
directors = sorted(movies_df["director"].unique())
selected_director = st.sidebar.selectbox("Director",directors)

if st.sidebar.button("Filtrar director"):
    result = search_by_director(selected_director)
    st.write(f"Total encontrados: {len(result)}")
    st.dataframe(result)

else:
    st.sidebar.warning("No hay datos de directores disponibles")
st.sidebar.subheader("Nuevo filme")

# Agregar nueva Película

with st.sidebar.form("movie_form"):
    company = st.text_input("Company")
    director = st.text_input("Director")
    genre = st.text_input("Genre")
    name = st.text_input("Movie Name")
    submit = st.form_submit_button("Guardar")

    if submit:
        db.collection("movies").add({
            "company": company,
            "director": director,
            "genre": genre,
            "name": name})

        st.success("Película agregada")




