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
                fechaactualizacion
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