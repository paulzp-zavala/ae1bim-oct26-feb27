from sqlalchemy.orm import Session
from crear_base_entidades import engine, Veterinario, HistoriaClinica

with Session(engine) as session:

    print("\n--- VETERINARIOS ORDENADOS POR APELLIDO ---")

    veterinarios = session.query(Veterinario).order_by(
        Veterinario.apellidos.asc()
    ).all()

    for v in veterinarios:
        print(v.id, v.apellidos, v.nombres,
              v.licencia_profesional)

    print("\n--- HISTORIAS CLINICAS ORDENADAS POR FECHA ---")

    historias = session.query(HistoriaClinica).order_by(
        HistoriaClinica.fecha_atencion.desc()
    ).all()

    for h in historias:
        print(h.id, h.nombre_mascota,
              h.fecha_atencion, h.diagnostico)