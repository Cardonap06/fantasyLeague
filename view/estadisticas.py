import streamlit as st
import pandas as pd


def estadisticas_page(db):
    st.header("📊 Estadísticas")
    st.info("Esta sección muestra consultas avanzadas usando MongoDB Aggregation Framework.")

    st.subheader("Jugadores con más de 100 puntos")
    resultado = list(
        db.jugadores.aggregate(
            [{"$match": {"puntosTotales": {"$gt": 100}}}]
        )
    )
    df = pd.DataFrame(resultado)

    if df.empty:
        st.warning("No hay jugadores con más de 100 puntos registrados aún.")
    else:
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])
        st.dataframe(df)

    st.divider()
    st.subheader("Top 3 jugadores")
    top3 = list(
        db.jugadores.aggregate(
            [{"$sort": {"puntosTotales": -1}}, {"$limit": 3}]
        )
    )
    df_top3 = pd.DataFrame(top3)

    if df_top3.empty:
        st.warning("No hay jugadores para mostrar en el ranking.")
    else:
        if "_id" in df_top3.columns:
            df_top3 = df_top3.drop(columns=["_id"])
        st.dataframe(df_top3)

    st.divider()
    st.subheader("Registrar estadísticas de un jugador")

    jugadores = list(db.jugadores.find().sort("puntosTotales", -1))
    jugadores_nombres = [jugador.get("nombre") for jugador in jugadores if jugador.get("nombre")]

    with st.form("estadisticas_form", clear_on_submit=True):
        jugador_estadistica = st.selectbox("Jugador", [""] + jugadores_nombres)
        goles = st.number_input("Goles", min_value=0, value=0)
        asistencias = st.number_input("Asistencias", min_value=0, value=0)
        tarjetas_amarillas = st.number_input("Tarjetas amarillas", min_value=0, value=0)
        tarjetas_rojas = st.number_input("Tarjetas rojas", min_value=0, value=0)
        fecha = st.date_input("Fecha de la jornada")
        guardar_estadistica = st.form_submit_button("Registrar estadísticas")

        if guardar_estadistica:
            if not jugador_estadistica:
                st.error("Selecciona un jugador para registrar las estadísticas.")
            else:
                db.estadisticas.insert_one({
                    "jugador": jugador_estadistica,
                    "goles": int(goles),
                    "asistencias": int(asistencias),
                    "tarjetasAmarillas": int(tarjetas_amarillas),
                    "tarjetasRojas": int(tarjetas_rojas),
                    "fecha": str(fecha),
                })
                st.success("Estadísticas registradas correctamente.")

    st.divider()
    st.subheader("Consultar estadísticas de un jugador")

    jugador_consulta = st.selectbox("Jugador para consultar", [""] + jugadores_nombres, key="jugador_consulta")
    if jugador_consulta:
        estadisticas_jugador = list(db.estadisticas.find({"jugador": jugador_consulta}).sort("fecha", -1))
        df_estadisticas = pd.DataFrame(estadisticas_jugador)
        if df_estadisticas.empty:
            st.info("No hay estadísticas registradas para este jugador.")
        else:
            if "_id" in df_estadisticas.columns:
                df_estadisticas = df_estadisticas.drop(columns=["_id"])
            df_estadisticas = df_estadisticas.rename(
                columns={
                    "jugador": "Jugador",
                    "goles": "Goles",
                    "asistencias": "Asistencias",
                    "tarjetasAmarillas": "Tarjetas amarillas",
                    "tarjetasRojas": "Tarjetas rojas",
                    "fecha": "Fecha",
                }
            )
            st.dataframe(df_estadisticas)

    st.divider()
    st.subheader("Crear jornada fantasy")

    with st.form("jornada_form", clear_on_submit=True):
        numero = st.number_input("Número de jornada", min_value=1, value=1)
        descripcion = st.text_input("Descripción")
        fecha_jornada = st.date_input("Fecha de la jornada")
        estado = st.selectbox("Estado", ["Programada", "Finalizada", "En curso"])
        crear_jornada = st.form_submit_button("Crear jornada")

        if crear_jornada:
            if not descripcion:
                st.error("Agrega una descripción para la jornada.")
            else:
                db.jornadas.insert_one({
                    "numero": int(numero),
                    "descripcion": descripcion,
                    "fecha": str(fecha_jornada),
                    "estado": estado,
                })
                st.success("Jornada fantasy creada correctamente.")

    st.divider()
    st.subheader("Jornadas fantasy registradas")

    jornadas = list(db.jornadas.find().sort("numero", 1))
    df_jornadas = pd.DataFrame(jornadas)
    if df_jornadas.empty:
        st.info("No hay jornadas registradas todavía.")
    else:
        if "_id" in df_jornadas.columns:
            df_jornadas = df_jornadas.drop(columns=["_id"])
        df_jornadas = df_jornadas.rename(
            columns={"numero": "Jornada", "descripcion": "Descripción", "fecha": "Fecha", "estado": "Estado"}
        )
        st.dataframe(df_jornadas)
