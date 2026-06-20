import streamlit as st
import pandas as pd


def usuarios_page(db):
    st.header("👥 Usuarios")
    st.markdown("Crea y administra los managers que participan en la Fantasy League.")

    with st.form("usuario_form", clear_on_submit=True):
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo electrónico")
        pais = st.text_input("País")
        submitted = st.form_submit_button("Registrar usuario")

        if submitted:
            if nombre and correo and pais:
                resultado = db.usuarios.insert_one({
                    "nombre": nombre,
                    "correo": correo,
                    "pais": pais,
                })
                st.success("Usuario registrado con éxito.")
                st.write("ID generado:", resultado.inserted_id)
            else:
                st.error("Por favor completa todos los campos para registrar el usuario.")

    st.divider()
    st.subheader("Lista de usuarios")

    usuarios = list(db.usuarios.find())
    df = pd.DataFrame(usuarios)

    if df.empty:
        st.info("Aún no hay usuarios registrados. Agrega un manager para empezar la liga.")
        return

    if "_id" in df.columns:
        df["_id"] = df["_id"].astype(str)
        df = df.drop(columns=["_id"])

    df = df.rename(columns={"nombre": "Nombre", "correo": "Correo", "pais": "País"})
    st.dataframe(df)

    st.divider()
    st.subheader("Editar información de usuario")

    usuarios_nombres = [usuario.get("nombre") for usuario in usuarios if usuario.get("nombre")]
    usuario_seleccionado = st.selectbox("Selecciona un usuario", [""] + usuarios_nombres, key="usuario_seleccionado")

    if usuario_seleccionado:
        usuario_doc = next((u for u in usuarios if u.get("nombre") == usuario_seleccionado), None)

        if usuario_doc:
            with st.form("editar_usuario_form"):
                nombre_edit = st.text_input("Nombre completo", value=usuario_doc.get("nombre", ""))
                correo_edit = st.text_input("Correo electrónico", value=usuario_doc.get("correo", ""))
                pais_edit = st.text_input("País", value=usuario_doc.get("pais", ""))
                guardar = st.form_submit_button("Guardar cambios")

                if guardar:
                    if nombre_edit and correo_edit and pais_edit:
                        db.usuarios.update_one(
                            {"_id": usuario_doc["_id"]},
                            {"$set": {"nombre": nombre_edit, "correo": correo_edit, "pais": pais_edit}},
                        )
                        st.success("Información del usuario actualizada correctamente.")
                    else:
                        st.error("Completa todos los campos para actualizar el usuario.")

    st.divider()
    st.subheader("Eliminar usuario")
    usuario_borrar = st.selectbox("Selecciona un usuario para eliminar", [""] + usuarios_nombres, key="usuario_borrar")
    if st.button("Eliminar usuario"):
        if not usuario_borrar:
            st.error("Selecciona un usuario antes de eliminar.")
        else:
            usuario_doc = next((u for u in usuarios if u.get("nombre") == usuario_borrar), None)
            if usuario_doc:
                db.usuarios.delete_one({"_id": usuario_doc["_id"]})
                st.success(f"Usuario {usuario_borrar} eliminado correctamente.")
            else:
                st.error("No se encontró el usuario seleccionado.")
