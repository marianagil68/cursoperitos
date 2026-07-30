import click
import re

from flask import current_app

from app.correos.service import CorreoService
from app.eventos.service import EventoService
from app.inscripciones.repository import InscripcionEventoRepository


def registrarcomandos(app):
    app.cli.add_command(enviarrecordatorios)


def validaremailprueba(contexto, parametro, valor):
    if valor is None:
        return None

    valor = valor.strip().lower()

    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor) is None:
        raise click.BadParameter(
            "debe ser una dirección de correo válida."
        )

    return valor


@click.command("enviar-recordatorios")
@click.option(
    "--desde-horas",
    type=click.FloatRange(min=0),
    default=23.5,
    show_default=True,
    help="Inicio de la ventana previa al evento."
)
@click.option(
    "--hasta-horas",
    type=click.FloatRange(min=0),
    default=24.5,
    show_default=True,
    help="Fin de la ventana previa al evento."
)
@click.option(
    "--simular",
    is_flag=True,
    help="Muestra los destinatarios sin enviar correos."
)
@click.option(
    "--destinatario-prueba",
    callback=validaremailprueba,
    help="Envía como máximo una prueba por evento a esta dirección."
)
@click.option(
    "--evento-id",
    type=click.IntRange(min=1),
    help="Procesa exclusivamente el evento indicado."
)
@click.option(
    "--nombre-prueba",
    help="Nombre utilizado en el saludo del correo de prueba."
)
def enviarrecordatorios(
    desde_horas,
    hasta_horas,
    simular,
    destinatario_prueba,
    evento_id,
    nombre_prueba
):
    """Envía una vez el recordatorio de eventos que comienzan en 24 horas."""
    if desde_horas >= hasta_horas:
        raise click.UsageError(
            "--desde-horas debe ser menor que --hasta-horas."
        )

    if simular and destinatario_prueba:
        raise click.UsageError(
            "--simular y --destinatario-prueba no pueden usarse juntos."
        )

    if nombre_prueba and not destinatario_prueba:
        raise click.UsageError(
            "--nombre-prueba requiere --destinatario-prueba."
        )

    eventoservice = EventoService()
    inscripcionesrepository = InscripcionEventoRepository()
    correoservice = CorreoService()
    if evento_id:
        evento = eventoservice.obtenerporid(evento_id)

        if evento is None:
            raise click.ClickException(
                f"No existe el evento con id {evento_id}."
            )

        eventos = [evento]
    else:
        eventos = eventoservice.obtenerproximosentrehoras(
            desde_horas,
            hasta_horas
        )

    enviados = 0
    omitidos = 0
    simulados = 0
    errores = 0

    if simular:
        click.echo("SIMULACIÓN: no se enviarán correos.\n")

    if destinatario_prueba:
        click.echo(
            "MODO PRUEBA: los participantes no recibirán correos. "
            f"Destinatario: {destinatario_prueba}\n"
        )

    for evento in eventos:
        personas = inscripcionesrepository.obtenerpersonasactivas(
            evento["eventoid"]
        )

        if simular:
            click.echo(f"Evento: {evento['titulo']}")
            click.echo(
                f"Fecha: {correoservice._formatearfecha(evento['fechainicio'])}"
            )

            if not personas:
                click.echo("Sin inscripciones activas.\n")
                continue

            for persona in personas:
                click.echo(
                    f"- {persona['nombre']} {persona['apellido']} "
                    f"<{persona['email']}>"
                )
                simulados += 1

            click.echo("")
            continue

        if destinatario_prueba:
            if not personas:
                omitidos += 1
                continue

            try:
                personaprueba = {
                    **personas[0],
                    "nombre": nombre_prueba or "Participante"
                }
                correoservice.enviarrecordatorioprueba(
                    personaprueba,
                    evento,
                    destinatario_prueba
                )
                enviados += 1
            except Exception:
                errores += 1
                current_app.logger.exception(
                    "No se pudo enviar el recordatorio de prueba "
                    "del evento %s.",
                    evento["eventoid"]
                )

            continue

        for persona in personas:
            try:
                resultado = correoservice.enviarrecordatoriocharla(
                    persona,
                    evento
                )

                if resultado["correoenviado"]:
                    enviados += 1
                else:
                    omitidos += 1
            except Exception:
                errores += 1
                current_app.logger.exception(
                    "No se pudo enviar el recordatorio del evento %s "
                    "a la persona %s.",
                    evento["eventoid"],
                    persona["personaid"]
                )

    click.echo(
        f"Eventos: {len(eventos)} | Enviados: {enviados} | "
        f"Simulados: {simulados} | Omitidos: {omitidos} | "
        f"Errores: {errores}"
    )

    if errores:
        raise click.ClickException(
            "Algunos recordatorios no pudieron enviarse."
        )
