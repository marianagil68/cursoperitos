from app.config.database import Database


class EventoRepository:
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
                capacidad,
                urlacceso
            FROM public.eventos
            WHERE activo = TRUE
              AND visibleweb = TRUE
              AND fechainicio > CURRENT_TIMESTAMP
            ORDER BY fechainicio
        """

        with Database() as db:
            return db.obtenertodos(sql)
        
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