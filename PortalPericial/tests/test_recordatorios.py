from datetime import datetime
from datetime import timezone
from unittest.mock import Mock

from app import createapp
from app.config.config import Config
from app.correos.service import CorreoService


def test_recordatorio_se_envia_una_sola_vez():
    servicio = CorreoService()
    servicio.repository = Mock()
    servicio.repository.obtenerenviado.return_value = None
    servicio.enviar = Mock(return_value={
        "correoid": 31,
        "estado": "ENVIADO"
    })

    persona = {
        "personaid": 9,
        "nombre": "Mariana",
        "email": "mariana@example.com"
    }
    evento = {
        "eventoid": 1,
        "titulo": "Charla de prueba",
        "fechainicio": datetime(2026, 8, 1, 13, tzinfo=timezone.utc),
        "urlacceso": "https://zoom.example.com/reunion"
    }

    resultado = servicio.enviarrecordatoriocharla(persona, evento)

    assert resultado["correoenviado"] is True
    html = servicio.enviar.call_args.kwargs["html"]
    assert "Mañana nos encontramos" in html
    assert "sábado 1 de agosto de 2026 · 10:00 hs" in html
    assert "https://zoom.example.com/reunion" in html


def test_recordatorio_ya_enviado_se_omite():
    servicio = CorreoService()
    servicio.repository = Mock()
    servicio.repository.obtenerenviado.return_value = {
        "correoid": 31,
        "estado": "ENVIADO"
    }
    servicio.enviar = Mock()

    resultado = servicio.enviarrecordatoriocharla(
        {
            "personaid": 9,
            "email": "mariana@example.com"
        },
        {
            "eventoid": 1
        }
    )

    assert resultado == {
        "correoenviado": False,
        "motivo": "YA_ENVIADO"
    }
    servicio.enviar.assert_not_called()


def test_comando_envia_a_inscripciones_activas(monkeypatch):
    eventoservice = Mock()
    inscripcionesrepository = Mock()
    correoservice = Mock()
    evento = {"eventoid": 1}
    personas = [
        {"personaid": 8},
        {"personaid": 9}
    ]

    eventoservice.obtenerproximosentrehoras.return_value = [evento]
    inscripcionesrepository.obtenerpersonasactivas.return_value = personas
    correoservice.enviarrecordatoriocharla.side_effect = [
        {"correoenviado": True},
        {"correoenviado": False}
    ]

    monkeypatch.setattr(
        "app.correos.commands.EventoService",
        Mock(return_value=eventoservice)
    )
    monkeypatch.setattr(
        "app.correos.commands.InscripcionEventoRepository",
        Mock(return_value=inscripcionesrepository)
    )
    monkeypatch.setattr(
        "app.correos.commands.CorreoService",
        Mock(return_value=correoservice)
    )

    runner = createapp().test_cli_runner()
    resultado = runner.invoke(args=["enviar-recordatorios"])

    assert resultado.exit_code == 0
    assert (
        "Eventos: 1 | Enviados: 1 | Simulados: 0 | "
        "Omitidos: 1 | Errores: 0"
    ) in (
        resultado.output
    )
    eventoservice.obtenerproximosentrehoras.assert_called_once_with(
        23.5,
        24.5
    )
    assert correoservice.enviarrecordatoriocharla.call_count == 2


def test_comando_simula_sin_enviar(monkeypatch):
    eventoservice = Mock()
    inscripcionesrepository = Mock()
    correoservice = Mock()
    evento = {
        "eventoid": 1,
        "titulo": "Charla de prueba",
        "fechainicio": datetime(2026, 8, 1, 13, tzinfo=timezone.utc)
    }
    persona = {
        "personaid": 9,
        "nombre": "Mariana",
        "apellido": "Gil",
        "email": "mariana@example.com"
    }

    eventoservice.obtenerproximosentrehoras.return_value = [evento]
    inscripcionesrepository.obtenerpersonasactivas.return_value = [persona]
    correoservice._formatearfecha.return_value = (
        "sábado 1 de agosto de 2026 · 10:00 hs"
    )

    monkeypatch.setattr(
        "app.correos.commands.EventoService",
        Mock(return_value=eventoservice)
    )
    monkeypatch.setattr(
        "app.correos.commands.InscripcionEventoRepository",
        Mock(return_value=inscripcionesrepository)
    )
    monkeypatch.setattr(
        "app.correos.commands.CorreoService",
        Mock(return_value=correoservice)
    )

    runner = createapp().test_cli_runner()
    resultado = runner.invoke(
        args=["enviar-recordatorios", "--simular"]
    )

    assert resultado.exit_code == 0
    assert "SIMULACIÓN: no se enviarán correos." in resultado.output
    assert "Mariana Gil <mariana@example.com>" in resultado.output
    assert "Enviados: 0 | Simulados: 1" in resultado.output
    correoservice.enviarrecordatoriocharla.assert_not_called()
    correoservice.enviarrecordatorioprueba.assert_not_called()


def test_comando_envia_una_prueba_por_evento(monkeypatch):
    eventoservice = Mock()
    inscripcionesrepository = Mock()
    correoservice = Mock()
    evento = {
        "eventoid": 1,
        "titulo": "Charla de prueba"
    }
    personas = [
        {"personaid": 8},
        {"personaid": 9}
    ]

    eventoservice.obtenerproximosentrehoras.return_value = [evento]
    inscripcionesrepository.obtenerpersonasactivas.return_value = personas

    monkeypatch.setattr(
        "app.correos.commands.EventoService",
        Mock(return_value=eventoservice)
    )
    monkeypatch.setattr(
        "app.correos.commands.InscripcionEventoRepository",
        Mock(return_value=inscripcionesrepository)
    )
    monkeypatch.setattr(
        "app.correos.commands.CorreoService",
        Mock(return_value=correoservice)
    )

    runner = createapp().test_cli_runner()
    resultado = runner.invoke(args=[
        "enviar-recordatorios",
        "--destinatario-prueba",
        "PROPIETARIA@example.com",
        "--nombre-prueba",
        "Mariana"
    ])

    assert resultado.exit_code == 0
    correoservice.enviarrecordatorioprueba.assert_called_once_with(
        {
            **personas[0],
            "nombre": "Mariana"
        },
        evento,
        "propietaria@example.com"
    )
    correoservice.enviarrecordatoriocharla.assert_not_called()


def test_comando_rechaza_modos_de_prueba_juntos():
    runner = createapp().test_cli_runner()
    resultado = runner.invoke(args=[
        "enviar-recordatorios",
        "--simular",
        "--destinatario-prueba",
        "propietaria@example.com"
    ])

    assert resultado.exit_code == 2
    assert "no pueden usarse juntos" in resultado.output


def test_recordatorio_prueba_no_se_asocia_al_participante():
    servicio = CorreoService()
    servicio.enviar = Mock(return_value={
        "correoid": 40,
        "estado": "ENVIADO"
    })
    persona = {
        "personaid": 9,
        "nombre": "Mariana"
    }
    evento = {
        "eventoid": 1,
        "titulo": "Charla de prueba",
        "fechainicio": datetime(2026, 8, 1, 13, tzinfo=timezone.utc),
        "urlacceso": "https://zoom.example.com/reunion"
    }

    servicio.enviarrecordatorioprueba(
        persona,
        evento,
        "propietaria@example.com"
    )

    assert servicio.enviar.call_args.kwargs["personaid"] is None
    assert (
        servicio.enviar.call_args.kwargs["destinatario"]
        == "propietaria@example.com"
    )
    assert "MENSAJE DE PRUEBA" in servicio.enviar.call_args.kwargs["html"]


def test_comando_simula_solamente_evento_indicado(monkeypatch):
    eventoservice = Mock()
    inscripcionesrepository = Mock()
    correoservice = Mock()
    evento = {
        "eventoid": 7,
        "titulo": "Charla seleccionada",
        "fechainicio": datetime(2026, 8, 1, 13, tzinfo=timezone.utc)
    }
    persona = {
        "personaid": 9,
        "nombre": "Mariana",
        "apellido": "Gil",
        "email": "mariana@example.com"
    }

    eventoservice.obtenerporid.return_value = evento
    inscripcionesrepository.obtenerpersonasactivas.return_value = [persona]
    correoservice._formatearfecha.return_value = (
        "sábado 1 de agosto de 2026 · 10:00 hs"
    )

    monkeypatch.setattr(
        "app.correos.commands.EventoService",
        Mock(return_value=eventoservice)
    )
    monkeypatch.setattr(
        "app.correos.commands.InscripcionEventoRepository",
        Mock(return_value=inscripcionesrepository)
    )
    monkeypatch.setattr(
        "app.correos.commands.CorreoService",
        Mock(return_value=correoservice)
    )

    runner = createapp().test_cli_runner()
    resultado = runner.invoke(args=[
        "enviar-recordatorios",
        "--evento-id",
        "7",
        "--simular"
    ])

    assert resultado.exit_code == 0
    eventoservice.obtenerporid.assert_called_once_with(7)
    eventoservice.obtenerproximosentrehoras.assert_not_called()
    assert "Charla seleccionada" in resultado.output
    correoservice.enviarrecordatoriocharla.assert_not_called()
    correoservice.enviarrecordatorioprueba.assert_not_called()


def test_comando_informa_evento_inexistente(monkeypatch):
    eventoservice = Mock()
    eventoservice.obtenerporid.return_value = None

    monkeypatch.setattr(
        "app.correos.commands.EventoService",
        Mock(return_value=eventoservice)
    )

    runner = createapp().test_cli_runner()
    resultado = runner.invoke(args=[
        "enviar-recordatorios",
        "--evento-id",
        "99",
        "--simular"
    ])

    assert resultado.exit_code == 1
    assert "No existe el evento con id 99." in resultado.output


def test_nombre_prueba_requiere_destinatario_prueba():
    runner = createapp().test_cli_runner()
    resultado = runner.invoke(args=[
        "enviar-recordatorios",
        "--nombre-prueba",
        "Mariana"
    ])

    assert resultado.exit_code == 2
    assert "requiere --destinatario-prueba" in resultado.output


def test_envio_incluye_texto_plano_y_messageid_del_dominio(monkeypatch):
    servicio = CorreoService()
    servicio.repository = Mock()
    servicio.repository.crear.return_value = 50
    servidor = Mock()

    monkeypatch.setattr(Config, "SMTP_REMITENTE", "info@portalpericial.com")
    monkeypatch.setattr(Config, "SMTP_HOST", "smtp.example.com")
    monkeypatch.setattr(Config, "SMTP_PORT", 465)
    monkeypatch.setattr(Config, "SMTP_USUARIO", "usuario")
    monkeypatch.setattr(Config, "SMTP_PASSWORD", "password")
    monkeypatch.setattr(Config, "SMTP_USAR_SSL", True)
    monkeypatch.setattr(
        "app.correos.service.smtplib.SMTP_SSL",
        Mock(return_value=servidor)
    )

    servicio.enviar(
        personaid=None,
        eventoid=1,
        destinatario="mariana@example.com",
        asunto="Mensaje de prueba",
        html=(
            "<h1>Mañana nos encontramos</h1>"
            "<p>Ingresá desde "
            '<a href="https://zoom.example.com/reunion">Zoom</a>.</p>'
        )
    )

    mensaje = servidor.send_message.call_args.args[0]
    partes = mensaje.get_payload()

    assert mensaje["Message-ID"].endswith("@portalpericial.com>")
    assert [parte.get_content_subtype() for parte in partes] == [
        "plain",
        "html"
    ]

    textoplano = partes[0].get_payload(decode=True).decode("utf-8")
    assert "Mañana nos encontramos" in textoplano
    assert "https://zoom.example.com/reunion" in textoplano
    servicio.repository.marcarenviado.assert_called_once()
