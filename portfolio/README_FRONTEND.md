# Front end del Portfolio (Fase 3) — Flask + Jinja2

Portado desde el diseño de Figma (React/Tailwind) a HTML + Jinja2 + CSS puro.
Para ver el front YA, sin backend: `pip install flask` → `python demo_app.py` → http://127.0.0.1:5000 (modo edición: `/?admin=1`). Borrá `demo_app.py` cuando tengas el backend real.

## Estructura
- `templates/base.html` → navbar, footer, fuentes (Google Fonts), íconos (Font Awesome), favicon, mensajes flash. Bloques: `title`, `description`, `extra_head`, `content`, `scripts`.
- `templates/index.html`, `login.html`, `admin/form.html` → `{% extends "base.html" %}` + `{% block content %}`.
- `templates/sections/_*.html` → una sección por archivo (`{% include %}` desde index).
- `templates/macros/_macros.html` → macros reutilizables (`encabezado`, `controles`, `timeline_item`, `asset`...).
- `static/css/style.css`, `static/js/main.js`, `static/img/favicon.*`, `static/files/` (poné acá tu `cv.pdf`).

## Qué tiene que darle el backend a los templates
| Variable | Cómo llega | Campos que usa el template |
|---|---|---|
| `perfil` | `@app.context_processor` | id, nombre, apellido, titulo, resumen, sobre_mi, edad, ubicacion, intereses, email, github_url, linkedin_url, foto, cv_url, disponible, frase_footer |
| `es_admin` | `@app.context_processor` (sesión) | bool |
| `estudios` | `index()` | id, titulo, institucion, periodo, descripcion |
| `experiencias` | `index()` | id, puesto, empresa, periodo, descripcion |
| `certificaciones` | `index()` | id, nombre, entidad, anio, url |
| `idiomas` | `index()` | id, nombre, nivel |
| `tecnologias` | `index()` | id, nombre, icono (clases FontAwesome), nivel (ENUM) |
| `proyectos` | `index()` | id, titulo, categoria, anio, descripcion, imagen, url, tecnologias (lista con .nombre) |
| `form_contacto` | `index()` | FlaskForm con nombre, email, asunto, mensaje |
| `form` | `login()` y `admin_form()` | FlaskForm (login: username, password) |

Tip POO: `periodo` y `edad` pueden ser `@property` del modelo (arma "2024 — Actualidad" / calcula la edad).
Filtrá `visible` y ordená por `orden` en la consulta, no en el template.

Endpoints usados con `url_for` (si usás blueprints, anteponé el prefijo):
`index`, `login`, `logout` (POST), `contacto` (POST), `admin_form` (`/admin/<seccion>/nuevo` y `/admin/<seccion>/<int:id>/editar`), `admin_eliminar` (POST `/admin/<seccion>/<int:id>/eliminar`).
`<seccion>` = perfil, estudios, experiencias, certificaciones, idiomas, tecnologias, proyectos.

## Checklist de la consigna
- Jinja2: `base.html` + extends/block/include/macros; `{% for %}` (con `{% else %}`) y `{% if %}` en todas las secciones.
- Iframe: Google Maps en `sections/_contacto.html`.
- Íconos: Font Awesome (`base.html`). Fuentes: Google Fonts Inter + Space Grotesk (`base.html`). Favicon: `static/img/favicon.svg|png`.
- Responsive: `static/css/style.css`, media queries al final → escritorio (>1100px), tablet (≤1100px y ≤820px), mobile (≤560px). Aplica a toda la página principal.
- Login con Flask-WTF: `login.html` (`form.hidden_tag()` = token CSRF); botones de edición solo con `es_admin`.
- CV descargable: botón "Descargar CV" (`perfil.cv_url`, ej. `files/cv.pdf`).

## Animaciones (indicar dónde están)
1. Fade-in + subida al hacer scroll: clase `.reveal` en `style.css` + `IntersectionObserver` en `main.js` (todas las secciones).
2. Barras de nivel que se llenan: `.skill-track i` en `style.css` (sección Tecnologías).
3. Zoom de la imagen al pasar el mouse: `.project-card:hover .project-image img` (Proyectos).
4. Tarjetas que se elevan en hover: `.info-card:hover, .tech-card:hover...`.
5. Subrayado animado en los links del navbar: `.navbar nav a::after`.
(Todas están comentadas como "ANIMACIÓN N" en `style.css`.)
