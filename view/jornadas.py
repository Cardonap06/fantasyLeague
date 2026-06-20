import streamlit as st


def jornadas_page(db):
    st.header("📅 Jornadas")

    jornadas = list(db.jornadas.find().sort("numero", 1))
    if not jornadas:
        st.info("No hay jornadas registradas.")
        return

    cols = st.columns(3)
    for i, jornada in enumerate(jornadas):
        col = cols[i % 3]
        numero = jornada.get("numero", "N/A")
        descripcion = jornada.get("descripcion", "")
        fecha = jornada.get("fecha", "")
        estado = jornada.get("estado", "")
        with col:
            st.markdown(
                f"""
                <div style="border:1px solid #ddd;padding:12px;border-radius:8px;background:#f8f9fa;color:#000;margin-bottom:8px">
                <h4 style="margin:0">Jornada {numero}</h4>
                <p style="margin:4px 0">{descripcion}</p>
                <small>Fecha: {fecha} — Estado: {estado}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
