from app.config.database import Database


class CorreoRepository:

    def hayenviadoreciente(
        self,
        personaid,
        eventoid,
        destinatario,
        asunto,
        minutos
    ):
        sql = """
            SELECT EXISTS
            (
                SELECT 1
                FROM public.correos
                WHERE personaid IS NOT DISTINCT FROM %s
                  AND eventoid IS NOT DISTINCT FROM %s
                  AND lower(destinatario) = lower(%s)
                  AND asunto = %s
                  AND estado IN ('PENDIENTE', 'ENVIADO')
                  AND fechacreacion >= (
                      CURRENT_TIMESTAMP - (%s * INTERVAL '1 minute')
                  )
            ) AS existe;
        """

        with Database() as db:
            fila = db.obteneruno(
                sql,
                (
                    personaid,
                    eventoid,
                    destinatario,
                    asunto,
                    minutos
                )
            )

        return fila["existe"]

    def obtenerenviado(
        self,
        personaid,
        eventoid,
        destinatario,
        asunto
    ):

        sql = """
            SELECT
                correoid,
                estado,
                fechaenviosmtp,
                messageid
            FROM public.correos
            WHERE personaid IS NOT DISTINCT FROM %s
              AND eventoid IS NOT DISTINCT FROM %s
              AND lower(destinatario) = lower(%s)
              AND asunto = %s
              AND estado = 'ENVIADO'
            ORDER BY fechacreacion DESC
            LIMIT 1;
        """

        with Database() as db:
            return db.obteneruno(
                sql,
                (
                    personaid,
                    eventoid,
                    destinatario,
                    asunto
                )
            )

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
