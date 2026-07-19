from app.config.database import Database


def main():
    sql = """
        SELECT
            current_database() AS basedatos,
            current_user AS usuario,
            version() AS version
    """

    with Database() as db:
        resultado = db.obteneruno(sql)

    print()
    print("Conexión exitosa")
    print("----------------")
    print(f"Base de datos : {resultado['basedatos']}")
    print(f"Usuario       : {resultado['usuario']}")
    print(f"Versión       : {resultado['version']}")
    print()


if __name__ == "__main__":
    main()