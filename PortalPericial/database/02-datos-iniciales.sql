BEGIN;

INSERT INTO public.eventos
(
    titulo,
    slug,
    descripcion,
    fechainicio,
    fechafin,
    capacidad
)
VALUES
(
    'Charla informativa - Sábado 1 de agosto',
    'charla-informativa-sabado-2026-08-01',
    'Presentación del Curso de Perito Informático.',
    '2026-08-01 10:00:00-03',
    '2026-08-01 11:30:00-03',
    NULL
),
(
    'Charla informativa - Martes 4 de agosto',
    'charla-informativa-martes-2026-08-04',
    'Presentación del Curso de Perito Informático.',
    '2026-08-04 20:00:00-03',
    '2026-08-04 21:30:00-03',
    NULL
);

COMMIT;