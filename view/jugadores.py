import streamlit as st


def jugadores_page(db):
    st.header("⚽ Jugadores disponibles")
    st.markdown("Selecciona jugadores para armar tu equipo. Los jugadores vienen del torneo oficial; aquí solo se muestran como tarjetas.")

    jugadores = list(db.jugadores.find().sort("puntosTotales", -1))

    if not jugadores:
        st.info("No hay jugadores cargados todavía.")
        return

    placeholder_image = "https://via.placeholder.com/150?text=Jugador"

    # Mostrar tarjetas en filas de 3 columnas
    per_row = 3
    for i in range(0, len(jugadores), per_row):
        row_items = jugadores[i : i + per_row]
        cols = st.columns(per_row)
        for col, jugador in zip(cols, row_items):
            with col:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    img_url = jugador.get("imagen") or placeholder_image
                    with col1:
                        try:
                            st.image(img_url, width=120)
                        except Exception:
                            st.image(placeholder_image, width=120)

                    with col2:
                        st.subheader(jugador.get("nombre", "Sin nombre"))
                        st.write(f"🏟️ Equipo: {jugador.get('equipo', '-')}")
                        st.write(f"⚽ Posición: {jugador.get('posicion', '-')}")
                        st.write(f"🏆 Puntos: {jugador.get('puntosTotales', 0)}")

                    st.markdown("---")
    
