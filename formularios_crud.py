
# ==============================================
# VETMANAGER - FORMULARIOS CRUD
# Interfaz web con Streamlit
# ==============================================

import streamlit as st
import pandas as pd

from datetime import date

from operaciones_crud import (
    crud_clinicas,
    crud_consultorios,
    crud_veterinarios,
    crud_historias
)


# ==============================================
# CONFIGURACION DE LOS MODULOS
# ==============================================

MODULOS = {
    "clinicas": {
        "titulo": "Clínicas veterinarias",
        "icono": "🏥",
        "gestor": crud_clinicas
    },

    "consultorios": {
        "titulo": "Consultorios",
        "icono": "🚪",
        "gestor": crud_consultorios
    },

    "veterinarios": {
        "titulo": "Veterinarios",
        "icono": "🩺",
        "gestor": crud_veterinarios
    },

    "historias_clinicas": {
        "titulo": "Historias clínicas",
        "icono": "📋",
        "gestor": crud_historias
    }
}


# ==============================================
# IDENTIFICAR REGISTROS
# ==============================================

def etiqueta_registro(entidad, registro):

    identificador = registro["id"]

    if entidad == "clinicas":

        nombre = registro["nombre_comercial"]

    elif entidad == "consultorios":

        nombre = registro["nombre"]

    elif entidad == "veterinarios":

        nombre = (
            registro["nombres"] + " " +
            registro["apellidos"]
        )

    else:

        nombre = (
            registro["nombre_mascota"] + " - " +
            registro["diagnostico"]
        )

    return f"{identificador} | {nombre}"


# ==============================================
# SELECTOR DE REGISTROS
# ==============================================

def seleccionar_registro(entidad, clave):

    registros = MODULOS[entidad]["gestor"].listar()

    if not registros:

        st.warning("No existen registros disponibles.")

        return None

    return st.selectbox(
        "Selecciona un registro",
        options=registros,
        format_func=lambda r: etiqueta_registro(
            entidad, r
        ),
        key=clave
    )


# ==============================================
# SELECTOR DE RELACIONES
# ==============================================

def seleccionar_relacion(
    entidad,
    etiqueta,
    clave,
    valor_actual=None
):

    registros = MODULOS[entidad]["gestor"].listar()

    if not registros:

        st.warning(
            f"No existen registros para: {etiqueta}"
        )

        return None

    indice = 0

    for i, registro in enumerate(registros):

        if registro["id"] == valor_actual:

            indice = i
            break

    seleccionado = st.selectbox(
        etiqueta,
        options=registros,
        index=indice,
        format_func=lambda r: etiqueta_registro(
            entidad, r
        ),
        key=clave
    )

    return seleccionado["id"]


# ==============================================
# CAMPOS DE LOS FORMULARIOS
# ==============================================

def campos_formulario(entidad, clave, registro=None):

    registro = registro or {}

    datos = {}

    # ------------------------------------------
    # CLINICAS
    # ------------------------------------------

    if entidad == "clinicas":

        datos["nombre_comercial"] = st.text_input(
            "Nombre comercial",
            value=registro.get("nombre_comercial", ""),
            max_chars=100,
            key=f"{clave}_nombre"
        )

        datos["direccion"] = st.text_input(
            "Dirección",
            value=registro.get("direccion", ""),
            max_chars=150,
            key=f"{clave}_direccion"
        )

        datos["veterinario_responsable"] = st.text_input(
            "Veterinario responsable",
            value=registro.get(
                "veterinario_responsable", ""
            ),
            max_chars=100,
            key=f"{clave}_responsable"
        )

    # ------------------------------------------
    # CONSULTORIOS
    # ------------------------------------------

    elif entidad == "consultorios":

        datos["nombre"] = st.text_input(
            "Nombre o número del consultorio",
            value=registro.get("nombre", ""),
            max_chars=100,
            key=f"{clave}_nombre"
        )

        datos["especialidad"] = st.text_input(
            "Especialidad",
            value=registro.get("especialidad", ""),
            max_chars=100,
            key=f"{clave}_especialidad"
        )

        datos["clinica_id"] = seleccionar_relacion(
            "clinicas",
            "Clínica asociada",
            f"{clave}_clinica",
            registro.get("clinica_id")
        )

    # ------------------------------------------
    # VETERINARIOS
    # ------------------------------------------

    elif entidad == "veterinarios":

        col1, col2 = st.columns(2)

        datos["nombres"] = col1.text_input(
            "Nombres",
            value=registro.get("nombres", ""),
            max_chars=100,
            key=f"{clave}_nombres"
        )

        datos["apellidos"] = col2.text_input(
            "Apellidos",
            value=registro.get("apellidos", ""),
            max_chars=100,
            key=f"{clave}_apellidos"
        )

        datos["correo"] = st.text_input(
            "Correo electrónico",
            value=registro.get("correo", ""),
            max_chars=100,
            key=f"{clave}_correo"
        )

        datos["licencia_profesional"] = st.text_input(
            "Licencia profesional",
            value=registro.get(
                "licencia_profesional", ""
            ),
            max_chars=50,
            key=f"{clave}_licencia"
        )

        datos["consultorio_id"] = seleccionar_relacion(
            "consultorios",
            "Consultorio asignado",
            f"{clave}_consultorio",
            registro.get("consultorio_id")
        )

    # ------------------------------------------
    # HISTORIAS CLINICAS
    # ------------------------------------------

    elif entidad == "historias_clinicas":

        datos["nombre_mascota"] = st.text_input(
            "Nombre de la mascota",
            value=registro.get("nombre_mascota", ""),
            max_chars=100,
            key=f"{clave}_mascota"
        )

        datos["fecha_atencion"] = st.date_input(
            "Fecha de atención",
            value=registro.get(
                "fecha_atencion", date.today()
            ),
            format="DD/MM/YYYY",
            key=f"{clave}_fecha"
        )

        datos["diagnostico"] = st.text_area(
            "Diagnóstico",
            value=registro.get("diagnostico", ""),
            max_chars=250,
            key=f"{clave}_diagnostico"
        )

        datos["tratamiento"] = st.text_area(
            "Tratamiento",
            value=registro.get("tratamiento", ""),
            max_chars=250,
            key=f"{clave}_tratamiento"
        )

        datos["veterinario_id"] = seleccionar_relacion(
            "veterinarios",
            "Veterinario responsable",
            f"{clave}_veterinario",
            registro.get("veterinario_id")
        )

    return datos


# ==============================================
# MOSTRAR TABLA CON RELACIONES
# ==============================================

def mostrar_registros(entidad, registros):

    if not registros:

        st.info("No existen registros.")

        return

    datos = []

    clinicas = {
        r["id"]: r
        for r in crud_clinicas.listar()
    }

    consultorios = {
        r["id"]: r
        for r in crud_consultorios.listar()
    }

    veterinarios = {
        r["id"]: r
        for r in crud_veterinarios.listar()
    }

    for registro in registros:

        fila = dict(registro)

        if entidad == "consultorios":

            clinica = clinicas.get(
                fila.pop("clinica_id"), {}
            )

            fila["Clínica"] = clinica.get(
                "nombre_comercial", "Sin asignar"
            )

        elif entidad == "veterinarios":

            consultorio = consultorios.get(
                fila.pop("consultorio_id"), {}
            )

            clinica = clinicas.get(
                consultorio.get("clinica_id"), {}
            )

            fila["Consultorio"] = consultorio.get(
                "nombre", "Sin asignar"
            )

            fila["Clínica"] = clinica.get(
                "nombre_comercial", "Sin asignar"
            )

        elif entidad == "historias_clinicas":

            veterinario = veterinarios.get(
                fila.pop("veterinario_id"), {}
            )

            consultorio = consultorios.get(
                veterinario.get("consultorio_id"), {}
            )

            clinica = clinicas.get(
                consultorio.get("clinica_id"), {}
            )

            fila["Veterinario"] = (
                veterinario.get("nombres", "") + " " +
                veterinario.get("apellidos", "")
            ).strip()

            fila["Clínica"] = clinica.get(
                "nombre_comercial", "Sin asignar"
            )

        datos.append(fila)

    df = pd.DataFrame(datos)

    df = df.rename(columns={
        "id": "ID",
        "nombre_comercial": "Nombre comercial",
        "direccion": "Dirección",
        "veterinario_responsable": "Responsable",
        "nombre": "Nombre",
        "especialidad": "Especialidad",
        "nombres": "Nombres",
        "apellidos": "Apellidos",
        "correo": "Correo",
        "licencia_profesional": "Licencia",
        "nombre_mascota": "Mascota",
        "fecha_atencion": "Fecha",
        "diagnostico": "Diagnóstico",
        "tratamiento": "Tratamiento"
    })

    st.dataframe(
        df,
        hide_index=True,
        width="stretch"
    )


# ==============================================
# RESULTADO DE LAS OPERACIONES
# ==============================================

def mostrar_resultado(resultado):

    correcto, mensaje = resultado

    if correcto:

        st.session_state["mensaje_crud"] = mensaje

        st.rerun()

    else:

        st.error(mensaje)


# ==============================================
# MODULO CRUD COMPLETO
# ==============================================

def mostrar_modulo_crud(entidad):

    configuracion = MODULOS[entidad]

    gestor = configuracion["gestor"]

    st.caption("VETMANAGER / ADMINISTRACIÓN")

    st.title(
        f"{configuracion['icono']} "
        f"{configuracion['titulo']}"
    )

    st.caption(
        "Registro, consulta, edición y eliminación "
        "mediante SQLAlchemy ORM."
    )

    if "mensaje_crud" in st.session_state:

        st.success(
            st.session_state.pop("mensaje_crud")
        )

    registros = gestor.listar()

    st.metric(
        "Total de registros",
        len(registros)
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Consultar",
        "➕ Registrar",
        "✏️ Editar",
        "🗑️ Eliminar"
    ])


    # ==========================================
    # READ - CONSULTAR
    # ==========================================

    with tab1:

        st.subheader("Registros existentes")

        busqueda = st.text_input(
            "Buscar registros",
            placeholder="Escribe para buscar...",
            key=f"{entidad}_busqueda"
        )

        resultados = registros

        if busqueda:

            resultados = [
                r for r in registros
                if busqueda.lower() in
                " ".join(
                    str(v) for v in r.values()
                ).lower()
            ]

        st.caption(
            f"Registros encontrados: {len(resultados)}"
        )

        mostrar_registros(entidad, resultados)


    # ==========================================
    # CREATE - REGISTRAR
    # ==========================================

    with tab2:

        st.subheader("Registrar nuevo elemento")

        st.caption(
            "Completa todos los campos obligatorios."
        )

        with st.form(
            f"{entidad}_crear",
            clear_on_submit=False
        ):

            datos = campos_formulario(
                entidad,
                f"{entidad}_nuevo"
            )

            guardar = st.form_submit_button(
                "Guardar registro",
                type="primary"
            )

            if guardar:

                mostrar_resultado(
                    gestor.crear(**datos)
                )


    # ==========================================
    # UPDATE - EDITAR
    # ==========================================

    with tab3:

        st.subheader("Editar registro existente")

        registro = seleccionar_registro(
            entidad,
            f"{entidad}_seleccionar_editar"
        )

        if registro is not None:

            identificador = registro["id"]

            with st.form(
                f"{entidad}_editar_{identificador}"
            ):

                datos = campos_formulario(
                    entidad,
                    f"{entidad}_edit_{identificador}",
                    registro
                )

                actualizar = st.form_submit_button(
                    "Guardar cambios",
                    type="primary"
                )

                if actualizar:

                    mostrar_resultado(
                        gestor.actualizar(
                            identificador,
                            **datos
                        )
                    )


    # ==========================================
    # DELETE - ELIMINAR
    # ==========================================

    with tab4:

        st.subheader("Eliminar registro")

        st.warning(
            "Esta operación es permanente. "
            "Verifica el registro antes de eliminarlo."
        )

        registro = seleccionar_registro(
            entidad,
            f"{entidad}_seleccionar_eliminar"
        )

        if registro is not None:

            identificador = registro["id"]

            mostrar_registros(
                entidad,
                [registro]
            )

            confirmar = st.checkbox(
                "Confirmo que deseo eliminar este registro.",
                key=f"{entidad}_confirmar_{identificador}"
            )

            eliminar = st.button(
                "Eliminar definitivamente",
                disabled=not confirmar,
                key=f"{entidad}_eliminar_{identificador}"
            )

            if eliminar:

                mostrar_resultado(
                    gestor.eliminar(identificador)
                )
