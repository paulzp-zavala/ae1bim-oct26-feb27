
# ==============================================
# VETMANAGER - SISTEMA DE GESTION VETERINARIA
# Universidad Tecnica Particular de Loja
# Desarrollo Basado en Plataformas Web
# Periodo OCT 2026 - FEB 2027
# ==============================================

import streamlit as st
import pandas as pd
import altair as alt

from pathlib import Path
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from crear_base_entidades import (
    engine,
    Clinica,
    Consultorio,
    Veterinario,
    HistoriaClinica
)

from formularios_crud import mostrar_modulo_crud


# ==============================================
# CONFIGURACION DE LA PAGINA
# ==============================================

st.set_page_config(
    page_title="VetManager",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==============================================
# ESTILOS CSS
# ==============================================

ruta_css = Path(__file__).parent / "assets" / "styles.css"

if ruta_css.exists():

    with ruta_css.open(encoding="utf-8") as archivo:

        st.markdown(
            f"<style>{archivo.read()}</style>",
            unsafe_allow_html=True
        )


# ==============================================
# FUNCIONES AUXILIARES
# ==============================================

def mostrar_tabla(datos):

    if datos:

        st.dataframe(
            pd.DataFrame(datos),
            hide_index=True,
            width="stretch"
        )

    else:

        st.warning(
            "No existen registros que cumplan "
            "las condiciones seleccionadas."
        )


def mostrar_historias(historias):

    datos = [
        {
            "ID": h.id,
            "Fecha": h.fecha_atencion,
            "Mascota": h.nombre_mascota,
            "Diagnóstico": h.diagnostico,
            "Tratamiento": h.tratamiento,
            "Veterinario": (
                h.veterinario.nombres + " " +
                h.veterinario.apellidos
            ),
            "Clínica": (
                h.veterinario.consultorio
                .clinica.nombre_comercial
            )
        }
        for h in historias
    ]

    mostrar_tabla(datos)


# ==============================================
# MENU LATERAL
# ==============================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 15px 0;">
            <div style="
                font-size: 28px;
                font-weight: 800;
                color: #10B981;">
                🐾 VetManager
            </div>
            <div style="
                font-size: 12px;
                color: #94A3B8;">
                SISTEMA DE GESTIÓN VETERINARIA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    opcion = st.radio(
        "MENÚ PRINCIPAL",
        [
            "Inicio",
            "Clínicas",
            "Consultorios",
            "Veterinarios",
            "Historias clínicas",
            "Consultas"
        ]
    )

    st.divider()

    st.caption("PROYECTO ACADÉMICO")

    st.markdown(
        "**Universidad Técnica Particular de Loja**"
    )

    st.caption(
        "Desarrollo Basado en Plataformas Web"
    )

    st.caption("Período OCT 2026 - FEB 2027")

    st.caption(
        "Python · SQLAlchemy · SQLite · Streamlit"
    )

    st.divider()

    st.caption("VetManager | Versión 2.0")

    st.caption("Gestión CRUD integrada")


# ==============================================
# MODULO INICIO - DASHBOARD
# ==============================================

def mostrar_inicio():

    st.caption("VETMANAGER / PANEL GENERAL")

    st.title("🐾 Panel general")

    st.markdown(
        "Resumen de la red de clínicas veterinarias."
    )

    with Session(engine) as session:

        # Consultas ORM

        total_clinicas = session.query(
            Clinica
        ).count()

        total_consultorios = session.query(
            Consultorio
        ).count()

        total_veterinarios = session.query(
            Veterinario
        ).count()

        total_historias = session.query(
            HistoriaClinica
        ).count()

        st.caption(
            "🟢 Conexión con SQLite establecida"
        )

        st.divider()

        # Indicadores

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🏥 Clínicas",
            total_clinicas
        )

        col2.metric(
            "🚪 Consultorios",
            total_consultorios
        )

        col3.metric(
            "🩺 Veterinarios",
            total_veterinarios
        )

        col4.metric(
            "📋 Historias clínicas",
            total_historias
        )

        st.divider()

        # Historias clinicas por establecimiento

        clinicas = session.query(Clinica).all()

        datos_clinicas = []

        for clinica in clinicas:

            cantidad = sum(
                len(veterinario.historias_clinicas)
                for consultorio in clinica.consultorios
                for veterinario in consultorio.veterinarios
            )

            datos_clinicas.append({
                "Clínica": clinica.nombre_comercial,
                "Historias clínicas": cantidad
            })

        df_clinicas = pd.DataFrame(
            datos_clinicas,
            columns=[
                "Clínica",
                "Historias clínicas"
            ]
        )

        # Graficos

        col_grafico1, col_grafico2 = st.columns([3, 2])

        with col_grafico1:

            st.subheader(
                "Historias por establecimiento"
            )

            st.caption(
                "Cantidad de atenciones registradas por clínica"
            )

            if not df_clinicas.empty:

                grafico_barras = alt.Chart(
                    df_clinicas
                ).mark_bar(
                    cornerRadiusEnd=6,
                    size=28,
                    color="#10B981"
                ).encode(

                    x=alt.X(
                        "Historias clínicas:Q",
                        title="Historias clínicas",
                        scale=alt.Scale(
                            zero=True,
                            nice=True
                        ),
                        axis=alt.Axis(
                            tickMinStep=1
                        )
                    ),

                    y=alt.Y(
                        "Clínica:N",
                        sort="-x",
                        title=None
                    ),

                    tooltip=[
                        "Clínica:N",
                        "Historias clínicas:Q"
                    ]

                ).properties(
                    height=280
                )

                st.altair_chart(
                    grafico_barras,
                    width="stretch"
                )

            else:

                st.info(
                    "No existen clínicas registradas."
                )

        with col_grafico2:

            st.subheader("Distribución clínica")

            st.caption(
                "Participación por establecimiento"
            )

            if total_historias > 0:

                grafico_circular = alt.Chart(
                    df_clinicas
                ).mark_arc(
                    innerRadius=65,
                    outerRadius=105
                ).encode(

                    theta=alt.Theta(
                        "Historias clínicas:Q"
                    ),

                    color=alt.Color(
                        "Clínica:N",
                        scale=alt.Scale(
                            scheme="tableau10"
                        ),
                        legend=alt.Legend(
                            orient="bottom",
                            title=None
                        )
                    ),

                    tooltip=[
                        "Clínica:N",
                        "Historias clínicas:Q"
                    ]

                ).properties(
                    height=280
                )

                st.altair_chart(
                    grafico_circular,
                    width="stretch"
                )

            else:

                st.info(
                    "Todavía no existen historias clínicas."
                )

        st.divider()

        st.subheader("Resumen por clínica")

        mostrar_tabla(datos_clinicas)


# ==============================================
# MODULO CONSULTAS AVANZADAS
# ==============================================

def mostrar_consultas():

    st.caption("VETMANAGER / SQLALCHEMY ORM")

    st.title("🔎 Consultas avanzadas")

    st.caption(
        "Explorador de objetos SQLAlchemy"
    )

    metodo = st.selectbox(
        "Selecciona una operación ORM",
        [
            "all()",
            "filter()",
            "order_by()",
            "or_()",
            "and_()"
        ]
    )

    with Session(engine) as session:

        consulta = session.query(HistoriaClinica)

        diagnosticos = [
            fila[0]
            for fila in session.query(
                HistoriaClinica.diagnostico
            ).distinct().order_by(
                HistoriaClinica.diagnostico
            ).all()
        ]

        nombres_clinicas = [
            c.nombre_comercial
            for c in session.query(
                Clinica
            ).order_by(
                Clinica.nombre_comercial
            ).all()
        ]

        historias = []


        # ======================================
        # ALL
        # ======================================

        if metodo == "all()":

            st.info(
                "Recupera todos los objetos de la entidad."
            )

            historias = consulta.all()

            st.code(
                "session.query(HistoriaClinica).all()",
                language="python"
            )


        # ======================================
        # FILTER
        # ======================================

        elif metodo == "filter()":

            st.info(
                "Recupera objetos que cumplen una condición."
            )

            if not diagnosticos:

                st.warning(
                    "No existen diagnósticos registrados."
                )

                return

            diagnostico = st.selectbox(
                "Selecciona un diagnóstico",
                diagnosticos
            )

            historias = consulta.filter(
                HistoriaClinica.diagnostico == diagnostico
            ).all()

            st.code(
                f"session.query(HistoriaClinica).filter(\n"
                f"    HistoriaClinica.diagnostico "
                f"== {diagnostico!r}\n"
                f").all()",
                language="python"
            )


        # ======================================
        # ORDER BY
        # ======================================

        elif metodo == "order_by()":

            st.info(
                "Ordena los objetos según un atributo."
            )

            orden = st.radio(
                "Orden por fecha",
                [
                    "Ascendente",
                    "Descendente"
                ],
                horizontal=True
            )

            if orden == "Ascendente":

                historias = consulta.order_by(
                    HistoriaClinica.fecha_atencion.asc()
                ).all()

                direccion = "asc"

            else:

                historias = consulta.order_by(
                    HistoriaClinica.fecha_atencion.desc()
                ).all()

                direccion = "desc"

            st.code(
                f"session.query(HistoriaClinica).order_by(\n"
                f"    HistoriaClinica.fecha_atencion."
                f"{direccion}()\n"
                f").all()",
                language="python"
            )


        # ======================================
        # OR Y AND
        # ======================================

        elif metodo in ["or_()", "and_()"]:

            if metodo == "or_()":

                st.info(
                    "Debe cumplirse al menos una condición."
                )

            else:

                st.info(
                    "Deben cumplirse ambas condiciones."
                )

            if not diagnosticos or not nombres_clinicas:

                st.warning(
                    "No existen datos suficientes."
                )

                return

            col1, col2 = st.columns(2)

            diagnostico = col1.selectbox(
                "Diagnóstico",
                diagnosticos
            )

            nombre_clinica = col2.selectbox(
                "Clínica",
                nombres_clinicas
            )

            consulta = (
                consulta
                .join(Veterinario)
                .join(Consultorio)
                .join(Clinica)
            )

            condicion1 = (
                HistoriaClinica.diagnostico == diagnostico
            )

            condicion2 = (
                Clinica.nombre_comercial == nombre_clinica
            )

            if metodo == "or_()":

                historias = consulta.filter(
                    or_(condicion1, condicion2)
                ).all()

                operador = "or_"

            else:

                historias = consulta.filter(
                    and_(condicion1, condicion2)
                ).all()

                operador = "and_"

            st.code(
                f"(\n"
                f"    session.query(HistoriaClinica)\n"
                f"    .join(Veterinario)\n"
                f"    .join(Consultorio)\n"
                f"    .join(Clinica)\n"
                f"    .filter(\n"
                f"        {operador}(\n"
                f"            HistoriaClinica.diagnostico "
                f"== {diagnostico!r},\n"
                f"            Clinica.nombre_comercial "
                f"== {nombre_clinica!r}\n"
                f"        )\n"
                f"    ).all()\n"
                f")",
                language="python"
            )


        # ======================================
        # RESULTADOS
        # ======================================

        st.divider()

        st.metric(
            "Registros encontrados",
            len(historias)
        )

        mostrar_historias(historias)


# ==============================================
# NAVEGACION PRINCIPAL
# ==============================================

if opcion == "Inicio":

    mostrar_inicio()

elif opcion == "Clínicas":

    mostrar_modulo_crud("clinicas")

elif opcion == "Consultorios":

    mostrar_modulo_crud("consultorios")

elif opcion == "Veterinarios":

    mostrar_modulo_crud("veterinarios")

elif opcion == "Historias clínicas":

    mostrar_modulo_crud("historias_clinicas")

elif opcion == "Consultas":

    mostrar_consultas()


# ==============================================
# PIE DE PAGINA
# ==============================================

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        padding: 15px;
    ">
        VetManager © 2026 |
        Versión 2.0 |
        Proyecto académico UTPL |
        Desarrollo Basado en Plataformas Web
    </div>
    """,
    unsafe_allow_html=True
)
