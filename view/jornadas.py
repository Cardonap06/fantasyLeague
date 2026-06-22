import streamlit as st
import pandas as pd


def jornadas_page(db):
    st.header("📅 Jornadas")


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
                        st.rerun()

    st.divider()


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
