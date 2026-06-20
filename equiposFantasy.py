import streamlit as st
import pandas as pd


def equipos_fantasy_page(db):
    st.header("🏟️ Equipos Fantasy")

    usuarios = list(db.usuarios.find())
    jugadores = list(db.jugadores.find())
    equipos = list(db.equiposFantasy.find())

    usuarios_nombres = [usuario.get("nombre") for usuario in usuarios if usuario.get("nombre")]
    jugadores_nombres = [jugador.get("nombre") for jugador in jugadores if jugador.get("nombre")]
    equipos_nombres = [equipo.get("nombreEquipo") for equipo in equipos if equipo.get("nombreEquipo")]

    st.subheader("CREAR EQUIPO")

    nombre_equipo = st.text_input("Nombre del equipo")
    usuario_equipo = st.selectbox("Usuario", [""] + usuarios_nombres)
    capitan = st.selectbox("Capitán", [""] + jugadores_nombres)
    jugadores_seleccionados = st.multiselect("Jugadores", jugadores_nombres)

    if st.button("Crear Equipo"):
        if not nombre_equipo or not usuario_equipo or not capitan or not jugadores_seleccionados:
            st.error("Complete todos los campos para crear el equipo.")
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
                        "posicion": jugador_doc.get("posicion")
                    })

            db.equiposFantasy.insert_one({
                "nombreEquipo": nombre_equipo,
                "usuario": usuario_equipo,
                "capitan": capitan,
                "jugadores": jugadores_objetos
            })

            st.success("Equipo creado correctamente.")

    st.subheader("Gestión del Equipo")

    st.markdown("### Agregar jugador")
    equipo_agregar = st.selectbox("Equipo", [""] + equipos_nombres, key="equipo_agregar")
    jugador_agregar = st.selectbox("Jugador disponible", [""] + jugadores_nombres, key="jugador_agregar")

    if st.button("Agregar Jugador"):
        if not equipo_agregar or not jugador_agregar:
            st.error("Seleccione un equipo y un jugador para agregar.")
        else:
            jugador_doc = next((j for j in jugadores if j.get("nombre") == jugador_agregar), None)
            equipo_doc = next((e for e in equipos if e.get("nombreEquipo") == equipo_agregar), None)
            jugadores_actuales = [jugador.get("nombre") for jugador in equipo_doc.get("jugadores", [])] if equipo_doc else []
            capitan_actual = equipo_doc.get("capitan") if equipo_doc else None

            if jugador_agregar == capitan_actual or jugador_agregar in jugadores_actuales:
                st.error("El jugador ya forma parte del equipo como capitán o como miembro.")
            elif jugador_doc:
                db.equiposFantasy.update_one(
                    {"nombreEquipo": equipo_agregar},
                    {
                        "$push": {
                            "jugadores": {
                                "nombre": jugador_doc.get("nombre"),
                                "posicion": jugador_doc.get("posicion")
                            }
                        }
                    }
                )
                st.success(f"Jugador {jugador_agregar} agregado al equipo {equipo_agregar}.")
            else:
                st.error("El jugador seleccionado no existe.")

    st.markdown("### Eliminar jugador")
    equipo_eliminar = st.selectbox("Equipo", [""] + equipos_nombres, key="equipo_eliminar")
    jugadores_equipo = []
    if equipo_eliminar:
        equipo_doc = next((e for e in equipos if e.get("nombreEquipo") == equipo_eliminar), None)
        jugadores_equipo = [jugador.get("nombre") for jugador in equipo_doc.get("jugadores", [])] if equipo_doc else []

    jugador_eliminar = st.selectbox("Jugador del equipo", [""] + jugadores_equipo, key="jugador_eliminar")

    if st.button("Eliminar Jugador"):
        if not equipo_eliminar or not jugador_eliminar:
            st.error("Seleccione un equipo y un jugador para eliminar.")
        else:
            db.equiposFantasy.update_one(
                {"nombreEquipo": equipo_eliminar},
                {
                    "$pull": {
                        "jugadores": {
                            "nombre": jugador_eliminar
                        }
                    }
                }
            )
            st.success(f"Jugador {jugador_eliminar} eliminado del equipo {equipo_eliminar}.")

    st.markdown("### Cambiar capitán")
    equipo_capitan = st.selectbox("Equipo", [""] + equipos_nombres, key="equipo_capitan")
    jugadores_equipo_capitan = []
    if equipo_capitan:
        equipo_doc_capitan = next((e for e in equipos if e.get("nombreEquipo") == equipo_capitan), None)
        jugadores_equipo_capitan = [jugador.get("nombre") for jugador in equipo_doc_capitan.get("jugadores", [])] if equipo_doc_capitan else []

    nuevo_capitan = st.selectbox("Nuevo capitán", [""] + jugadores_equipo_capitan, key="nuevo_capitan")

    if st.button("Cambiar Capitán"):
        if not equipo_capitan or not nuevo_capitan:
            st.error("Seleccione un equipo y un capitán para cambiar.")
        else:
            db.equiposFantasy.update_one(
                {"nombreEquipo": equipo_capitan},
                {
                    "$set": {
                        "capitan": nuevo_capitan
                    }
                }
            )
            st.success(f"Capitán del equipo {equipo_capitan} cambiado a {nuevo_capitan}.")

    st.subheader("EQUIPOS REGISTRADOS")
    equipos_registrados = list(db.equiposFantasy.find())
    df_equipos = pd.DataFrame(equipos_registrados)

    if not df_equipos.empty:
        df_equipos["cantidadJugadores"] = df_equipos["jugadores"].apply(lambda lista: len(lista) if isinstance(lista, list) else 0)
        if "_id" in df_equipos.columns:
            df_equipos = df_equipos.drop("_id", axis=1)
        df_equipos = df_equipos[["nombreEquipo", "usuario", "capitan", "cantidadJugadores"]]
        st.dataframe(df_equipos)
    else:
        st.write("No hay equipos registrados todavía.")