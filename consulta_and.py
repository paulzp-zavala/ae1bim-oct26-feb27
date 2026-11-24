from datetime import date
from sqlalchemy import and_
from sqlalchemy.orm import Session
from crear_base_entidades import engine, Consultorio, Clinica, HistoriaClinica

with Session(engine) as session:

    print("\n--- CONSULTORIOS DE MEDICINA GENERAL EN VETCARE ---")

    consultorios = session.query(Consultorio).join(Clinica).filter(
        and_(
            Consultorio.especialidad == "Medicina general",
            Clinica.nombre_comercial == "VetCare"
        )
    ).all()

    for c in consultorios:
        print(c.id, c.nombre, c.especialidad,
              c.clinica.nombre_comercial)

    print("\n--- HISTORIAS CLINICAS CON DERMATITIS DESDE EL 15 DE NOVIEMBRE ---")

    historias = session.query(HistoriaClinica).filter(
        and_(
            HistoriaClinica.diagnostico == "Dermatitis",
            HistoriaClinica.fecha_atencion >= date(2026, 11, 15)
        )
    ).all()

    for h in historias:
        print(h.id, h.nombre_mascota,
              h.fecha_atencion, h.diagnostico)