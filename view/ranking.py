import streamlit as st
import pandas as pd


def ranking_page(db):

    st.header("🏆 Ranking de la Liga")
    st.markdown(
        "Clasificación de managers según los puntos acumulados por los jugadores de sus equipos."
    )

    equipos = list(db.equiposFantasy.find())

    if not equipos:
        st.info("No hay equipos fantasy registrados.")
        return

    ranking = []

    for equipo in equipos:

        puntos_equipo = 0

        for jugador_equipo in equipo.get("jugadores", []):

            jugador_db = db.jugadores.find_one(
                {
                    "nombre": jugador_equipo.get("nombre")
                }
            )

            if jugador_db:

                puntos_equipo += jugador_db.get(
                    "puntosTotales",
                    0
                )

        ranking.append(
            {
                "Manager": equipo.get(
                    "usuario",
                    "Sin manager"
                ),
                "Equipo": equipo.get(
                    "nombreEquipo",
                    "Sin nombre"
                ),
                "Puntos": puntos_equipo
            }
        )

    ranking = sorted(
        ranking,
        key=lambda x: x["Puntos"],
        reverse=True
    )

    df = pd.DataFrame(ranking)

    df.insert(
        0,
        "Posición",
        range(
            1,
            len(df) + 1
        )
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    if len(df) >= 1:
        st.success(
            f"🥇 Líder actual: {df.iloc[0]['Manager']} ({df.iloc[0]['Puntos']} pts)"
        )