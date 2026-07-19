from app.config.database import Database


class InscripcionEventoRepository:

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