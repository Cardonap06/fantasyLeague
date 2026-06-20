import streamlit as st
import pandas as pd


def partidos_page(db):
    st.header("⚽ Partidos")

    # Intentamos ordenar por jornada y fecha; si faltan campos, se muestran igualmente
    try:
        partidos = list(db.partidos.find().sort([("jornada", 1), ("fecha", 1)]))
    except Exception:
        partidos = list(db.partidos.find())

    if not partidos:
        st.info("No hay partidos registrados.")
        return

    # Agrupar por jornada (soporta varios nombres de campo posibles)
    agrupado = {}
    for p in partidos:
        j = p.get("jornada") or p.get("numeroJornada") or p.get("numero") or "Sin jornada"
        agrupado.setdefault(j, []).append(p)

    for jornada, matches in agrupado.items():
        st.subheader(f"Jornada {jornada}")


        jornada_doc = db.jornadas.find_one(
            {"numero": jornada}
        )

        if jornada_doc:
            st.caption(
                f"📅 Fecha: {jornada_doc['fecha']}"
            )

        rows = []
        for m in matches:
            local = m.get("equipoLocal") or m.get("local") or m.get("equipo_local") or m.get("home") or "Local"
            visitante = m.get("equipoVisitante") or m.get("visitante") or m.get("equipo_visitante") or m.get("away") or "Visitante"
            goles_local = m.get("golesLocal") if m.get("golesLocal") is not None else m.get("goles_local", "")
            goles_visit = m.get("golesVisitante") if m.get("golesVisitante") is not None else m.get("goles_visitante", "")
            rows.append({
                "Local": local,
                "Visitante": visitante,
                "Goles Local": goles_local,
                "Goles Visitante": goles_visit
            })

        df = pd.DataFrame(rows)
        if df.empty:
            st.write("No hay datos para esta jornada.")
        else:
            st.table(df)

        st.divider()
