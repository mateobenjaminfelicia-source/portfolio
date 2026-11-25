-- Ejecutar UNA VEZ sobre la base ya creada con portfolio_mateo_sin_create_database.sql.
-- Agrega lo que el backend necesita: ícono en tecnologías, orden/visible en las secciones
-- que todavía no lo tenían y la tabla de mensajes de contacto.

ALTER TABLE tecnologias ADD COLUMN icono VARCHAR(80) NULL AFTER tipo;

ALTER TABLE perfil_tecnologia
  ADD COLUMN orden SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN visible BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE formaciones
  ADD COLUMN orden SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN visible BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE proyectos
  ADD COLUMN orden SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN visible BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE capacitaciones
  ADD COLUMN orden SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN visible BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE reconocimientos
  ADD COLUMN orden SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN visible BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE objetivos_academicos
  ADD COLUMN orden SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  ADD COLUMN visible BOOLEAN NOT NULL DEFAULT TRUE;

CREATE TABLE mensajes_contacto (
    id_mensaje INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    leido BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB;
