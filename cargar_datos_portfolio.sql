-- Carga inicial del portfolio de Mateo Benjamin Felicia.
-- Ejecutar en la base Clever Cloud ya creada. Los archivos apuntan a app/static/docs.
-- Basado en las tablas actuales del proyecto.

START TRANSACTION;

SET @perfil = (SELECT id_perfil FROM administradores LIMIT 1);
SET @es = (SELECT id_idioma FROM idiomas WHERE codigo_iso = 'es');
SET @en = (SELECT id_idioma FROM idiomas WHERE codigo_iso = 'en');
SET @fr = (SELECT id_idioma FROM idiomas WHERE codigo_iso = 'fr');
SET @id = (SELECT id_idioma FROM idiomas WHERE codigo_iso = 'id');
SET @area_prog = (SELECT id_area FROM areas_conocimiento WHERE codigo = 'programacion');
SET @area_web = (SELECT id_area FROM areas_conocimiento WHERE codigo = 'desarrollo_web');
SET @area_mat = (SELECT id_area FROM areas_conocimiento WHERE codigo = 'matematica');

UPDATE perfil
SET nombre = 'Mateo Benjamin',
    apellido = 'Felicia',
    cv_url = '/static/docs/cv_mateo_felicia.pdf',
    ubicacion = 'Córdoba Capital, Córdoba, Argentina'
WHERE id_perfil = @perfil;

INSERT INTO perfil_traduccion (id_perfil, id_idioma, titular, sobre_mi)
VALUES (@perfil, @es,
        'Estudiante avanzado de Programación en el Instituto Técnico Renault',
        'Soy estudiante avanzado del Instituto Técnico Renault, con orientación en Programación. Me interesan la tecnología, la matemática y el desarrollo de soluciones mediante software. Trabajo con Python, JavaScript, HTML y CSS, y tengo experiencia en estructuras de datos, programación orientada a objetos y manejo de JSON. Desarrollé Atlas Bíblico, un proyecto educativo para organizar información histórica y geográfica. En equipo obtuve el primer puesto en Odisea Matemática 2023. Busco seguir desarrollando mis habilidades y aportar compromiso, curiosidad y capacidad analítica a nuevos proyectos.')
ON DUPLICATE KEY UPDATE titular = VALUES(titular), sobre_mi = VALUES(sobre_mi);

UPDATE contactos SET valor = 'mateobenjaminfelicia@gmail.com', url = 'mailto:mateobenjaminfelicia@gmail.com', orden = 1, visible = TRUE
WHERE id_perfil = @perfil AND tipo = 'email';
INSERT INTO contactos (id_perfil, tipo, valor, url, orden, visible)
SELECT @perfil, 'email', 'mateobenjaminfelicia@gmail.com', 'mailto:mateobenjaminfelicia@gmail.com', 1, TRUE
WHERE NOT EXISTS (SELECT 1 FROM contactos WHERE id_perfil = @perfil AND tipo = 'email');

UPDATE contactos SET valor = '+549-351-8504620', url = 'tel:+5493518504620', orden = 2, visible = TRUE
WHERE id_perfil = @perfil AND tipo = 'telefono';
INSERT INTO contactos (id_perfil, tipo, valor, url, orden, visible)
SELECT @perfil, 'telefono', '+549-351-8504620', 'tel:+5493518504620', 2, TRUE
WHERE NOT EXISTS (SELECT 1 FROM contactos WHERE id_perfil = @perfil AND tipo = 'telefono');

UPDATE contactos SET valor = 'mateobenjaminfelicia-source', url = 'https://github.com/mateobenjaminfelicia-source', orden = 3, visible = TRUE
WHERE id_perfil = @perfil AND tipo = 'github';
INSERT INTO contactos (id_perfil, tipo, valor, url, orden, visible)
SELECT @perfil, 'github', 'mateobenjaminfelicia-source', 'https://github.com/mateobenjaminfelicia-source', 3, TRUE
WHERE NOT EXISTS (SELECT 1 FROM contactos WHERE id_perfil = @perfil AND tipo = 'github');

UPDATE contactos SET valor = 'Mateo Benjamin Felicia', url = 'https://www.linkedin.com/in/mateo-benjamin-felicia-a25544415', orden = 4, visible = TRUE
WHERE id_perfil = @perfil AND tipo = 'linkedin';
INSERT INTO contactos (id_perfil, tipo, valor, url, orden, visible)
SELECT @perfil, 'linkedin', 'Mateo Benjamin Felicia', 'https://www.linkedin.com/in/mateo-benjamin-felicia-a25544415', 4, TRUE
WHERE NOT EXISTS (SELECT 1 FROM contactos WHERE id_perfil = @perfil AND tipo = 'linkedin');

INSERT INTO perfil_idioma (id_perfil, id_idioma, nivel) VALUES
(@perfil, @es, 'nativo'), (@perfil, @en, 'B2'), (@perfil, @fr, 'A1'), (@perfil, @id, 'A1')
ON DUPLICATE KEY UPDATE nivel = VALUES(nivel);

INSERT INTO tecnologias (nombre, tipo, icono) VALUES
('Python', 'lenguaje', 'fa-brands fa-python'),
('JavaScript', 'lenguaje', 'fa-brands fa-js'),
('GitHub', 'herramienta', 'fa-brands fa-github'),
('HTML', 'marcado', 'fa-brands fa-html5'),
('CSS', 'marcado', 'fa-brands fa-css3-alt')
ON DUPLICATE KEY UPDATE tipo = VALUES(tipo), icono = VALUES(icono);

INSERT INTO perfil_tecnologia (id_perfil, id_tecnologia, nivel, orden, visible)
SELECT @perfil, t.id_tecnologia,
       CASE t.nombre WHEN 'GitHub' THEN 'avanzado' WHEN 'HTML' THEN 'basico' WHEN 'CSS' THEN 'basico' ELSE 'intermedio' END,
       CASE t.nombre WHEN 'Python' THEN 1 WHEN 'JavaScript' THEN 2 WHEN 'GitHub' THEN 3 WHEN 'HTML' THEN 4 ELSE 5 END,
       TRUE
FROM tecnologias t WHERE t.nombre IN ('Python', 'JavaScript', 'GitHub', 'HTML', 'CSS')
ON DUPLICATE KEY UPDATE nivel = VALUES(nivel), orden = VALUES(orden), visible = TRUE;

INSERT INTO organizaciones (nombre, sitio_web, ubicacion)
SELECT 'Instituto Técnico Renault', NULL, 'Córdoba, Argentina'
WHERE NOT EXISTS (SELECT 1 FROM organizaciones WHERE nombre = 'Instituto Técnico Renault');
SET @org_renault = (SELECT id_organizacion FROM organizaciones WHERE nombre = 'Instituto Técnico Renault' ORDER BY id_organizacion LIMIT 1);

INSERT INTO formaciones (id_perfil, id_organizacion, anio_inicio, anio_fin, estado, orden, visible)
SELECT @perfil, @org_renault, 2020, NULL, 'en_curso', 1, TRUE
WHERE NOT EXISTS (SELECT 1 FROM formaciones WHERE id_perfil = @perfil AND id_organizacion = @org_renault AND anio_inicio = 2020);
SET @formacion = (SELECT id_formacion FROM formaciones WHERE id_perfil = @perfil AND id_organizacion = @org_renault AND anio_inicio = 2020 ORDER BY id_formacion DESC LIMIT 1);
INSERT INTO formacion_traduccion (id_formacion, id_idioma, titulo, descripcion)
VALUES (@formacion, @es, 'Estudios técnicos con orientación en Programación',
        'Instituto Técnico Renault · 2020–actualidad. Formación en programación con Python y JavaScript, estructuras de datos, desarrollo web, bases de datos y resolución de problemas. Título previsto al egresar: Técnico en Programación.')
ON DUPLICATE KEY UPDATE titulo = VALUES(titulo), descripcion = VALUES(descripcion);

INSERT INTO proyectos (id_perfil, anio_inicio, anio_fin, estado, repositorio_url, demo_url, imagen_url, orden, visible)
SELECT @perfil, 2025, 2025, 'finalizado', NULL, NULL, NULL, 1, TRUE
WHERE NOT EXISTS (SELECT 1 FROM proyectos p JOIN proyecto_traduccion tr ON tr.id_proyecto = p.id_proyecto
                  WHERE p.id_perfil = @perfil AND tr.id_idioma = @es AND tr.nombre = 'Atlas Bíblico');
SET @proy_atlas = (SELECT p.id_proyecto FROM proyectos p
                   WHERE p.id_perfil = @perfil AND p.anio_inicio = 2025
                   ORDER BY p.id_proyecto DESC LIMIT 1);
INSERT INTO proyecto_traduccion (id_proyecto, id_idioma, nombre, descripcion, objetivo, rol)
VALUES (@proy_atlas, @es, 'Atlas Bíblico',
        'Proyecto educativo para organizar información histórica y geográfica de textos bíblicos. Implementé estructuras de datos en Python y diseñé una interfaz básica para visualizar el contenido.',
        'Organizar y facilitar la consulta de información histórica y geográfica.', 'Desarrollador')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion), objetivo = VALUES(objetivo), rol = VALUES(rol);
INSERT IGNORE INTO proyecto_area (id_proyecto, id_area) VALUES (@proy_atlas, @area_prog), (@proy_atlas, @area_web);
INSERT INTO proyecto_tecnologia (id_proyecto, id_tecnologia)
SELECT @proy_atlas, id_tecnologia FROM tecnologias WHERE nombre = 'Python'
ON DUPLICATE KEY UPDATE id_tecnologia = VALUES(id_tecnologia);

INSERT INTO organizaciones (nombre, sitio_web, ubicacion)
SELECT 'Olimpiada Matemática Argentina', NULL, 'Córdoba, Argentina'
WHERE NOT EXISTS (SELECT 1 FROM organizaciones WHERE nombre = 'Olimpiada Matemática Argentina');
SET @org_oma = (SELECT id_organizacion FROM organizaciones WHERE nombre = 'Olimpiada Matemática Argentina' ORDER BY id_organizacion LIMIT 1);

INSERT INTO reconocimientos (id_perfil, id_organizacion, anio, orden, visible)
SELECT @perfil, @org_oma, 2023, 1, TRUE
WHERE NOT EXISTS (SELECT 1 FROM reconocimientos r JOIN reconocimiento_traduccion tr ON tr.id_reconocimiento = r.id_reconocimiento
                  WHERE r.id_perfil = @perfil AND tr.id_idioma = @es AND tr.nombre = 'Odisea Matemática – primer puesto');
SET @rec_odisea = (SELECT r.id_reconocimiento FROM reconocimientos r
                   WHERE r.id_perfil = @perfil AND r.id_organizacion = @org_oma AND r.anio = 2023
                   ORDER BY r.id_reconocimiento LIMIT 1);
INSERT INTO reconocimiento_traduccion (id_reconocimiento, id_idioma, nombre, descripcion, resultado)
VALUES (@rec_odisea, @es, 'Odisea Matemática – primer puesto',
        'Instancia provincial OMA 2023. Competencia intercolegial de resolución de problemas matemáticos, realizada en La Falda, Córdoba.',
        'Primer puesto por desempeño en equipo')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion), resultado = VALUES(resultado);
INSERT IGNORE INTO reconocimiento_area (id_reconocimiento, id_area) VALUES (@rec_odisea, @area_mat);

INSERT INTO reconocimientos (id_perfil, id_organizacion, anio, orden, visible)
SELECT @perfil, @org_oma, 2025, 2, TRUE
WHERE NOT EXISTS (SELECT 1 FROM reconocimientos r JOIN reconocimiento_traduccion tr ON tr.id_reconocimiento = r.id_reconocimiento
                  WHERE r.id_perfil = @perfil AND tr.id_idioma = @es AND tr.nombre = 'Olimpiada Matemática Argentina – certamen provincial 2025');
SET @rec_oma25 = (SELECT r.id_reconocimiento FROM reconocimientos r
                  WHERE r.id_perfil = @perfil AND r.id_organizacion = @org_oma AND r.anio = 2025
                  ORDER BY r.id_reconocimiento DESC LIMIT 1);
INSERT INTO reconocimiento_traduccion (id_reconocimiento, id_idioma, nombre, descripcion, resultado)
VALUES (@rec_oma25, @es, 'Olimpiada Matemática Argentina – certamen provincial 2025',
        'Participación en el segundo nivel del certamen provincial XLII, realizado en Valle Hermoso, Córdoba.',
        'Participante · segundo nivel')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion), resultado = VALUES(resultado);
INSERT IGNORE INTO reconocimiento_area (id_reconocimiento, id_area) VALUES (@rec_oma25, @area_mat);

INSERT INTO reconocimientos (id_perfil, id_organizacion, anio, orden, visible)
SELECT @perfil, @org_oma, 2023, 3, TRUE
WHERE NOT EXISTS (SELECT 1 FROM reconocimientos r JOIN reconocimiento_traduccion tr ON tr.id_reconocimiento = r.id_reconocimiento
                  WHERE r.id_perfil = @perfil AND tr.id_idioma = @es AND tr.nombre = 'Olimpiada Cordobesa de Matemática 2023');
SET @rec_cordoba = (SELECT r.id_reconocimiento FROM reconocimientos r
                    WHERE r.id_perfil = @perfil AND r.id_organizacion = @org_oma AND r.anio = 2023
                      AND r.id_reconocimiento <> @rec_odisea
                    ORDER BY r.id_reconocimiento DESC LIMIT 1);
INSERT INTO reconocimiento_traduccion (id_reconocimiento, id_idioma, nombre, descripcion, resultado)
VALUES (@rec_cordoba, @es, 'Olimpiada Cordobesa de Matemática 2023',
        'Participación en el primer nivel de la competencia provincial, realizada en La Falda, Córdoba.',
        'Participante · primer nivel')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion), resultado = VALUES(resultado);
INSERT IGNORE INTO reconocimiento_area (id_reconocimiento, id_area) VALUES (@rec_cordoba, @area_mat);

INSERT INTO organizaciones (nombre, sitio_web, ubicacion)
SELECT 'Cambridge English', NULL, 'Cambridge, Reino Unido'
WHERE NOT EXISTS (SELECT 1 FROM organizaciones WHERE nombre = 'Cambridge English');
SET @org_cambridge = (SELECT id_organizacion FROM organizaciones WHERE nombre = 'Cambridge English' ORDER BY id_organizacion LIMIT 1);
INSERT INTO capacitaciones (id_perfil, id_organizacion, tipo, estado, anio_inicio, anio_fin, horas, certificado_url, orden, visible)
SELECT @perfil, @org_cambridge, 'certificacion', 'finalizada', 2026, 2026, NULL, '/static/docs/certificado_ingles_b2.pdf', 1, TRUE
WHERE NOT EXISTS (SELECT 1 FROM capacitaciones c JOIN capacitacion_traduccion tr ON tr.id_capacitacion = c.id_capacitacion
                  WHERE c.id_perfil = @perfil AND tr.id_idioma = @es AND tr.nombre = 'Cambridge B2 First (Grade B)');
SET @cap_b2 = (SELECT c.id_capacitacion FROM capacitaciones c
               WHERE c.id_perfil = @perfil AND c.id_organizacion = @org_cambridge
               ORDER BY c.id_capacitacion DESC LIMIT 1);
INSERT INTO capacitacion_traduccion (id_capacitacion, id_idioma, nombre, descripcion)
VALUES (@cap_b2, @es, 'Cambridge B2 First (Grade B)',
        'Examen rendido el 14 de noviembre de 2026. Resultado: Pass at Grade B, puntaje global 174 y nivel MCER B2.')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

INSERT INTO organizaciones (nombre, sitio_web, ubicacion)
SELECT 'Junior Achievement Córdoba', NULL, 'Córdoba, Argentina'
WHERE NOT EXISTS (SELECT 1 FROM organizaciones WHERE nombre = 'Junior Achievement Córdoba');
SET @org_ja = (SELECT id_organizacion FROM organizaciones WHERE nombre = 'Junior Achievement Córdoba' ORDER BY id_organizacion LIMIT 1);
INSERT INTO capacitaciones (id_perfil, id_organizacion, tipo, estado, anio_inicio, anio_fin, horas, certificado_url, orden, visible)
SELECT @perfil, @org_ja, 'curso', 'finalizada', NULL, NULL, 8, '/static/docs/certificado_junior_achievement_desafio_innovacion.jpeg', 2, TRUE
WHERE NOT EXISTS (SELECT 1 FROM capacitaciones c JOIN capacitacion_traduccion tr ON tr.id_capacitacion = c.id_capacitacion
                  WHERE c.id_perfil = @perfil AND tr.id_idioma = @es AND tr.nombre = 'Desafío de innovación');
SET @cap_ja = (SELECT c.id_capacitacion FROM capacitaciones c
               WHERE c.id_perfil = @perfil AND c.id_organizacion = @org_ja
               ORDER BY c.id_capacitacion DESC LIMIT 1);
INSERT INTO capacitacion_traduccion (id_capacitacion, id_idioma, nombre, descripcion)
VALUES (@cap_ja, @es, 'Desafío de innovación',
        'Programa de Renault Group Fundación Argentina y Junior Achievement Córdoba. Certificado de finalización con 8 horas de dedicación.')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

INSERT INTO organizaciones (nombre, sitio_web, ubicacion)
SELECT 'Alianza Pro Evangelización del Niño', NULL, 'Córdoba, Argentina'
WHERE NOT EXISTS (SELECT 1 FROM organizaciones WHERE nombre = 'Alianza Pro Evangelización del Niño');
SET @org_alfa = (SELECT id_organizacion FROM organizaciones WHERE nombre = 'Alianza Pro Evangelización del Niño' ORDER BY id_organizacion LIMIT 1);
INSERT INTO capacitaciones (id_perfil, id_organizacion, tipo, estado, anio_inicio, anio_fin, horas, certificado_url, orden, visible)
SELECT @perfil, @org_alfa, 'curso', 'finalizada', 2026, 2026, 45, '/static/docs/certificado_ensenando_con_exito_ninez_nivel_1.jpeg', 3, TRUE
WHERE NOT EXISTS (SELECT 1 FROM capacitaciones c JOIN capacitacion_traduccion tr ON tr.id_capacitacion = c.id_capacitacion
                  WHERE c.id_perfil = @perfil AND tr.id_idioma = @es AND tr.nombre = 'Enseñando con Éxito a la Niñez – Nivel 1');
SET @cap_ninez = (SELECT c.id_capacitacion FROM capacitaciones c
                  WHERE c.id_perfil = @perfil AND c.id_organizacion = @org_alfa
                  ORDER BY c.id_capacitacion DESC LIMIT 1);
INSERT INTO capacitacion_traduccion (id_capacitacion, id_idioma, nombre, descripcion)
VALUES (@cap_ninez, @es, 'Enseñando con Éxito a la Niñez – Nivel 1',
        'Curso aprobado de 45 horas teórico-prácticas. Certificado fechado el 10 de noviembre de 2026.')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

INSERT INTO habilidades (id_perfil, codigo, orden, visible)
SELECT @perfil, x.codigo, x.orden, TRUE FROM (
    SELECT 'pensamiento_logico_y_analitico' AS codigo, 1 AS orden UNION ALL
    SELECT 'resolucion_de_problemas', 2 UNION ALL
    SELECT 'aprendizaje_autonomo', 3 UNION ALL
    SELECT 'trabajo_en_equipo', 4
) x WHERE NOT EXISTS (SELECT 1 FROM habilidades h WHERE h.id_perfil = @perfil AND h.codigo = x.codigo);
INSERT IGNORE INTO habilidad_area (id_habilidad, id_area)
SELECT h.id_habilidad, CASE WHEN h.codigo = 'resolucion_de_problemas' THEN @area_mat ELSE @area_prog END
FROM habilidades h WHERE h.id_perfil = @perfil;

INSERT INTO conocimientos_tecnicos (id_perfil, codigo, orden, visible)
SELECT @perfil, x.codigo, x.orden, TRUE FROM (
    SELECT 'programacion_orientada_a_objetos' AS codigo, 1 AS orden UNION ALL
    SELECT 'manejo_de_json', 2 UNION ALL
    SELECT 'estructuras_de_datos', 3
) x WHERE NOT EXISTS (SELECT 1 FROM conocimientos_tecnicos c WHERE c.id_perfil = @perfil AND c.codigo = x.codigo);
INSERT IGNORE INTO conocimiento_area (id_conocimiento, id_area)
SELECT c.id_conocimiento, @area_prog FROM conocimientos_tecnicos c WHERE c.id_perfil = @perfil;

COMMIT;
