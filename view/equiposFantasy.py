import streamlit as st
import pandas as pd


def equipos_fantasy_page(db):
    st.header("🏟️ Equipos Fantasy")
    st.markdown("Construye tu escuadra, asigna capitanes y revisa la plantilla de cada equipo.")

    usuarios = list(db.usuarios.find())
    jugadores = list(db.jugadores.find())
    equipos = list(db.equiposFantasy.find())

    usuarios_nombres = [usuario.get("nombre") for usuario in usuarios if usuario.get("nombre")]
    jugadores_nombres = [jugador.get("nombre") for jugador in jugadores if jugador.get("nombre")]
    equipos_nombres = [equipo.get("nombreEquipo") for equipo in equipos if equipo.get("nombreEquipo")]

    with st.form("crear_equipo_form", clear_on_submit=True):
        st.subheader("Crear equipo fantasy")
        nombre_equipo = st.text_input("Nombre del equipo")
        usuario_equipo = st.selectbox("Manager", [""] + usuarios_nombres)
        capitan = st.selectbox("Capitán", [""] + jugadores_nombres)
        jugadores_seleccionados = st.multiselect("Jugadores", jugadores_nombres)
        crear_equipo = st.form_submit_button("Crear equipo")

        if crear_equipo:
            if not nombre_equipo or not usuario_equipo or not capitan or not jugadores_seleccionados:
                st.error("Completa todos los campos para crear el equipo.")
            elif len(jugadores_seleccionados) < 3:
                st.error("El equipo debe tener al menos 3 jugadores.")
            elif len(jugadores_seleccionados) > 5:
                st.error("El equipo no puede tener más de 5 jugadores.")
            else:
                jugadores_objetos = []
                for nombre in jugadores_seleccionados:
                    jugador_doc = next((j for j in jugadores if j.get("nombre") == nombre), None)
                    if jugador_doc:
                        jugadores_objetos.append({
                            "nombre": jugador_doc.get("nombre"),
                            "posicion": jugador_doc.get("posicion"),
                        })

                db.equiposFantasy.insert_one({
                    "nombreEquipo": nombre_equipo,
                    "usuario": usuario_equipo,
                    "capitan": capitan,
                    "jugadores": jugadores_objetos,
                })
                st.success("Equipo creado correctamente.")

    st.divider()
    st.subheader("Agregar jugador a un equipo")

    equipo_para_agregar = st.selectbox("Equipo", [""] + equipos_nombres, key="equipo_agregar")
    jugador_para_agregar = st.selectbox("Jugador", [""] + jugadores_nombres, key="jugador_agregar")
    if st.button("Agregar jugador al equipo"):
        if not equipo_para_agregar or not jugador_para_agregar:
            st.error("Selecciona un equipo y un jugador.")
        else:
            equipo_doc = next((e for e in equipos if e.get("nombreEquipo") == equipo_para_agregar), None)
            jugador_doc = next((j for j in jugadores if j.get("nombre") == jugador_para_agregar), None)
            if not equipo_doc or not jugador_doc:
                st.error("Equipo o jugador no válidos.")
            else:
                miembros = [j.get("nombre") for j in equipo_doc.get("jugadores", [])]
                if jugador_para_agregar in miembros:
                    st.error("El jugador ya pertenece a este equipo.")
                elif len(miembros) >= 5:
                    st.error("El equipo ya tiene el máximo de 5 jugadores.")
                else:
                    db.equiposFantasy.update_one(
                        {"nombreEquipo": equipo_para_agregar},
                        {
                            "$push": {
                                "jugadores": {
                                    "nombre": jugador_doc.get("nombre"),
                                    "posicion": jugador_doc.get("posicion"),
                                }
                            }
                        },
                    )
                    st.success(f"{jugador_para_agregar} fue agregado a {equipo_para_agregar}.")

    st.divider()
    st.subheader("Actualizar alineación de un equipo")

    equipo_para_alinear = st.selectbox("Equipo a ajustar", [""] + equipos_nombres, key="equipo_alinear")
    alineacion_actual = []
    if equipo_para_alinear:
        equipo_doc = next((e for e in equipos if e.get("nombreEquipo") == equipo_para_alinear), None)
        alineacion_actual = [j.get("nombre") for j in equipo_doc.get("jugadores", [])] if equipo_doc else []

    jugadores_nuevos = st.multiselect(
        "Jugadores en alineación",
        jugadores_nombres,
        default=alineacion_actual,
        key="alineacion_nueva",
    )
    if st.button("Guardar alineación"):
        if not equipo_para_alinear:
            st.error("Selecciona un equipo para actualizar la alineación.")
        elif len(jugadores_nuevos) < 3:
            st.error("La alineación debe tener al menos 3 jugadores.")
        elif len(jugadores_nuevos) > 5:
            st.error("La alineación no puede superar los 5 jugadores.")
        else:
            jugadores_objetos = []
            for nombre in jugadores_nuevos:
                jugador_doc = next((j for j in jugadores if j.get("nombre") == nombre), None)
                if jugador_doc:
                    jugadores_objetos.append({
                        "nombre": jugador_doc.get("nombre"),
                        "posicion": jugador_doc.get("posicion"),
                    })
            db.equiposFantasy.update_one(
                {"nombreEquipo": equipo_para_alinear},
                {"$set": {"jugadores": jugadores_objetos}},
            )
            st.success("Alineación actualizada correctamente.")

    st.divider()
    st.subheader("Cambiar capitán del equipo")
    equipo_capitan = st.selectbox("Selecciona un equipo", [""] + equipos_nombres, key="equipo_capitan")
    jugadores_equipo_capitan = []
    if equipo_capitan:
        equipo_doc = next((e for e in equipos if e.get("nombreEquipo") == equipo_capitan), None)
        jugadores_equipo_capitan = [j.get("nombre") for j in equipo_doc.get("jugadores", [])] if equipo_doc else []

    nuevo_capitan = st.selectbox("Nuevo capitán", [""] + jugadores_equipo_capitan, key="nuevo_capitan")
    if st.button("Cambiar capitán"):
        if not equipo_capitan or not nuevo_capitan:
            st.error("Selecciona un equipo y un nuevo capitán.")
        else:
            db.equiposFantasy.update_one(
                {"nombreEquipo": equipo_capitan},
                {"$set": {"capitan": nuevo_capitan}},
            )
            st.success(f"Capitán de {equipo_capitan} cambiado a {nuevo_capitan}.")

    st.divider()
    st.subheader("Equipos registrados")

    equipos_registrados = list(db.equiposFantasy.find())
    df_equipos = pd.DataFrame(equipos_registrados)

    if df_equipos.empty:
        st.info("No hay equipos registrados en la liga.")
        return

    if "_id" in df_equipos.columns:
        df_equipos = df_equipos.drop(columns=["_id"])

    df_equipos["Jugadores totales"] = df_equipos["jugadores"].apply(
        lambda lista: len(lista) if isinstance(lista, list) else 0
    )
    df_equipos = df_equipos.rename(
        columns={
            "nombreEquipo": "Equipo",
            "usuario": "Manager",
            "capitan": "Capitán",
        }
    )
    st.dataframe(df_equipos[["Equipo", "Manager", "Capitán", "Jugadores totales"]])
