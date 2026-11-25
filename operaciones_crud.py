
# ==============================================
# VETMANAGER - OPERACIONES CRUD
# Python + SQLAlchemy ORM + SQLite
# ==============================================

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from crear_base_entidades import (
    engine,
    Clinica,
    Consultorio,
    Veterinario,
    HistoriaClinica
)


# ==============================================
# CONFIGURACION DE ENTIDADES
# ==============================================

ENTIDADES = {
    "clinicas": Clinica,
    "consultorios": Consultorio,
    "veterinarios": Veterinario,
    "historias_clinicas": HistoriaClinica
}


CAMPOS = {
    "clinicas": [
        "nombre_comercial",
        "direccion",
        "veterinario_responsable"
    ],

    "consultorios": [
        "nombre",
        "especialidad",
        "clinica_id"
    ],

    "veterinarios": [
        "nombres",
        "apellidos",
        "correo",
        "licencia_profesional",
        "consultorio_id"
    ],

    "historias_clinicas": [
        "fecha_atencion",
        "diagnostico",
        "tratamiento",
        "nombre_mascota",
        "veterinario_id"
    ]
}


# ==============================================
# CLASE PARA LA GESTION CRUD
# ==============================================

class GestorCRUD:

    def __init__(self, entidad):

        if entidad not in ENTIDADES:
            raise ValueError("Entidad no válida.")

        self.entidad = entidad
        self.modelo = ENTIDADES[entidad]


    # ==========================================
    # VALIDACION DE DATOS
    # ==========================================

    def validar_datos(self, session, datos):

        for campo in CAMPOS[self.entidad]:

            valor = datos.get(campo)

            if valor is None:
                raise ValueError(
                    f"El campo {campo} es obligatorio."
                )

            if isinstance(valor, str):

                valor = valor.strip()

                if not valor:
                    raise ValueError(
                        f"El campo {campo} es obligatorio."
                    )

                datos[campo] = valor

                columna = self.modelo.__table__.columns[campo]
                longitud = getattr(
                    columna.type, "length", None
                )

                if longitud and len(valor) > longitud:
                    raise ValueError(
                        f"El campo {campo} supera "
                        f"los {longitud} caracteres."
                    )

        # Validar relaciones entre entidades

        if self.entidad == "consultorios":

            clinica = session.get(
                Clinica,
                datos["clinica_id"]
            )

            if clinica is None:
                raise ValueError(
                    "La clínica seleccionada no existe."
                )

        elif self.entidad == "veterinarios":

            consultorio = session.get(
                Consultorio,
                datos["consultorio_id"]
            )

            if consultorio is None:
                raise ValueError(
                    "El consultorio seleccionado no existe."
                )

            correo = datos["correo"]

            if "@" not in correo:
                raise ValueError(
                    "Ingresa un correo electrónico válido."
                )

        elif self.entidad == "historias_clinicas":

            veterinario = session.get(
                Veterinario,
                datos["veterinario_id"]
            )

            if veterinario is None:
                raise ValueError(
                    "El veterinario seleccionado no existe."
                )


    # ==========================================
    # CREATE - REGISTRAR
    # ==========================================

    def crear(self, **datos):

        with Session(engine) as session:

            try:

                self.validar_datos(session, datos)

                nuevo_objeto = self.modelo(
                    **{
                        campo: datos[campo]
                        for campo in CAMPOS[self.entidad]
                    }
                )

                session.add(nuevo_objeto)

                session.flush()

                identificador = nuevo_objeto.id

                session.commit()

                return (
                    True,
                    f"Registro creado correctamente. "
                    f"ID: {identificador}"
                )

            except (SQLAlchemyError, ValueError) as error:

                session.rollback()

                return False, str(error)


    # ==========================================
    # READ - CONSULTAR TODOS
    # ==========================================

    def listar(self):

        with Session(engine) as session:

            registros = session.query(
                self.modelo
            ).order_by(
                self.modelo.id
            ).all()

            return [
                {
                    columna.name: getattr(
                        registro,
                        columna.name
                    )
                    for columna in
                    self.modelo.__table__.columns
                }
                for registro in registros
            ]


    # ==========================================
    # READ - BUSCAR POR ID
    # ==========================================

    def buscar(self, identificador):

        with Session(engine) as session:

            registro = session.get(
                self.modelo,
                identificador
            )

            if registro is None:
                return None

            return {
                columna.name: getattr(
                    registro,
                    columna.name
                )
                for columna in
                self.modelo.__table__.columns
            }


    # ==========================================
    # UPDATE - ACTUALIZAR
    # ==========================================

    def actualizar(self, identificador, **datos):

        with Session(engine) as session:

            try:

                registro = session.get(
                    self.modelo,
                    identificador
                )

                if registro is None:
                    return False, "Registro no encontrado."

                datos_actualizados = {
                    campo: datos.get(
                        campo,
                        getattr(registro, campo)
                    )
                    for campo in CAMPOS[self.entidad]
                }

                self.validar_datos(
                    session,
                    datos_actualizados
                )

                for campo, valor in datos_actualizados.items():

                    setattr(
                        registro,
                        campo,
                        valor
                    )

                session.commit()

                return (
                    True,
                    "Registro actualizado correctamente."
                )

            except (SQLAlchemyError, ValueError) as error:

                session.rollback()

                return False, str(error)


    # ==========================================
    # DELETE - ELIMINAR
    # ==========================================

    def eliminar(self, identificador):

        with Session(engine) as session:

            try:

                registro = session.get(
                    self.modelo,
                    identificador
                )

                if registro is None:
                    return False, "Registro no encontrado."

                # Proteger las relaciones existentes

                if isinstance(registro, Clinica):

                    if registro.consultorios:

                        return (
                            False,
                            "No se puede eliminar la clínica "
                            "porque tiene consultorios asociados."
                        )

                elif isinstance(registro, Consultorio):

                    if registro.veterinarios:

                        return (
                            False,
                            "No se puede eliminar el consultorio "
                            "porque tiene veterinarios asociados."
                        )

                elif isinstance(registro, Veterinario):

                    if registro.historias_clinicas:

                        return (
                            False,
                            "No se puede eliminar el veterinario "
                            "porque tiene historias clínicas asociadas."
                        )

                session.delete(registro)

                session.commit()

                return (
                    True,
                    "Registro eliminado correctamente."
                )

            except SQLAlchemyError as error:

                session.rollback()

                return False, str(error)


# ==============================================
# OBJETOS GESTORES DE CADA ENTIDAD
# ==============================================

crud_clinicas = GestorCRUD("clinicas")

crud_consultorios = GestorCRUD("consultorios")

crud_veterinarios = GestorCRUD("veterinarios")

crud_historias = GestorCRUD("historias_clinicas")


# ==============================================
# PRUEBA DE FUNCIONAMIENTO
# ==============================================

if __name__ == "__main__":

    print("=" * 50)
    print("VETMANAGER - MOTOR CRUD")
    print("=" * 50)

    print("\nClínicas:", len(crud_clinicas.listar()))

    print(
        "Consultorios:",
        len(crud_consultorios.listar())
    )

    print(
        "Veterinarios:",
        len(crud_veterinarios.listar())
    )

    print(
        "Historias clínicas:",
        len(crud_historias.listar())
    )

    print("\nMotor CRUD conectado correctamente.")
