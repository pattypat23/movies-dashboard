import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import json

# -------------------------
# CONEXIÓN A FIREBASE
# -------------------------
if not firebase_admin._apps:
    cred_dict = json.loads(st.secrets["firebase"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.write("Conectando Firestore...")

docs = list(db.collection("movies").stream())

st.write("Docs encontrados:", len(docs))
st.write(docs)


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

st.write("Total películas:", len(movies_df))
st.dataframe(movies_df)

# -------------------------
# SIDEBAR
# -------------------------
# movies_df.head()

st.sidebar.title("Filtros")

movie_name = st.sidebar.text_input("Buscar película")

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
st.title("Movies Dashboard")

# Mostrar todos
if st.sidebar.checkbox("Mostrar todas las películas"):
    st.header("Listado completo de películas")
    st.dataframe(movies_df)


