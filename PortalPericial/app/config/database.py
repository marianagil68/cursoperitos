import psycopg
from psycopg.rows import dict_row

from app.config.config import Config


class Database:
    def __init__(self):
        self.conexion = None

    def __enter__(self):
        self.conexion = psycopg.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            row_factory=dict_row
        )

        return self

    def __exit__(self, tipoerror, valorerror, traceback):
        if self.conexion is None:
            return

        try:
            if tipoerror is None:
                self.conexion.commit()
            else:
                self.conexion.rollback()
        finally:
            self.conexion.close()

    def ejecutar(self, sql, parametros=None):
        return self.conexion.execute(sql, parametros)

    def obteneruno(self, sql, parametros=None):
        cursor = self.ejecutar(sql, parametros)
        return cursor.fetchone()

    def obtenertodos(self, sql, parametros=None):
        cursor = self.ejecutar(sql, parametros)
        return cursor.fetchall()