
from sqlalchemy.orm import Session
from crear_base_entidades import (
    engine, Clinica, Consultorio,
    Veterinario, HistoriaClinica
)

with Session(engine) as session:

    print("\n--- CLINICAS ---")
    clinicas = session.query(Clinica).all()

    for c in clinicas:
        print(c.id, c.nombre_comercial,
              c.direccion, c.veterinario_responsable)

        total_historias = session.query(HistoriaClinica)\
            .join(Veterinario)\
            .join(Consultorio)\
            .filter(Consultorio.clinica_id == c.id)\
            .count()

        print("Numero de historias clinicas:", total_historias)
        print("---------")

    print("\n--- CONSULTORIOS ---")
    consultorios = session.query(Consultorio).all()

    for c in consultorios:
        print(c.id, c.nombre, c.especialidad,
              c.clinica.nombre_comercial)

    print("\n--- VETERINARIOS ---")
    veterinarios = session.query(Veterinario).all()

    for v in veterinarios:
        print(v.id, v.nombres, v.apellidos,
              v.correo, v.licencia_profesional)

    print("\n--- HISTORIAS CLINICAS ---")
    historias = session.query(HistoriaClinica).all()

    for h in historias:
        print(h.id, h.nombre_mascota,
              h.fecha_atencion, h.diagnostico,
              h.tratamiento)
