from sqlalchemy.orm import Session
from crear_base_entidades import engine, Consultorio, HistoriaClinica

with Session(engine) as session:

    print("\n--- CONSULTORIOS DE MEDICINA GENERAL ---")

    consultorios = session.query(Consultorio).filter(
        Consultorio.especialidad == "Medicina general"
    ).all()

    for c in consultorios:
        print(c.id, c.nombre, c.especialidad,
              c.clinica.nombre_comercial)

    print("\n--- HISTORIAS CLINICAS CON DERMATITIS ---")

    historias = session.query(HistoriaClinica).filter(
        HistoriaClinica.diagnostico == "Dermatitis"
    ).all()

    for h in historias:
        print(h.id, h.nombre_mascota,
              h.diagnostico, h.tratamiento)