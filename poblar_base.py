
from datetime import date
from sqlalchemy.orm import Session
from crear_base_entidades import (
    engine, Clinica, Consultorio,
    Veterinario, HistoriaClinica
)

with Session(engine) as session:

    if session.query(Clinica).count() > 0:

        # Actualizar direcciones de las clinicas existentes
        session.query(Clinica).filter(
            Clinica.nombre_comercial == "Animal Health"
        ).update({"direccion": "Av. Universitaria, Loja"})

        session.query(Clinica).filter(
            Clinica.nombre_comercial == "PetLife"
        ).update({"direccion": "Av. 25 de Junio, Machala"})

        session.commit()

        print("Direcciones actualizadas correctamente.")

    else:
        # Clinicas
        c1 = Clinica(
            nombre_comercial="VetCare",
            direccion="Av. Loja, Cuenca",
            veterinario_responsable="Carlos Torres"
        )

        c2 = Clinica(
            nombre_comercial="Animal Health",
            direccion="Av. Universitaria, Loja",
            veterinario_responsable="Ana Molina"
        )

        c3 = Clinica(
            nombre_comercial="PetLife",
            direccion="Av. 25 de Junio, Machala",
            veterinario_responsable="Diego Castro"
        )

        # Consultorios
        co1 = Consultorio(
            nombre="Consultorio 1",
            especialidad="Medicina general",
            clinica=c1
        )

        co2 = Consultorio(
            nombre="Consultorio 2",
            especialidad="Cirugia",
            clinica=c1
        )

        co3 = Consultorio(
            nombre="Consultorio 3",
            especialidad="Dermatologia",
            clinica=c2
        )

        co4 = Consultorio(
            nombre="Consultorio 4",
            especialidad="Medicina general",
            clinica=c3
        )

        # Veterinarios
        v1 = Veterinario(
            nombres="Carlos",
            apellidos="Torres",
            correo="carlos@example.com",
            licencia_profesional="VET001",
            consultorio=co1
        )

        v2 = Veterinario(
            nombres="Maria",
            apellidos="Lopez",
            correo="maria@example.com",
            licencia_profesional="VET002",
            consultorio=co2
        )

        v3 = Veterinario(
            nombres="Ana",
            apellidos="Molina",
            correo="ana@example.com",
            licencia_profesional="VET003",
            consultorio=co3
        )

        v4 = Veterinario(
            nombres="Diego",
            apellidos="Castro",
            correo="diego@example.com",
            licencia_profesional="VET004",
            consultorio=co4
        )

        # Historias clinicas
        h1 = HistoriaClinica(
            fecha_atencion=date(2026, 11, 10),
            diagnostico="Gastritis",
            tratamiento="Dieta especial",
            nombre_mascota="Max",
            veterinario=v1
        )

        h2 = HistoriaClinica(
            fecha_atencion=date(2026, 11, 12),
            diagnostico="Fractura",
            tratamiento="Cirugia",
            nombre_mascota="Rocky",
            veterinario=v2
        )

        h3 = HistoriaClinica(
            fecha_atencion=date(2026, 11, 14),
            diagnostico="Dermatitis",
            tratamiento="Tratamiento topico",
            nombre_mascota="Luna",
            veterinario=v3
        )

        h4 = HistoriaClinica(
            fecha_atencion=date(2026, 11, 16),
            diagnostico="Parasitosis",
            tratamiento="Desparasitacion",
            nombre_mascota="Toby",
            veterinario=v4
        )

        h5 = HistoriaClinica(
            fecha_atencion=date(2026, 11, 18),
            diagnostico="Otitis",
            tratamiento="Limpieza auricular",
            nombre_mascota="Nina",
            veterinario=v1
        )

        h6 = HistoriaClinica(
            fecha_atencion=date(2026, 11, 20),
            diagnostico="Dermatitis",
            tratamiento="Champu medicado",
            nombre_mascota="Coco",
            veterinario=v3
        )

        session.add_all([h1, h2, h3, h4, h5, h6])
        session.commit()

        print("Datos ingresados correctamente.")
