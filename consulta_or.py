from sqlalchemy import or_
from sqlalchemy.orm import Session
from crear_base_entidades import engine, Consultorio, HistoriaClinica

with Session(engine) as session:

    print("\n--- CONSULTORIOS DE MEDICINA GENERAL O CIRUGIA ---")

    consultorios = session.query(Consultorio).filter(
        or_(
            Consultorio.especialidad == "Medicina general",
            Consultorio.especialidad == "Cirugia"
        )
    ).all()

    for c in consultorios:
        print(c.id, c.nombre, c.especialidad,
              c.clinica.nombre_comercial)

    print("\n--- HISTORIAS CLINICAS CON DERMATITIS U OTITIS ---")

    historias = session.query(HistoriaClinica).filter(
        or_(
            HistoriaClinica.diagnostico == "Dermatitis",
            HistoriaClinica.diagnostico == "Otitis"
        )
    ).all()

    for h in historias:
        print(h.id, h.nombre_mascota,
              h.diagnostico, h.tratamiento)