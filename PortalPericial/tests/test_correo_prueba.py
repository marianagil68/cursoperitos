from unittest.mock import Mock

from app import createapp
from app.config.config import Config
from app.correos import controller


def test_endpoint_prueba_no_existe_en_produccion(monkeypatch):
    enviar = Mock()
    monkeypatch.setattr(controller.service, "enviar", enviar)

    aplicacion = createapp()
    aplicacion.config.update(TESTING=True, DEBUG=False)
    cliente = aplicacion.test_client()

    respuesta = cliente.get("/correos/prueba")

    assert respuesta.status_code == 404
    enviar.assert_not_called()


def test_endpoint_prueba_funciona_en_desarrollo(monkeypatch):
    enviar = Mock(return_value={
        "correoid": 25,
        "estado": "ENVIADO"
    })
    monkeypatch.setattr(controller.service, "enviar", enviar)

    aplicacion = createapp()
    aplicacion.config.update(TESTING=True, DEBUG=True)
    cliente = aplicacion.test_client()

    respuesta = cliente.get("/correos/prueba")

    assert respuesta.status_code == 200
    assert respuesta.get_json() == {
        "ok": True,
        "correoid": {
            "correoid": 25,
            "estado": "ENVIADO"
        }
    }
    enviar.assert_called_once()
    assert (
        enviar.call_args.kwargs["destinatario"]
        == Config.SMTP_DESTINATARIO_ADMIN
    )
