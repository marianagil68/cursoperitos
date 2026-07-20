from unittest.mock import Mock

import pytest

from app import createapp
from app.correos.service import CorreoService
from app.inscripciones import controller
from app.personas.service import PersonaService
from app.shared.exceptions import ErrorReenvioReciente


@pytest.fixture
def cliente():
    aplicacion = createapp()
    aplicacion.config.update(TESTING=True)

    return aplicacion.test_client()


def test_endpoint_reenvia_correo(cliente, monkeypatch):
    resultado = {
        "correoenviado": True,
        "mensaje": "Te reenviamos el correo con los datos de acceso."
    }
    reenviar = Mock(return_value=resultado)

    monkeypatch.setattr(
        controller.personaservice,
        "reenviarcorreoinscripcion",
        reenviar
    )

    respuesta = cliente.post(
        "/api/inscripciones/reenviar-correo",
        json={
            "email": "persona@example.com",
            "eventoid": 1
        }
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json() == resultado
    reenviar.assert_called_once_with("persona@example.com", 1)


def test_endpoint_limita_reenvios_recientes(cliente, monkeypatch):
    reenviar = Mock(side_effect=ErrorReenvioReciente("Esperá unos minutos."))

    monkeypatch.setattr(
        controller.personaservice,
        "reenviarcorreoinscripcion",
        reenviar
    )

    respuesta = cliente.post(
        "/api/inscripciones/reenviar-correo",
        json={
            "email": "persona@example.com",
            "eventoid": 1
        }
    )

    assert respuesta.status_code == 429
    assert respuesta.get_json() == {"error": "Esperá unos minutos."}


def test_servicio_verifica_inscripcion_antes_de_reenviar():
    servicio = PersonaService()
    servicio.repository = Mock()
    servicio.inscripcioneservice = Mock()
    servicio.eventoservice = Mock()
    servicio.correoservice = Mock()

    servicio.repository.obtenerporemail.return_value = {
        "personaid": 9,
        "nombre": "Persona",
        "apellido": "Prueba",
        "email": "persona@example.com"
    }
    servicio.inscripcioneservice.obtener.return_value = None

    with pytest.raises(LookupError):
        servicio.reenviarcorreoinscripcion(
            "persona@example.com",
            1
        )

    servicio.correoservice.reenviarconfirmacioncharla.assert_not_called()


def test_servicio_reenvia_solo_a_persona_inscripta():
    servicio = PersonaService()
    servicio.repository = Mock()
    servicio.inscripcioneservice = Mock()
    servicio.eventoservice = Mock()
    servicio.correoservice = Mock()

    persona = {
        "personaid": 9,
        "nombre": "Persona",
        "apellido": "Prueba",
        "email": "persona@example.com"
    }
    evento = {
        "eventoid": 1,
        "titulo": "Charla de prueba",
        "urlacceso": "https://zoom.example.com/prueba"
    }

    servicio.repository.obtenerporemail.return_value = persona
    servicio.inscripcioneservice.obtener.return_value = {
        "inscripcioneventoid": 15
    }
    servicio.eventoservice.obtenerpublicoporid.return_value = {
        "eventoid": 1
    }
    servicio.eventoservice.obtenerporid.return_value = evento

    resultado = servicio.reenviarcorreoinscripcion(
        "PERSONA@example.com",
        1
    )

    assert resultado["correoenviado"] is True
    servicio.correoservice.reenviarconfirmacioncharla.assert_called_once_with(
        persona,
        evento
    )


def test_correo_reenviado_respeta_limite_de_cinco_minutos():
    servicio = CorreoService()
    servicio.repository = Mock()
    servicio.repository.hayenviadoreciente.return_value = True
    servicio.enviar = Mock()

    persona = {
        "personaid": 9,
        "email": "persona@example.com"
    }
    evento = {
        "eventoid": 1
    }

    with pytest.raises(ErrorReenvioReciente):
        servicio.reenviarconfirmacioncharla(persona, evento)

    servicio.enviar.assert_not_called()


def test_correo_reenviado_no_avisa_al_administrador():
    servicio = CorreoService()
    servicio.repository = Mock()
    servicio.repository.hayenviadoreciente.return_value = False
    servicio.enviar = Mock(return_value={
        "correoid": 20,
        "estado": "ENVIADO"
    })
    servicio._crearhtmlconfirmacioncharla = Mock(
        return_value="<p>Confirmación</p>"
    )

    persona = {
        "personaid": 9,
        "email": "persona@example.com"
    }
    evento = {
        "eventoid": 1
    }

    resultado = servicio.reenviarconfirmacioncharla(persona, evento)

    assert resultado["estado"] == "ENVIADO"
    servicio.enviar.assert_called_once_with(
        personaid=9,
        eventoid=1,
        destinatario="persona@example.com",
        asunto=servicio.ASUNTO_REENVIO_CONFIRMACION_CHARLA,
        html="<p>Confirmación</p>"
    )
