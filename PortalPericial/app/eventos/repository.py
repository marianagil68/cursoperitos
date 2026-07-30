from app.config.database import Database


class EventoRepository:

    def obtenerproximosentrehoras(self, desdehoras, hastahoras):
        sql = """
            SELECT
                eventoid,
                titulo,
                slug,
                descripcion,
                fechainicio,
                fechafin,
                capacidad,
                visibleweb,
                activo,
                fechacreacion,
                fechaactualizacion,
                urlacceso
            FROM public.eventos
            WHERE activo = TRUE
              AND fechainicio >= (
                  CURRENT_TIMESTAMP + (%s * INTERVAL '1 hour')
              )
              AND fechainicio < (
                  CURRENT_TIMESTAMP + (%s * INTERVAL '1 hour')
              )
            ORDER BY fechainicio
        """

        with Database() as db:
            return db.obtenertodos(
                sql,
                (desdehoras, hastahoras)
            )

    def obtenertodos(self):
        sql = """
            SELECT
                eventoid,
                titulo,
                slug,
                descripcion,
                fechainicio,
                fechafin,
                capacidad,
                visibleweb,
                activo,
                fechacreacion,
                fechaactualizacion,
                urlacceso
            FROM public.eventos
            ORDER BY fechainicio
        """

        with Database() as db:
            return db.obtenertodos(sql)

    def obtenerpublicosproximos(self):
        sql = """
            SELECT
                eventoid,
                titulo,
                slug,
                descripcion,
                fechainicio,
                fechafin,
                capacidad
            FROM public.eventos
            WHERE activo = TRUE
              AND visibleweb = TRUE
              AND fechainicio > CURRENT_TIMESTAMP
            ORDER BY fechainicio
        """

        with Database() as db:
            return db.obtenertodos(sql)

    def obtenerpublicoporid(self, eventoid):
        sql = """
            SELECT
                eventoid,
                titulo,
                slug,
                descripcion,
                fechainicio,
                fechafin,
                capacidad
            FROM public.eventos
            WHERE eventoid = %s
              AND activo = TRUE
              AND visibleweb = TRUE
              AND fechainicio > CURRENT_TIMESTAMP
        """

        with Database() as db:
            return db.obteneruno(sql, (eventoid,))

    def obtenerporid(self, eventoid):
        sql = """
            SELECT
                eventoid,
                titulo,
                slug,
                descripcion,
                fechainicio,
                fechafin,
                capacidad,
                visibleweb,
                activo,
                fechacreacion,
                fechaactualizacion,
                urlacceso
            FROM public.eventos
            WHERE eventoid = %s
        """

        with Database() as db:
            return db.obteneruno(sql, (eventoid,))
