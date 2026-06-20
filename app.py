import streamlit as st
from pymongo import MongoClient
from PIL import Image

try:
    from fantasyLeague.view.equiposFantasy import equipos_fantasy_page
    from fantasyLeague.view.usuarios import usuarios_page
    from fantasyLeague.view.jugadores import jugadores_page
    from fantasyLeague.view.ranking import ranking_page
    from fantasyLeague.view.estadisticas import estadisticas_page
    from fantasyLeague.view.partidos import partidos_page
    from fantasyLeague.view.jornadas import jornadas_page
except ImportError:
    from view.equiposFantasy import equipos_fantasy_page
    from view.usuarios import usuarios_page
    from view.jugadores import jugadores_page
    from view.ranking import ranking_page
    from view.estadisticas import estadisticas_page
    from view.partidos import partidos_page
    from view.jornadas import jornadas_page

icon = Image.open("icon.png")

st.set_page_config(
    page_title="Fantasy League",
    page_icon=icon,
    layout="wide"
)

st.markdown(
    """
    <style>
    div[role="radiogroup"] label {
        font-size: 22px !important;
        font-weight: 600 !important;
        padding: 10px 0 !important;
    }

    [data-testid="stSidebar"] h1 {
        font-size: 42px !important;
    }

    [data-testid="stSidebar"] {
    background-color: #1C1F2E;
    }

    .stApp {
        background: linear-gradient(
            180deg,
            #0A1F44 0%,
            #14213D 100%
        );
        color: #ffffff;
    }

    .css-1d391kg, .css-1d391kg span {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

client = MongoClient("mongodb://localhost:27017")
db = client["FantasyLeague"]

st.sidebar.title("Fantasy League ⚽")
st.sidebar.markdown("---")

opcion = st.sidebar.radio(
    "Menú",
    [
        "Inicio",
        "Usuarios",
        "Jugadores",
        "Equipos Fantasy",
        "Partidos",
        "Jornadas",
        "Estadísticas",
        "Ranking"
    ],
)

st.sidebar.markdown("---")

if opcion == "Inicio":
    st.title("Fantasy League")
    st.markdown(
        """
        Bienvenido a la plataforma Fantasy League. Aquí puedes gestionar usuarios,
        crear jugadores, armar equipos fantasy y revisar estadísticas reales del torneo.
        """
    )
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👤 Usuarios registrados", db.usuarios.count_documents({}))
    col2.metric("⚽ Jugadores en la base", db.jugadores.count_documents({}))
    col3.metric("🏟️ Equipos fantasy", db.equiposFantasy.count_documents({}))
    col4.metric("🏆 Partidos analizados", db.partidos.count_documents({}))

    st.divider()

    col_izq, col_der = st.columns(2)
    with col_izq:
        st.subheader("Top 3 jugadores")
        top_jugadores = list(
            db.jugadores.aggregate([
                {"$sort": {"puntosTotales": -1}},
                {"$limit": 3}
            ])
        )
        if top_jugadores:
            for jugador in top_jugadores:
                st.write(f"⚽ {jugador.get('nombre', 'Sin nombre')} — {jugador.get('puntosTotales', 0)} pts")
        else:
            st.info("No hay jugadores registrados aún.")

    # Mostrar últimos 3 partidos debajo del Top 3 jugadores
    with col_izq:
        st.subheader("Últimos 3 partidos")
        try:
            ultimos = list(db.partidos.find().sort("fecha", -1).limit(3))
        except Exception:
            ultimos = list(db.partidos.find().sort([("_id", -1)]).limit(3))

        if ultimos:
            for p in ultimos:
                local = p.get("equipoLocal") or p.get("local") or "Local"
                visit = p.get("equipoVisitante") or p.get("visitante") or "Visitante"
                goles_local = p.get("golesLocal") if p.get("golesLocal") is not None else p.get("goles_local", "")
                goles_visit = p.get("golesVisitante") if p.get("golesVisitante") is not None else p.get("goles_visitante", "")
                fecha = p.get("fecha", "")
                st.write(f"{fecha} — {local} {goles_local} : {goles_visit} {visit}")
        else:
            st.info("No hay partidos registrados aún.")

    with col_der:
        st.subheader("Equipos activos")
        equipos = list(db.equiposFantasy.find())
        if equipos:
            for equipo in equipos:
                st.write(f"🏆 {equipo.get('nombreEquipo', 'Equipo sin nombre')}")
        else:
            st.info("No hay equipos fantasy creados todavía.")

    st.divider()
    st.success("Visualiza y administra tu liga con estadísticas en tiempo real desde MongoDB.")

elif opcion == "Usuarios":
    usuarios_page(db)

elif opcion == "Partidos":
    partidos_page(db)

elif opcion == "Jornadas":
    jornadas_page(db)

elif opcion == "Jugadores":
    jugadores_page(db)

elif opcion == "Ranking":
    ranking_page(db)

elif opcion == "Equipos Fantasy":
    equipos_fantasy_page(db)

elif opcion == "Estadísticas":
    estadisticas_page(db)
