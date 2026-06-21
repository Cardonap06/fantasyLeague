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

    # Calcular puntos de cada equipo
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

    # Ordenar ranking
    ranking = sorted(
        ranking,
        key=lambda x: x["Puntos"],
        reverse=True
    )

    # Guardar/Actualizar ranking en MongoDB
    for posicion, item in enumerate(ranking, start=1):

        db.rankings.update_one(
            {
                "equipo": item["Equipo"]
            },
            {
                "$set": {
                    "posicion": posicion,
                    "manager": item["Manager"],
                    "equipo": item["Equipo"],
                    "puntosTotales": item["Puntos"]
                }
            },
            upsert=True
        )

    # Crear DataFrame para mostrar
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

    # Mostrar líder
    if len(df) >= 1:

        lider = df.iloc[0]

        st.success(
            f"🥇 Líder actual: {lider['Manager']} ({lider['Puntos']} pts)"
        )

