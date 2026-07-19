BEGIN;

-- ============================================================
-- DATOS FICTICIOS DE DESARROLLO
-- ============================================================
-- Este archivo debe ejecutarse después de:
-- 01-esquema.sql
-- 02-datos-iniciales.sql
--
-- No ejecutar en producción.
-- ============================================================

-- ------------------------------------------------------------
-- PERSONAS
-- ------------------------------------------------------------

INSERT INTO public.personas
(
    nombre,
    apellido,
    email,
    telefono,
    whatsapp,
    emailvalidado,
    origen,
    activo
)
VALUES
(
    'Ana',
    'Martínez',
    'ana.martinez@test.portalpericial.com',
    '1123456701',
    '1123456701',
    TRUE,
    'CHARLA',
    TRUE
),
(
    'Bruno',
    'Fernández',
    'bruno.fernandez@test.portalpericial.com',
    '1123456702',
    '1123456702',
    TRUE,
    'CHARLA',
    TRUE
),
(
    'Carla',
    'López',
    'carla.lopez@test.portalpericial.com',
    '1123456703',
    '1123456703',
    FALSE,
    'WEB',
    TRUE
),
(
    'Diego',
    'Sánchez',
    'diego.sanchez@test.portalpericial.com',
    '1123456704',
    '1123456704',
    TRUE,
    'CHARLA',
    TRUE
),
(
    'Elena',
    'Romero',
    'elena.romero@test.portalpericial.com',
    '1123456705',
    '1123456705',
    FALSE,
    'WEB',
    TRUE
),
(
    'Federico',
    'Gómez',
    'federico.gomez@test.portalpericial.com',
    '1123456706',
    '1123456706',
    TRUE,
    'CHARLA',
    TRUE
),
(
    'Gabriela',
    'Torres',
    'gabriela.torres@test.portalpericial.com',
    '1123456707',
    '1123456707',
    TRUE,
    'CHARLA',
    TRUE
),
(
    'Hernán',
    'Ruiz',
    'hernan.ruiz@test.portalpericial.com',
    '1123456708',
    '1123456708',
    FALSE,
    'WEB',
    TRUE
),
(
    'Inés',
    'Castro',
    'ines.castro@test.portalpericial.com',
    '1123456709',
    '1123456709',
    TRUE,
    'CHARLA',
    TRUE
),
(
    'Javier',
    'Medina',
    'javier.medina@test.portalpericial.com',
    '1123456710',
    '1123456710',
    FALSE,
    'WEB',
    TRUE
)
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- INSCRIPCIONES AL EVENTO DEL SÁBADO
-- ------------------------------------------------------------

INSERT INTO public.inscripcioneseventos
(
    personaid,
    eventoid,
    estado,
    fechainscripcion,
    observaciones
)
SELECT
    p.personaid,
    e.eventoid,
    d.estado,
    d.fechainscripcion,
    d.observaciones
FROM
(
    VALUES
        (
            'ana.martinez@test.portalpericial.com',
            'ASISTIO',
            '2026-07-20 09:15:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'bruno.fernandez@test.portalpericial.com',
            'ASISTIO',
            '2026-07-21 14:30:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'carla.lopez@test.portalpericial.com',
            'AUSENTE',
            '2026-07-22 11:10:00-03'::TIMESTAMPTZ,
            'No se conectó a la charla.'
        ),
        (
            'diego.sanchez@test.portalpericial.com',
            'CONFIRMADO',
            '2026-07-23 18:40:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'elena.romero@test.portalpericial.com',
            'CANCELADO',
            '2026-07-24 08:05:00-03'::TIMESTAMPTZ,
            'Canceló por incompatibilidad horaria.'
        ),
        (
            'federico.gomez@test.portalpericial.com',
            'INSCRIPTO',
            '2026-07-25 16:20:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'gabriela.torres@test.portalpericial.com',
            'INSCRIPTO',
            '2026-07-26 10:00:00-03'::TIMESTAMPTZ,
            NULL
        )
) AS d(email, estado, fechainscripcion, observaciones)
JOIN public.personas p
    ON lower(btrim(p.email)) = lower(btrim(d.email))
JOIN public.eventos e
    ON e.slug = 'charla-informativa-sabado-2026-08-01'
ON CONFLICT (personaid, eventoid) DO NOTHING;

-- ------------------------------------------------------------
-- INSCRIPCIONES AL EVENTO DEL MARTES
-- ------------------------------------------------------------

INSERT INTO public.inscripcioneseventos
(
    personaid,
    eventoid,
    estado,
    fechainscripcion,
    observaciones
)
SELECT
    p.personaid,
    e.eventoid,
    d.estado,
    d.fechainscripcion,
    d.observaciones
FROM
(
    VALUES
        (
            'ana.martinez@test.portalpericial.com',
            'CONFIRMADO',
            '2026-07-20 09:18:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'diego.sanchez@test.portalpericial.com',
            'INSCRIPTO',
            '2026-07-23 18:42:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'federico.gomez@test.portalpericial.com',
            'INSCRIPTO',
            '2026-07-25 16:23:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'gabriela.torres@test.portalpericial.com',
            'CONFIRMADO',
            '2026-07-26 10:04:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'hernan.ruiz@test.portalpericial.com',
            'INSCRIPTO',
            '2026-07-27 12:15:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'ines.castro@test.portalpericial.com',
            'INSCRIPTO',
            '2026-07-28 19:30:00-03'::TIMESTAMPTZ,
            NULL
        ),
        (
            'javier.medina@test.portalpericial.com',
            'CANCELADO',
            '2026-07-29 09:50:00-03'::TIMESTAMPTZ,
            'Solicitó cancelar la inscripción.'
        )
) AS d(email, estado, fechainscripcion, observaciones)
JOIN public.personas p
    ON lower(btrim(p.email)) = lower(btrim(d.email))
JOIN public.eventos e
    ON e.slug = 'charla-informativa-martes-2026-08-04'
ON CONFLICT (personaid, eventoid) DO NOTHING;

COMMIT;