import streamlit as st
from pymongo import MongoClient
import pandas as pd
from equiposFantasy import equipos_fantasy_page

st.set_page_config(
    page_title="Fantasy League",
    page_icon="⚽",
    layout="wide"
)

client = MongoClient("mongodb://localhost:27017")
#db = client["Fantasyleague"]    #isabella
db = client["fantasyLeague"]     #sara

st.sidebar.title("⚽ Fantasy League")

opcion = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "Inicio",
        "Usuarios",
        "Jugadores",
        "Ranking",
        "Equipos Fantasy",
        "Estadísticas"
    ]
)

if opcion == "Inicio":

    st.title("⚽ Fantasy League")

    st.write(
        """
        Plataforma Fantasy League basada en MongoDB.
        Proyecto Final NoSQL.
        """
    )

elif opcion == "Usuarios":

    st.subheader("Registrar Usuario")

    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")
    pais = st.text_input("País")

    if st.button("Registrar"):

        if nombre and correo and pais:

            resultado = db.usuarios.insert_one({
                "nombre": nombre,
                "correo": correo,
                "pais": pais
            })

            st.success("Usuario registrado correctamente")
            st.write("ID generado:", resultado.inserted_id)

        else:
            st.error("Complete todos los campos")

    st.header("Usuarios")

    usuarios = list(db.usuarios.find())

    df = pd.DataFrame(usuarios)

    if not df.empty:

        if "_id" in df.columns:
            df["_id"] = df["_id"].astype(str)

        st.dataframe(df)

elif opcion == "Jugadores":

    st.header("⚽ Jugadores")

    jugadores = list(
        db.jugadores.find().sort(
            "puntosTotales",
            -1
        )
    )

    df = pd.DataFrame(jugadores)

    if not df.empty:

        if "_id" in df.columns:
            df = df.drop("_id", axis=1)

        st.dataframe(df)

elif opcion == "Ranking":

    st.header("🏆 Ranking")

    ranking = list(
        db.rankings.find().sort(
            "puntosTotales",
            -1
        )
    )

    df = pd.DataFrame(ranking)

    if not df.empty:

        if "_id" in df.columns:
            df = df.drop("_id", axis=1)

        st.dataframe(df)

elif opcion == "Equipos Fantasy":
    equipos_fantasy_page(db)

elif opcion == "Estadísticas":

    st.header("📊 Estadísticas MongoDB")

    st.info(
        "Esta sección utiliza Aggregation Framework de MongoDB ($match, $sort y $limit)."
    )

    st.subheader("Jugadores con más de 100 puntos")

    resultado = list(
        db.jugadores.aggregate([
            {
                "$match": {
                    "puntosTotales": {
                        "$gt": 100
                    }
                }
            }
        ])
    )

    df = pd.DataFrame(resultado)

    if not df.empty:

        if "_id" in df.columns:
            df = df.drop("_id", axis=1)

        st.dataframe(df)

    st.subheader("Top 3 Jugadores")

    top3 = list(
        db.jugadores.aggregate([
            {
                "$sort": {
                    "puntosTotales": -1
                }
            },
            {
                "$limit": 3
            }
        ])
    )

    df_top3 = pd.DataFrame(top3)

    if not df_top3.empty:

        if "_id" in df_top3.columns:
            df_top3 = df_top3.drop("_id", axis=1)

        st.dataframe(df_top3)