import streamlit as st
import pandas as pd


def ranking_page(db):
    st.header("🏆 Ranking de la liga")
    st.markdown("Consulta la tabla de posiciones de la Fantasy League ordenada por puntos.")

    ranking = list(db.rankings.find().sort("puntosTotales", -1))
    df = pd.DataFrame(ranking)

    if df.empty:
        st.info("No hay datos de ranking disponibles todavía.")
        return

    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    df = df.rename(
        columns={
            "nombre": "Nombre",
            "equipo": "Equipo",
            "puntosTotales": "Puntos totales",
            "posicion": "Posición en ranking",
        }
    )

    st.dataframe(df)
