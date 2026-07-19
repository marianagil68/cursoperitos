from app.config.database import Database


class CorreoRepository:

    def crear(
        self,
        personaid,
        eventoid,
        remitente,
        destinatario,
        asunto,
        cuerpohtml
    ):

        sql = """
            INSERT INTO public.correos
            (
                personaid,
                eventoid,
                remitente,
                destinatario,
                asunto,
                cuerpohtml,
                estado
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'PENDIENTE'
            )
            RETURNING correoid;
        """

        with Database() as db:

            correo = db.obteneruno(
                sql,
                (
                    personaid,
                    eventoid,
                    remitente,
                    destinatario,
                    asunto,
                    cuerpohtml
                )
            )

            return correo["correoid"]

    def marcarenviado(
        self,
        correoid,
        messageid=None
    ):

        sql = """
            UPDATE public.correos
            SET
                estado = 'ENVIADO',
                fechaenviosmtp = CURRENT_TIMESTAMP,
                intentos = intentos + 1,
                messageid = %s,
                error = NULL
            WHERE correoid = %s;
        """

        with Database() as db:

            db.ejecutar(
                sql,
                (
                    messageid,
                    correoid
                )
            )

    def marcarerror(
        self,
        correoid,
        error
    ):

        sql = """
            UPDATE public.correos
            SET
                estado = 'ERROR',
                intentos = intentos + 1,
                error = %s
            WHERE correoid = %s;
        """

        with Database() as db:

            db.ejecutar(
                sql,
                (
                    str(error),
                    correoid
                )
            )

    def obtenerporid(
        self,
        correoid
    ):

        sql = """
            SELECT
                correoid,
                personaid,
                eventoid,
                remitente,
                destinatario,
                asunto,
                cuerpohtml,
                fechacreacion,
                fechaenviosmtp,
                estado,
                intentos,
                error,
                messageid
            FROM public.correos
            WHERE correoid = %s;
        """

        with Database() as db:

            return db.obteneruno(
                sql,
                (
                    correoid,
                )
            )