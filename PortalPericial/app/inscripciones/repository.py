from app.config.database import Database


class InscripcionEventoRepository:

    def obtenerpersonasactivas(self, eventoid):
        sql = """
            SELECT
                p.personaid,
                p.nombre,
                p.apellido,
                p.email,
                p.whatsapp
            FROM public.inscripcioneseventos AS i
            INNER JOIN public.personas AS p
                ON p.personaid = i.personaid
            WHERE i.eventoid = %s
              AND i.estado IN ('INSCRIPTO', 'CONFIRMADO')
              AND p.activo = TRUE
            ORDER BY p.apellido, p.nombre, p.personaid
        """

        with Database() as db:
            return db.obtenertodos(sql, (eventoid,))

    def obtener(self, personaid, eventoid):
        sql = """
            SELECT *
            FROM inscripcioneseventos
            WHERE personaid = %s
              AND eventoid = %s
        """

        with Database() as db:
            return db.obteneruno(sql, (personaid, eventoid))

    def insertar(
        self,
        personaid,
        eventoid,
        estado="INSCRIPTO",
        observaciones=None
    ):
        sql = """
            INSERT INTO inscripcioneseventos
            (
                personaid,
                eventoid,
                estado,
                observaciones
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (personaid, eventoid) DO NOTHING
            RETURNING inscripcioneventoid
        """

        with Database() as db:
            fila = db.obteneruno(
                sql,
                (
                    personaid,
                    eventoid,
                    estado,
                    observaciones
                )
            )

        if fila is None:
            return None

        return fila["inscripcioneventoid"]

    def actualizarestado(
        self,
        personaid,
        eventoid,
        estado
    ):
        sql = """
            UPDATE inscripcioneseventos
            SET estado = %s,
                fechaactualizacion = CURRENT_TIMESTAMP
            WHERE personaid = %s
              AND eventoid = %s
        """

        with Database() as db:
            db.ejecutar(
                sql,
                (
                    estado,
                    personaid,
                    eventoid
                )
            )
