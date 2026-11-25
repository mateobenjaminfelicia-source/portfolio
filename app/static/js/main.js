/* main.js — comportamiento del front (sin librerías) */
(function () {
  var root = document.documentElement;

  /* Tema claro/oscuro: se guarda en localStorage */
  var btn = document.getElementById('theme-toggle');
  function pintarBoton() {
    if (!btn) return;
    var oscuro = root.dataset.theme !== 'light';
    btn.querySelector('i').className = oscuro ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    btn.querySelector('span').textContent = oscuro ? 'Claro' : 'Oscuro';
  }
  if (btn) btn.addEventListener('click', function () {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
    pintarBoton();
  });
  pintarBoton();

  /* Menú hamburguesa (mobile/tablet) */
  var menu = document.getElementById('menu'), burger = document.getElementById('menu-button');
  if (burger) burger.addEventListener('click', function () {
    var abierto = menu.classList.toggle('open');
    burger.querySelector('i').className = abierto ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
  });
  if (menu) menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') menu.classList.remove('open'); });

  /* ANIMACIÓN 1 y 2: al entrar al viewport, .reveal pasa a .visible (CSS hace el fade-in y llena las barras) */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('visible'); obs.unobserve(en.target); } });
    }, { threshold: 0.12 });
    items.forEach(function (el) { obs.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('visible'); }); }

  /* Mostrar/ocultar contraseña en el login */
  var ojo = document.getElementById('toggle-pass');
  if (ojo) ojo.addEventListener('click', function () {
    var input = ojo.parentNode.querySelector('input');
    var ver = input.type === 'password';
    input.type = ver ? 'text' : 'password';
    ojo.querySelector('i').className = ver ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye';
  });

  /* Los mensajes flash desaparecen solos */
  var flash = document.querySelector('.flash-wrap');
  if (flash) setTimeout(function () { flash.remove(); }, 6000);

  /* Año del footer */
  document.querySelectorAll('[data-anio]').forEach(function (s) { s.textContent = new Date().getFullYear(); });
})();
