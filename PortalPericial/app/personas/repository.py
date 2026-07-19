from app.config.database import Database


class PersonaRepository:

    def obtenerporid(self, personaid):
        sql = """
            SELECT *
            FROM personas
            WHERE personaid = %s
        """

        with Database() as db:
            return db.obteneruno(sql, (personaid,))

    def obtenerporemail(self, email):
        sql = """
            SELECT *
            FROM personas
            WHERE lower(email) = lower(%s)
        """

        with Database() as db:
            return db.obteneruno(sql, (email,))

    def insertar(
        self,
        nombre,
        apellido,
        email,
        telefono,
        whatsapp,
        origen
    ):
        sql = """
            INSERT INTO personas
            (
                nombre,
                apellido,
                email,
                telefono,
                whatsapp,
                origen
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING personaid
        """

        with Database() as db:
            fila = db.obteneruno(
                sql,
                (
                    nombre,
                    apellido,
                    email,
                    telefono,
                    whatsapp,
                    origen
                )
            )

        return fila["personaid"]

    def actualizarultimoacceso(self, personaid):
        sql = """
            UPDATE personas
            SET fechaultimoacceso = CURRENT_TIMESTAMP
            WHERE personaid = %s
        """

        with Database() as db:
            db.ejecutar(sql, (personaid,))