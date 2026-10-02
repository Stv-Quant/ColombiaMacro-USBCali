// ColombiaMacro: dibuja los graficos y aplica el horizonte temporal en el navegador.
(function () {
  var CONFIG = { displayModeBar: false, responsive: true, scrollZoom: false };

  // ---------------------------------------------------------------- tema oscuro / claro para los graficos
  // Los graficos se definen con la paleta clara; en tema oscuro cada color conocido se cambia por su par.
  // El fondo de todos los graficos es transparente: se ve el vidrio de la tarjeta.
  // [color de origen (Python), tema claro "Andes", tema oscuro "Banco central"]
  var ROLES = [
    ['#0b0b0b', '#14161a', '#eef0f3'], ['#52514e', '#3d424a', '#b9c0cc'], ['#7a7974', '#62676f', '#8a93a3'], ['#a3a19b', '#9a9da3', '#6f7d92'],
    ['#6b6a66', '#55595f', '#9aa7ba'], ['#dcdad4', 'rgba(20,22,26,0.18)', 'rgba(207,179,122,0.28)'], ['#eeede8', 'rgba(20,22,26,0.07)', 'rgba(238,240,243,0.07)'],
    ['#b9b7b0', 'rgba(20,22,26,0.32)', 'rgba(238,240,243,0.32)'], ['#c9c7c0', 'rgba(20,22,26,0.24)', 'rgba(238,240,243,0.24)'],
    ['#fff', '#f3f0e8', '#0c1527'], ['#ffffff', '#faf8f3', '#0d1830'], ['#f7f6f2', '#efebe1', '#17233a'],
    ['#f3c9b3', '#e8c3ad', '#6e3a22'], ['#bfd7f3', '#c3d3e3', '#1d3f6b'], ['#9ec5f0', '#9db8d3', '#3a5f8f'], ['#5b9be3', '#4d7aa6', '#6f9ccf'],
    ['#2a78d6', '#2a64ad', '#5b8fd8'], ['#eb6834', '#c44a26', '#d9653f'], ['#1baf7a', '#108063', '#2c9f78'], ['#eda100', '#998000', '#a3951f'],
    ['#4a3aa7', '#7a4fb0', '#9b7bdb'], ['#1f4f8f', '#14365a', '#cfe0f5'], ['#1a7f4b', '#0f6a4c', '#7fcaa3'], ['#b7791f', '#8a5a00', '#e2b968'],
    ['#c0392b', '#a3341f', '#f0a48a'], ['#2b6cb0', '#244f7d', '#a8c8ee'], ['#b3261e', '#9b2c1a', '#ee9a86'], ['#b04a17', '#943f14', '#f2b08f'],
    ['#127a55', '#0b5a42', '#9ad8b8'], ['#8a6d3b', '#9a5a22', '#b07040'], ['#d6457a', '#c2457d', '#cc64b4'], ['#0f8fa3', '#1a8fa6', '#2a9cb0'],
    ['rgba(11,11,11,0.07)', 'rgba(20,22,26,0.06)', 'rgba(255,255,255,0.07)'], ['rgba(82,81,78,0.13)', 'rgba(20,22,26,0.1)', 'rgba(183,195,212,0.14)'],
    ['rgba(27,175,122,0.12)', 'rgba(13,90,67,0.10)', 'rgba(143,209,176,0.10)'],
    ['rgba(42,120,214,0.62)', 'rgba(42,100,173,0.55)', 'rgba(91,143,216,0.6)'], ['rgba(235,104,52,0.68)', 'rgba(196,74,38,0.6)', 'rgba(217,101,63,0.62)']
  ];
  var FUENTE = { light: '"InterTight", "Segoe UI", system-ui, sans-serif', dark: '"Plex", "Segoe UI", system-ui, sans-serif' };
  function nrm(c) { return String(c).replace(/\s+/g, '').toLowerCase(); }
  var ROL = {};
  ROLES.forEach(function (r, i) { r.forEach(function (v) { if (!(nrm(v) in ROL)) ROL[nrm(v)] = i; }); });
  function tema() { return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }
  function esColor(v) { return typeof v === 'string' && (v.charAt(0) === '#' || v.slice(0, 3) === 'rgb'); }
  function cambiar(v, col) { var i = ROL[nrm(v)]; return i === undefined ? v : ROLES[i][col]; }
  function convertir(o, col, prof) {
    if (!o || typeof o !== 'object' || prof > 9 || ArrayBuffer.isView(o)) return o;
    if (Array.isArray(o)) {
      if (o.length > 40 && !esColor(o[0]) && !(o[0] && typeof o[0] === 'object')) return o;   // series de datos
      for (var i = 0; i < o.length; i++) {
        var v = o[i];
        if (esColor(v)) o[i] = cambiar(v, col); else if (v && typeof v === 'object') convertir(v, col, prof + 1);
      }
      return o;
    }
    for (var k in o) {
      if (!Object.prototype.hasOwnProperty.call(o, k) || k.charAt(0) === '_') continue;
      var w = o[k];
      if (k === 'paper_bgcolor' || k === 'plot_bgcolor') { o[k] = 'rgba(0,0,0,0)'; continue; }
      if (k === 'family' && typeof w === 'string') { o[k] = FUENTE[col === 2 ? 'dark' : 'light']; continue; }
      if (esColor(w)) o[k] = cambiar(w, col); else if (w && typeof w === 'object') convertir(w, col, prof + 1);
    }
    return o;
  }
  function tematizar(obj) { return convertir(obj, tema() === 'dark' ? 2 : 1, 0); }
  if (window.Plotly) {
    ['newPlot', 'react'].forEach(function (fn) {
      var orig = Plotly[fn];
      Plotly[fn] = function (el, data, layout, cfg) {
        layout = layout || {}; layout.paper_bgcolor = 'rgba(0,0,0,0)'; layout.plot_bgcolor = 'rgba(0,0,0,0)';
        tematizar(data); tematizar(layout);
        return orig.call(Plotly, el, data, layout, cfg);
      };
    });
    var origRelayout = Plotly.relayout;
    Plotly.relayout = function (el, upd, val) {
      if (upd && typeof upd === 'object') tematizar(upd);
      return origRelayout.apply(Plotly, arguments);
    };
  }
  function retematizarGraficos() {
    document.querySelectorAll('.js-plotly-plot').forEach(function (el) {
      if (!el.data || !el.layout) return;
      try { Plotly.react(el, el.data, el.layout, CONFIG); } catch (e) { if (window.console) console.error(e); }
    });
  }
  function botonTema() {
    var btn = document.getElementById('theme-btn');
    if (!btn) return;
    function pintar() {
      var t = tema();
      btn.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false');
      btn.title = btn.getAttribute('aria-label') + ' (' + (t === 'dark' ? btn.dataset.oscuro : btn.dataset.claro) + ')';
    }
    btn.addEventListener('click', function () {
      var nuevo = tema() === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nuevo);
      try { localStorage.setItem('cm-tema', nuevo); } catch (e) {}
      pintar(); retematizarGraficos();
    });
    pintar();
  }

  // ---------------------------------------------------------------- barra de lectura, seccion activa y aparicion suave
  function lectura() {
    var bar = document.getElementById('progress-bar');
    var enlaces = Array.prototype.slice.call(document.querySelectorAll('.menu a[href^="#"]'));
    var secciones = enlaces.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
    var pendiente = false;
    function actualizar() {
      pendiente = false;
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ')';
      var activo = -1, lim = window.innerHeight * 0.35;
      secciones.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < lim) activo = i; });
      enlaces.forEach(function (a, i) { a.classList.toggle('activo', i === activo); });
    }
    window.addEventListener('scroll', function () { if (!pendiente) { pendiente = true; requestAnimationFrame(actualizar); } }, { passive: true });
    window.addEventListener('resize', actualizar);
    actualizar();
    if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.card, .answer, .section .chart, .curve-app, .notes, .table-wrap').forEach(function (el, i) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight) return;           // lo que ya se ve no se anima
      el.classList.add('rv'); io.observe(el);
    });
  }
  var plots = [];

  function toDate(v) { return new Date(v).getTime(); }

  function extentX(fig) {
    var lo = Infinity, hi = -Infinity;
    fig.data.forEach(function (tr) {
      Array.prototype.forEach.call(tr.x || [], function (x) { if (x === null || x === undefined || x === '') return; var t = toDate(x); if (isNaN(t)) return; if (t < lo) lo = t; if (t > hi) hi = t; });
    });
    return [lo, hi];
  }

  // Rango vertical de un eje (y o y2) con los datos visibles entre x0 y x1.
  function yRange(fig, x0, x1, eje) {
    var lo = Infinity, hi = -Infinity, bars = false;
    fig.data.forEach(function (tr) {
      if ((tr.yaxis || 'y') !== eje) return;
      if (tr.type === 'bar') bars = true;
      var xs = tr.x || [], ys = tr.y || [];
      for (var i = 0; i < xs.length; i++) {
        var t = toDate(xs[i]), y = ys[i];
        if (xs[i] === null || isNaN(t) || y === null || y === undefined || isNaN(y) || t < x0 || t > x1) continue;
        if (y < lo) lo = y; if (y > hi) hi = y;
      }
    });
    (fig.layout.shapes || []).forEach(function (s) {
      if ((s.yref || 'y') === eje) {
        [s.y0, s.y1].forEach(function (v) { if (typeof v === 'number') { if (v < lo) lo = v; if (v > hi) hi = v; } });
      }
    });
    if (bars || eje === 'y2') { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
    if (!isFinite(lo)) return null;
    var pad = (hi - lo) * 0.08 || 1;
    return [lo - pad, hi + pad];
  }

  // Graficos base 100: cada serie se re-basa a 100 en el primer dato visible del horizonte.
  function rebase(p, x0) {
    var ys = p.orig.map(function (o) {
      if (!o) return null;
      var base = null;
      for (var i = 0; i < o.x.length; i++) {
        if (toDate(o.x[i]) >= x0 && o.y[i] !== null && !isNaN(o.y[i])) { base = o.y[i]; break; }
      }
      return base ? o.y.map(function (v) { return v === null ? null : 100 * v / base; }) : o.y;
    });
    var idx = [], upd = [];
    ys.forEach(function (y, k) { if (p.orig[k]) { idx.push(k); upd.push(y); } });
    if (idx.length) Plotly.restyle(p.el, { y: upd }, idx);
  }

  function applyHorizon(years) {
    plots.forEach(function (p) {
      if (p.notime) return;
      var ext = p.ext, x1 = ext[1] + 25 * 864e5, x0;
      if (years === 0) { x0 = ext[0] - 25 * 864e5; }
      else { var d = new Date(ext[1]); d.setFullYear(d.getFullYear() - years); x0 = d.getTime(); }
      x0 = Math.max(x0, ext[0] - 25 * 864e5);   // no dejar espacio vacio antes del primer dato
      if (p.orig) rebase(p, x0);
      var upd = { 'xaxis.range': [new Date(x0).toISOString().slice(0, 10), new Date(x1).toISOString().slice(0, 10)] };
      var yr = p.noy ? null : yRange(p.fig, x0, x1, 'y'); if (yr) upd['yaxis.range'] = yr;
      if (p.fig.layout.yaxis2) { var y2 = yRange(p.fig, x0, x1, 'y2'); if (y2) upd['yaxis2.range'] = y2; }
      Plotly.relayout(p.el, upd);
    });
  }

  // ---------------------------------------------------------------- curva TES
  var PALETA = ['#eb6834', '#1baf7a', '#4a3aa7', '#eda100', '#0f8fa3', '#8a6d3b', '#d6457a', '#6b6a66'];   // orden categorico fijo (azul = hoy)
  var TXT = {
    es: { plazos: ['1 año', '5 años', '10 años'], pend: 'Pendiente 10a − 1a', vs: 'vs. hace 1 año', cierre: 'Cierre', fijada: 'fijada (clic en la historia para soltar)',
          meses: ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'], normal: 'normal', plana: 'plana', invertida: 'invertida' },
    en: { plazos: ['1 year', '5 years', '10 years'], pend: 'Slope 10y − 1y', vs: 'vs. 1 year ago', cierre: 'Year-end', fijada: 'pinned (click the history to release)',
          meses: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], normal: 'normal', plana: 'flat', invertida: 'inverted' }
  };

  function curvaTES() {
    var app = document.getElementById('curva-app');
    if (!app) return;
    var lang = app.dataset.lang === 'en' ? 'en' : 'es', X = TXT[lang];
    var scr = document.querySelector('script[src*="assets/app.js"]');
    var src = scr.src.replace(/app\.js(\?.*)?$/, 'curva_tes.json$1');
    function fmt(v, dec, signo) {
      if (v === null || v === undefined || isNaN(v)) return '—';
      var s = Math.abs(v).toFixed(dec);
      if (lang === 'es') s = s.replace('.', ',');
      return (v < 0 ? '−' : (signo ? '+' : '')) + s;
    }
    function fechaTxt(iso) { var p = iso.split('-'); return parseInt(p[2], 10) + ' ' + X.meses[parseInt(p[1], 10) - 1] + ' ' + p[0]; }

    fetch(src).then(function (r) { return r.json(); }).then(function (D) {
      var n = D.f.length, tipo = 'pesos', idx = n - 1, fijada = false;
      var t = D.f.map(function (f) { return Date.parse(f); });
      var cierres = {};                      // ano -> indice del ultimo dia habil
      D.f.forEach(function (f, i) { cierres[f.slice(0, 4)] = i; });
      var anos = Object.keys(cierres).sort();
      var ultimoAno = D.f[n - 1].slice(0, 4);
      anos = anos.filter(function (a) { return a !== ultimoAno; });
      var elegidos = anos.slice(-2);

      var slider = document.getElementById('curva-slider');
      slider.max = n - 1; slider.value = idx;
      var gC = document.getElementById('g-curva-tes'), gH = document.getElementById('g-curva-hist');

      function cols() { return ['tes_' + tipo + '_1y', 'tes_' + tipo + '_5y', 'tes_' + tipo + '_10y']; }
      function curva(i) { return cols().map(function (c) { return D[c][i]; }); }
      function haceUnAno(i) {                // indice mas cercano 365 dias antes
        var obj = t[i] - 365 * 864e5, lo = 0, hi = i;
        while (lo < hi) { var m = (lo + hi) >> 1; if (t[m] < obj) lo = m + 1; else hi = m; }
        return Math.abs(t[lo] - obj) < 20 * 864e5 ? lo : null;
      }
      function indicePorFecha(ms) {
        var lo = 0, hi = n - 1;
        while (lo < hi) { var m = (lo + hi + 1) >> 1; if (t[m] <= ms) lo = m; else hi = m - 1; }
        return lo;
      }
      function rangoY() {
        var lo = Infinity, hi = -Infinity;
        cols().forEach(function (c) { D[c].forEach(function (v) { if (v !== null) { if (v < lo) lo = v; if (v > hi) hi = v; } }); });
        var pad = (hi - lo) * 0.06; return [Math.floor(lo - pad), Math.ceil(hi + pad)];
      }
      var LAYOUT = {
        height: 340, margin: { l: 6, r: 10, t: 6, b: 6 }, paper_bgcolor: '#fff', plot_bgcolor: '#fff',
        font: { family: "Inter, 'Segoe UI', system-ui, sans-serif", size: 12.5, color: '#52514e' },
        separators: lang === 'es' ? ',.' : '.,', showlegend: true,
        legend: { orientation: 'h', x: 0, y: 1, yanchor: 'bottom', font: { size: 12 } },
        hoverlabel: { bgcolor: '#fff', bordercolor: '#dcdad4', font: { size: 12.5, color: '#0b0b0b' } }
      };
      function layoutCurva() {
        return Object.assign({}, LAYOUT, {
          hovermode: 'closest',
          xaxis: { tickvals: [1, 5, 10], ticktext: X.plazos, range: [0.5, 10.5], showgrid: false, showline: true,
                   linecolor: '#dcdad4', fixedrange: true, automargin: true, tickfont: { color: '#7a7974' } },
          yaxis: { range: rangoY(), ticksuffix: '%', gridcolor: '#eeede8', zeroline: false, fixedrange: true, automargin: true,
                   tickfont: { color: '#7a7974' } }
        });
      }
      function dibujarCurva() {
        var trazos = [];
        elegidos.forEach(function (a, k) {
          var i = cierres[a];
          trazos.push({ x: [1, 5, 10], y: curva(i), name: X.cierre + ' ' + a, mode: 'lines+markers',
                        line: { color: PALETA[anos.indexOf(a) % PALETA.length], width: 1.6 }, marker: { size: 6 },
                        hovertemplate: '%{y:.2f}%<extra>' + X.cierre + ' ' + a + '</extra>' });
        });
        var y = curva(idx), prev = haceUnAno(idx), yp = prev === null ? [null, null, null] : curva(prev);
        var cd = y.map(function (v, k) { return yp[k] === null || v === null ? '' : fmt(v - yp[k], 2, true) + ' pp ' + X.vs; });
        trazos.push({ x: [1, 5, 10], y: y, name: fechaTxt(D.f[idx]), mode: 'lines+markers+text',
                      text: y.map(function (v) { return fmt(v, 2) + '%'; }), textposition: 'top center', cliponaxis: false,
                      textfont: { size: 12.5, color: '#0b0b0b' }, customdata: cd,
                      line: { color: '#2a78d6', width: 3.4 }, marker: { size: 10, color: '#2a78d6', line: { color: '#fff', width: 2 } },
                      hovertemplate: '%{y:.2f}%  <span style="color:#7a7974">%{customdata}</span><extra>' + fechaTxt(D.f[idx]) + '</extra>' });
        Plotly.react(gC, trazos, layoutCurva(), { displayModeBar: false, responsive: true });
      }
      function dibujarHistoria() {
        var colores = ['#9ec5f0', '#5b9be3', '#1f4f8f'];
        var trazos = cols().map(function (c, k) {
          return { x: D.f, y: D[c], name: X.plazos[k], mode: 'lines', line: { color: colores[k], width: k === 2 ? 2 : 1.4 },
                   hovertemplate: '%{y:.2f}%' };
        });
        var lay = Object.assign({}, LAYOUT, {
          hovermode: 'x unified',
          xaxis: { type: 'date', showgrid: false, showline: true, linecolor: '#dcdad4', fixedrange: true, automargin: true, hoverformat: '%d/%m/%Y',
                   tickfont: { color: '#7a7974' } },
          yaxis: { range: rangoY(), ticksuffix: '%', gridcolor: '#eeede8', zeroline: false, fixedrange: true, automargin: true,
                   tickfont: { color: '#7a7974' } },
          shapes: [marca()]
        });
        Plotly.react(gH, trazos, lay, { displayModeBar: false, responsive: true });
      }
      function marca() {
        return { type: 'line', xref: 'x', yref: 'paper', x0: D.f[idx], x1: D.f[idx], y0: 0, y1: 1,
                 line: { color: fijada ? '#b3261e' : '#0b0b0b', width: 1.2, dash: fijada ? 'solid' : 'dot' } };
      }
      function stats() {
        var y = curva(idx), prev = haceUnAno(idx), yp = prev === null ? [null, null, null] : curva(prev);
        function bloque(nombre, v, vp) {
          var ch = (v === null || vp === null) ? null : v - vp;
          var cl = ch === null ? '' : (ch > 0.005 ? 'up' : (ch < -0.005 ? 'down' : 'flat'));
          var fl = ch === null ? '' : (ch > 0.005 ? '▲ ' : (ch < -0.005 ? '▼ ' : '= '));
          return '<div class="stat"><span class="stat-n">' + nombre + '</span><span class="stat-v">' + fmt(v, 2, false) + (nombre === X.pend ? ' pp' : '%') +
                 '</span><span class="stat-f">' + fechaTxt(D.f[idx]) + '</span><span class="stat-c">' +
                 (ch === null ? '' : '<span class="chg ' + cl + '">' + fl + fmt(ch, 2, true) + ' pp</span> <small>' + X.vs + '</small>') + '</span></div>';
        }
        var p = (y[2] === null || y[0] === null) ? null : y[2] - y[0];
        var pp = (yp[2] === null || yp[0] === null) ? null : yp[2] - yp[0];
        var forma = p === null ? '' : (p > 0.3 ? X.normal : (p < 0 ? X.invertida : X.plana));
        document.getElementById('curva-stats').innerHTML =
          bloque('TES ' + X.plazos[0], y[0], yp[0]) + bloque('TES ' + X.plazos[1], y[1], yp[1]) +
          bloque('TES ' + X.plazos[2], y[2], yp[2]) + bloque(X.pend, p, pp).replace('</span><span class="stat-f">', ' <small>(' + forma + ')</small></span><span class="stat-f">');
        document.getElementById('curva-fecha').textContent = fechaTxt(D.f[idx]) + (fijada ? ' · ' + X.fijada : '');
      }
      function fijar(i, conHistoria) {
        idx = Math.max(0, Math.min(n - 1, i)); slider.value = idx;
        dibujarCurva(); stats();
        if (conHistoria) Plotly.relayout(gH, { shapes: [marca()] });
      }
      function chips() {
        var box = document.getElementById('curva-anos');
        box.innerHTML = '';
        anos.slice().reverse().forEach(function (a) {
          var b = document.createElement('button');
          b.textContent = a; b.className = elegidos.indexOf(a) >= 0 ? 'on' : '';
          b.addEventListener('click', function () {
            var k = elegidos.indexOf(a);
            if (k >= 0) elegidos.splice(k, 1); else elegidos.push(a);
            elegidos.sort(); b.classList.toggle('on'); dibujarCurva();
          });
          box.appendChild(b);
        });
      }

      slider.addEventListener('input', function () { fijada = true; fijar(parseInt(slider.value, 10), true); });
      document.getElementById('curva-hoy').addEventListener('click', function () { fijada = false; fijar(n - 1, true); });
      app.querySelectorAll('.seg button').forEach(function (b) {
        b.addEventListener('click', function () {
          tipo = b.dataset.tipo;
          app.querySelectorAll('.seg button').forEach(function (o) { o.classList.toggle('on', o === b); });
          dibujarHistoria(); fijar(idx, false);
        });
      });
      chips(); dibujarHistoria(); fijar(idx, false);
      gH.on('plotly_hover', function (ev) {
        if (fijada || !ev.points || !ev.points.length) return;
        fijar(indicePorFecha(Date.parse(ev.points[0].x)), true);
      });
      gH.on('plotly_click', function (ev) {
        if (!ev.points || !ev.points.length) return;
        fijada = !fijada; fijar(indicePorFecha(Date.parse(ev.points[0].x)), true);
      });
    }).catch(function () {
      document.getElementById('curva-stats').innerHTML = '<p class="note">No fue posible cargar la curva / Could not load the curve.</p>';
    });
  }

  // ---------------------------------------------------------------- reloj del ciclo
  function relojCiclo() {
    var app = document.getElementById('ciclo-app');
    if (!app) return;
    var D = JSON.parse(document.getElementById('ciclo-datos').textContent);
    var X = JSON.parse(document.getElementById('ciclo-textos').textContent);
    var lang = app.dataset.lang === 'en' ? 'en' : 'es';
    var Q = D.trimestres, F = D.fases, n = Q.length, idx = n - 1, estela = 8;
    var slider = document.getElementById('ciclo-slider');
    var gR = document.getElementById('g-ciclo-reloj'), gH = document.getElementById('g-ciclo-hist');
    slider.max = n - 1; slider.value = idx;
    var FONT = { family: "Inter, 'Segoe UI', system-ui, sans-serif", size: 12.5, color: '#52514e' };
    var CFG = { displayModeBar: false, responsive: true };
    function fmt(v, dec, signo) {
      var s = Math.abs(v).toFixed(dec); if (lang === 'es') s = s.replace('.', ',');
      return (v < 0 ? '−' : (signo ? '+' : '')) + s;
    }
    function tinte(hex, a) {
      var r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
      return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
    }
    function racha(i) { var k = 1; while (i - k >= 0 && Q[i - k].fase === Q[i].fase) k++; return k; }

    function dibujarReloj() {
      var ini = Math.max(0, idx - estela + 1), tr = Q.slice(ini, idx + 1);
      var lx = 2, ly = 1.5;
      tr.forEach(function (p) { lx = Math.max(lx, Math.abs(p.x) * 1.3); ly = Math.max(ly, Math.abs(p.y) * 1.3); });
      var cuad = { expansion: [0, lx, 0, ly], desaceleracion: [0, lx, -ly, 0], contraccion: [-lx, 0, -ly, 0], recuperacion: [-lx, 0, 0, ly] };
      var shapes = Object.keys(cuad).map(function (k) {
        var c = cuad[k];
        return { type: 'rect', xref: 'x', yref: 'y', x0: c[0], x1: c[1], y0: c[2], y1: c[3], line: { width: 0 },
                 fillcolor: tinte(F[k].color, 0.07), layer: 'below' };
      });
      var anot = [];
      var pos = { expansion: [1, 1], desaceleracion: [1, -1], contraccion: [-1, -1], recuperacion: [-1, 1] };
      Object.keys(pos).forEach(function (k) {
        var sx = pos[k][0], sy = pos[k][1];
        anot.push({ x: sx * lx * 0.97, y: sy * ly * 0.95, xanchor: sx > 0 ? 'right' : 'left', yanchor: sy > 0 ? 'top' : 'bottom',
                    showarrow: false, text: '<b>' + F[k].nombre + '</b>', font: { size: 13, color: F[k].color } });
      });
      for (var i = 1; i < tr.length; i++) {
        anot.push({ x: tr[i].x, y: tr[i].y, ax: tr[i - 1].x, ay: tr[i - 1].y, axref: 'x', ayref: 'y', xref: 'x', yref: 'y',
                    showarrow: true, arrowhead: 2, arrowsize: 1.1, arrowwidth: 1.4, standoff: 7, startstandoff: 5,
                    arrowcolor: tinte('#52514e', 0.25 + 0.6 * i / tr.length), text: '' });
      }
      var ult = tr[tr.length - 1];
      anot.push({ x: ult.x, y: ult.y, text: '<b>' + ult.q + '</b>', showarrow: false, yshift: 20, font: { size: 13, color: '#0b0b0b' } });
      var hover = tr.map(function (p) {
        return p.q + ' · ' + F[p.fase].nombre + '<br>' + X.ck_hover + ': ' + fmt(p.x, 1, true) + '%<br>' + X.vs_2t + ': ' + fmt(p.y, 1, true) + ' pp';
      });
      var datos = [{
        x: tr.map(function (p) { return p.x; }), y: tr.map(function (p) { return p.y; }), mode: 'markers',
        marker: { size: tr.map(function (p, i) { return i === tr.length - 1 ? 20 : 9; }),
                  color: tr.map(function (p) { return F[p.fase].color; }),
                  opacity: tr.map(function (p, i) { return 0.35 + 0.65 * (i + 1) / tr.length; }),
                  line: { color: '#fff', width: 2 } },
        text: hover, hovertemplate: '%{text}<extra></extra>', showlegend: false
      }];
      var lay = {
        height: 420, margin: { l: 6, r: 10, t: 6, b: 6 }, paper_bgcolor: '#fff', plot_bgcolor: '#fff', font: FONT,
        hovermode: 'closest', shapes: shapes, annotations: anot, showlegend: false,
        hoverlabel: { bgcolor: '#fff', bordercolor: '#dcdad4', font: { size: 12.5, color: '#0b0b0b' } },
        xaxis: { range: [-lx, lx], zeroline: true, zerolinecolor: '#b9b7b0', zerolinewidth: 1.2, showgrid: false, ticksuffix: '%',
                 fixedrange: true, automargin: true, title: { text: X.ck_eje_x, font: { size: 12 } }, tickfont: { color: '#7a7974' } },
        yaxis: { range: [-ly, ly], zeroline: true, zerolinecolor: '#b9b7b0', zerolinewidth: 1.2, showgrid: false, ticksuffix: ' pp',
                 fixedrange: true, automargin: true, title: { text: X.ck_eje_y, font: { size: 12 } }, tickfont: { color: '#7a7974' } }
      };
      Plotly.react(gR, datos, lay, CFG);
    }

    function marcaHist() {
      var ini = Math.max(0, idx - estela + 1);
      var d0 = new Date(Q[ini].f), d1 = new Date(Q[idx].f);
      d0.setMonth(d0.getMonth() - 2); d0.setDate(1); d1.setDate(d1.getDate() + 10);
      return [{ type: 'rect', xref: 'x', yref: 'paper', x0: d0.toISOString().slice(0, 10), x1: d1.toISOString().slice(0, 10),
                y0: 0, y1: 1, fillcolor: 'rgba(11,11,11,0.07)', line: { width: 0 }, layer: 'below' },
              { type: 'line', xref: 'paper', x0: 0, x1: 1, yref: 'y', y0: 0, y1: 0, line: { color: '#52514e', width: 1 } }];
    }
    function dibujarHist() {
      var datos = [{
        type: 'bar', x: Q.map(function (p) { return p.f; }), y: Q.map(function (p) { return p.x; }),
        marker: { color: Q.map(function (p) { return F[p.fase].color; }), line: { width: 0 } }, showlegend: false,
        customdata: Q.map(function (p) { return [p.q, F[p.fase].nombre, fmt(p.x, 1, true), fmt(p.y, 1, true)]; }),
        hovertemplate: '<b>%{customdata[0]}</b> · %{customdata[1]}<br>' + X.ck_hover + ': %{customdata[2]}%<br>' + X.vs_2t + ': %{customdata[3]} pp<extra></extra>'
      }, {
        type: 'scatter', mode: 'lines', x: Q.map(function (p) { return p.f; }), y: Q.map(function (p) { return p.y; }),
        line: { color: '#0b0b0b', width: 1.2, dash: 'dot' }, name: X.ck_dir, hoverinfo: 'skip'
      }];
      var lay = {
        height: 380, margin: { l: 6, r: 10, t: 6, b: 6 }, paper_bgcolor: '#fff', plot_bgcolor: '#fff', font: FONT,
        hovermode: 'closest', bargap: 0.15, shapes: marcaHist(), showlegend: true,
        legend: { orientation: 'h', x: 0, y: 1, yanchor: 'bottom', font: { size: 12 } },
        separators: lang === 'es' ? ',.' : '.,',
        xaxis: { type: 'date', showgrid: false, showline: true, linecolor: '#dcdad4', fixedrange: true, automargin: true, tickfont: { color: '#7a7974' },
                 title: { text: X.ck_hist_x, font: { size: 12 } } },
        yaxis: { ticksuffix: '%', gridcolor: '#eeede8', zeroline: false, fixedrange: true, automargin: true, tickfont: { color: '#7a7974' },
                 title: { text: X.ck_hist_y, font: { size: 12 } } }
      };
      Plotly.react(gH, datos, lay, CFG);
    }
    function stats() {
      var p = Q[idx], f = F[p.fase];
      function bloque(nombre, valor, detalle) {
        return '<div class="stat"><span class="stat-n">' + nombre + '</span><span class="stat-v">' + valor + '</span><span class="stat-f">' + p.q +
               '</span><span class="stat-c">' + (detalle || '') + '</span></div>';
      }
      var nivel = (p.x >= 0 ? X.ck_encima : X.ck_debajo).replace('{v}', fmt(Math.abs(p.x), 1));
      var dir = (p.y >= 0 ? X.ck_mejora : X.ck_empeora).replace('{v}', fmt(Math.abs(p.y), 1));
      document.getElementById('ciclo-stats').innerHTML =
        '<div class="stat"><span class="stat-n">' + X.ck_fase + '</span><span class="stat-v"><span class="phase-pill ph-' + p.fase + '">' + f.nombre + '</span></span><span class="stat-f">' + p.q + '</span><span class="stat-c">' + f.desc + '</span></div>' +
        bloque(X.ck_brecha, fmt(p.x, 1, true) + '%', nivel) +
        bloque(X.ck_dir, '<span class="chg ' + (p.y >= 0 ? 'up' : 'down') + '">' + (p.y >= 0 ? '▲ ' : '▼ ') + fmt(p.y, 1, true) + ' pp</span>', dir) +
        bloque(X.ck_racha, String(racha(idx)), racha(idx) === 1 ? X.ck_trim1 : X.ck_trim);
      document.getElementById('ciclo-q').textContent = p.q;
    }
    function ir(i) {
      idx = Math.max(0, Math.min(n - 1, i)); slider.value = idx;
      dibujarReloj(); stats(); Plotly.relayout(gH, { shapes: marcaHist() });
    }
    slider.addEventListener('input', function () { ir(parseInt(slider.value, 10)); });
    document.getElementById('ciclo-hoy').addEventListener('click', function () { ir(n - 1); });
    app.querySelectorAll('.seg button').forEach(function (b) {
      b.addEventListener('click', function () {
        estela = parseInt(b.dataset.n, 10);
        app.querySelectorAll('.seg button').forEach(function (o) { o.classList.toggle('on', o === b); });
        ir(idx);
      });
    });
    dibujarHist(); ir(idx);
    function porFecha(ev) {
      if (!ev.points || !ev.points.length) return null;
      var f = String(ev.points[0].x).slice(0, 10);
      for (var i = 0; i < n; i++) if (Q[i].f === f) return i;
      return null;
    }
    gH.on('plotly_click', function (ev) { var i = porFecha(ev); if (i !== null) ir(i); });
    gH.on('plotly_hover', function (ev) { var i = porFecha(ev); if (i !== null && i !== idx) ir(i); });
  }

  // ---------------------------------------------------------------- menu: ocultar al bajar, mostrar al subir
  function cabecera() {
    var top = document.querySelector('.top'), btn = document.getElementById('menu-toggle');
    if (!top) return;
    var ultimo = window.scrollY, movil = function () { return window.matchMedia('(max-width:1100px)').matches; };
    window.addEventListener('scroll', function () {
      var y = window.scrollY, bajando = y > ultimo + 4, subiendo = y < ultimo - 4;
      if (bajando && y > 120) { top.classList.add('oculta'); document.body.classList.add('top-oculta'); document.body.classList.remove('menu-abierto'); if (btn && movil()) btn.classList.remove('abierto'); }
      else if (subiendo || y < 60) { top.classList.remove('oculta'); document.body.classList.remove('top-oculta'); }
      if (bajando || subiendo) ultimo = y;
    }, { passive: true });
    // grupos del menu: clic abre/cierra (en escritorio tambien abren al pasar el cursor)
    var grupos = Array.prototype.slice.call(document.querySelectorAll('.grp'));
    function cerrarGrupos(salvo) {
      grupos.forEach(function (g) { if (g !== salvo) { g.classList.remove('abierto'); g.querySelector('.grp-b').setAttribute('aria-expanded', 'false'); } });
    }
    grupos.forEach(function (g) {
      var b = g.querySelector('.grp-b');
      b.addEventListener('click', function (ev) {
        if (document.body.classList.contains('menu-abierto')) return;   // en el menu movil los grupos van desplegados
        ev.stopPropagation();
        var abre = !g.classList.contains('abierto');
        cerrarGrupos(g); g.classList.toggle('abierto', abre); b.setAttribute('aria-expanded', abre ? 'true' : 'false');
      });
    });
    document.addEventListener('click', function (ev) { if (!ev.target.closest('.grp')) cerrarGrupos(null); });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') cerrarGrupos(null); });
    if (!btn) return;
    var txt = btn.querySelector('.mt-txt');
    function pintar() {
      var visible = document.body.classList.contains('menu-abierto');
      btn.setAttribute('aria-expanded', visible ? 'true' : 'false');
      btn.classList.toggle('abierto', visible);
      if (txt) txt.textContent = visible ? btn.dataset.ocultar : btn.dataset.mostrar;
    }
    btn.addEventListener('click', function () { cerrarGrupos(null); document.body.classList.toggle('menu-abierto'); pintar(); });
    document.querySelectorAll('.menu a').forEach(function (a) {
      a.addEventListener('click', function () { document.body.classList.remove('menu-abierto'); pintar(); });
    });
    window.addEventListener('resize', function () { if (!movil()) document.body.classList.remove('menu-abierto'); pintar(); });
    pintar();
  }

  // ---------------------------------------------------------------- utilidades comunes
  var BASE_LAYOUT = function (lang) {
    return {
      paper_bgcolor: '#fff', plot_bgcolor: '#fff', margin: { l: 6, r: 30, t: 6, b: 6 },
      font: { family: "Inter, 'Segoe UI', system-ui, sans-serif", size: 12.5, color: '#52514e' },
      separators: lang === 'es' ? ',.' : '.,',
      hoverlabel: { bgcolor: '#fff', bordercolor: '#dcdad4', font: { size: 12.5, color: '#0b0b0b' } },
      legend: { orientation: 'h', x: 0, y: 1, yanchor: 'bottom', font: { size: 12 } }
    };
  };
  function numTxt(v, dec, lang, signo) {
    if (v === null || v === undefined || isNaN(v)) return '—';
    var s = Math.abs(v).toFixed(dec); if (lang === 'es') s = s.replace('.', ',');
    return (v < 0 ? '-' : (signo ? '+' : '')) + s;
  }

  // ---------------------------------------------------------------- mapa esquematico de las regiones
  function mapaRegiones() {
    document.querySelectorAll('.tmapa').forEach(function (box) {
      function pintar(m) {
        box.setAttribute('data-m', m);
        box.querySelectorAll('.tm-btn button').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-m') === m); });
        box.querySelectorAll('.tm-c').forEach(function (c) {
          var v = (c.getAttribute('data-' + m) || 'na|—').split('|');
          c.className = 'tm-c tm-b' + v[0];
          c.querySelector('.tm-v').textContent = v[1];
        });
      }
      box.querySelectorAll('.tm-btn button').forEach(function (b) {
        b.addEventListener('click', function () { pintar(b.getAttribute('data-m')); });
      });
      pintar(box.getAttribute('data-m') || 'v19');
    });
  }

  // ---------------------------------------------------------------- sectores: elegir trimestre
  function sectoresSelector() {
    var sel = document.getElementById('sec-q'), el = document.getElementById('g-sec-barras');
    if (!sel || !el) return;
    var D = JSON.parse(document.getElementById('sec-datos').textContent);
    var X = JSON.parse(document.getElementById('sec-textos').textContent);
    var lang = document.documentElement.lang === 'en' ? 'en' : 'es';
    var cap = el.closest('figure').querySelector('figcaption');
    var base = cap.textContent.replace(/\s*\([^)]*\)\s*$/, '');
    function dibujar(k) {
      var q = D[k], filas = q.s.slice().sort(function (a, b) { return a[1] - b[1]; });
      var ys = filas.map(function (r) { return r[0]; });
      var lo = 0, hi = 0;
      filas.forEach(function (r) { [r[1], r[2]].forEach(function (v) { if (v !== null) { lo = Math.min(lo, v); hi = Math.max(hi, v); } }); });
      var trazos = [{
        type: 'bar', orientation: 'h', y: ys, x: filas.map(function (r) { return r[1]; }), showlegend: false,
        marker: { color: filas.map(function (r) { return r[1] >= 0 ? '#2a78d6' : '#eb6834'; }) },
        text: filas.map(function (r) { return numTxt(r[1], 1, lang, true) + '%'; }), textposition: 'outside', cliponaxis: false,
        customdata: filas.map(function (r) { return [numTxt(r[3], 1, lang) + '%', numTxt(r[4], 2, lang, true) + ' pp', r[2] === null ? '—' : numTxt(r[2], 1, lang) + '%']; }),
        hovertemplate: '<b>%{y}</b><br>' + X.sec_crec + ': %{x:.1f}%<br>' + X.sec_hace + ': %{customdata[2]}<br>' + X.sec_peso + ': %{customdata[0]}<br>' + X.sec_aporte + ': %{customdata[1]}<extra></extra>'
      }, {
        type: 'scatter', mode: 'markers', y: ys, x: filas.map(function (r) { return r[2]; }), hoverinfo: 'skip',
        name: X.sec_raya.replace('{q}', q.qa), marker: { symbol: 'line-ns', size: 16, line: { width: 2.5, color: '#0b0b0b' } }
      }];
      var lay = Object.assign(BASE_LAYOUT(lang), {
        height: 440, hovermode: 'closest', bargap: 0.28, showlegend: true,
        xaxis: { ticksuffix: '%', gridcolor: '#eeede8', zeroline: false, fixedrange: true, range: [lo - 2, hi + 3], automargin: true, tickfont: { color: '#7a7974' } },
        yaxis: { fixedrange: true, automargin: true, tickfont: { size: 12, color: '#52514e' } },
        shapes: [{ type: 'line', xref: 'x', x0: 0, x1: 0, yref: 'paper', y0: 0, y1: 1, line: { color: '#52514e', width: 1 } }]
      });
      Plotly.react(el, trazos, lay, { displayModeBar: false, responsive: true });
      cap.textContent = base + ' (' + q.q + ')';
    }
    function elegir(k) { if (k < 0 || k >= D.length) return; sel.value = String(k); dibujar(k); }
    sel.addEventListener('change', function () { elegir(parseInt(sel.value, 10)); });
    sel.addEventListener('input', function () { elegir(parseInt(sel.value, 10)); });
    // clic en una columna del mapa: ver ese trimestre en las barras
    var mapa = document.getElementById('g-sec-mapa');
    if (mapa && mapa.on) mapa.on('plotly_click', function (ev) {
      var pt = ev && ev.points && ev.points[0]; if (!pt) return;
      var t = new Date(pt.x).getTime(), mejor = -1, dist = Infinity;
      D.forEach(function (q, i) { var dd = Math.abs(new Date(q.f).getTime() - t); if (dd < dist) { dist = dd; mejor = i; } });
      if (mejor >= 0 && dist < 60 * 864e5) { elegir(mejor); el.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    });
    document.getElementById('sec-ultimo').addEventListener('click', function () { sel.value = D.length - 1; dibujar(D.length - 1); });
  }


  // ---------------------------------------------------------------- ampliar un grafico sin mover la pagina
  // La figura se saca del flujo (position:fixed) y un hueco del mismo tamano ocupa su lugar;
  // es el mismo elemento, asi que conserva selectores, clics y hover.
  function ampliar() {
    var es = (document.documentElement.lang || 'es') !== 'en';
    var T = es ? { abrir: 'Ampliar gráfico', cerrar: 'Cerrar (Esc)' } : { abrir: 'Expand chart', cerrar: 'Close (Esc)' };
    var activo = null, fondo = document.createElement('div');
    fondo.className = 'exp-fondo';
    fondo.addEventListener('click', function () { cerrar(); });
    document.body.appendChild(fondo);

    function graficos(fig) { return Array.prototype.slice.call(fig.querySelectorAll('.js-plotly-plot')); }
    function alto(el) {
      var n = graficos(activo.fig).length, base = el._altoOrig || 360;
      var max = window.innerHeight * (n > 1 ? 0.42 : 0.68);
      return Math.round(Math.max(base, Math.min(base * 1.8, max)));
    }
    function ajustar() {
      if (!activo) return;
      graficos(activo.fig).forEach(function (el) {
        if (el._altoOrig === undefined) el._altoOrig = (el.layout && el.layout.height) || el.offsetHeight;
        var h = alto(el);
        el.style.height = h + 'px';
        var w = el.clientWidth;
        if (el.layout && (el.layout.height !== h || el.layout.width !== w)) Plotly.relayout(el, { height: h, width: w });
      });
    }
    function fijarScroll(y) {   // sin anclaje de scroll ni desplazamiento suave: la pagina no se mueve
      if (Math.abs(window.scrollY - y) > 1) window.scrollTo({ top: y, left: 0, behavior: 'instant' });
    }
    function abrir(fig, btn) {
      if (activo) cerrar();
      var y = window.scrollY;
      document.documentElement.style.overflowAnchor = 'none';
      var hueco = document.createElement('div');
      hueco.className = 'exp-hueco' + (fig.classList.contains('wide') ? ' wide' : '');
      hueco.style.height = fig.offsetHeight + 'px';
      fig.parentNode.insertBefore(hueco, fig);
      activo = { fig: fig, hueco: hueco, btn: btn, y: y };
      fig.classList.add('expandida');
      document.body.classList.add('con-expandida');
      btn.setAttribute('aria-label', T.cerrar); btn.title = T.cerrar; btn.textContent = '✕';
      graficos(fig).forEach(function (el) {
        el._altoOrig = (el.layout && el.layout.height) || el.offsetHeight;
        el._estiloOrig = el.style.height;
        el.on && el.on('plotly_afterplot', function () {   // un selector redibuja: mantener el tamano ampliado
          if (activo && activo.fig === fig && el.layout && (el.layout.height !== alto(el) || el.layout.width !== el.clientWidth)) setTimeout(ajustar, 0);
        });
      });
      fijarScroll(y);
      requestAnimationFrame(function () { ajustar(); fijarScroll(y); });
      btn.focus({ preventScroll: true });
    }
    function cerrar() {
      if (!activo) return;
      var a = activo; activo = null;
      a.fig.classList.remove('expandida');
      document.body.classList.remove('con-expandida');
      a.btn.setAttribute('aria-label', T.abrir); a.btn.title = T.abrir; a.btn.textContent = '⤢';
      graficos(a.fig).forEach(function (el) {
        el.style.height = el._estiloOrig || '';
        if (el._altoOrig) Plotly.relayout(el, { height: el._altoOrig, width: null }).then(function () { Plotly.Plots.resize(el); });
        delete el._altoOrig; delete el._estiloOrig;
      });
      a.hueco.parentNode && a.hueco.parentNode.removeChild(a.hueco);
      fijarScroll(a.y);
      requestAnimationFrame(function () { fijarScroll(a.y); document.documentElement.style.overflowAnchor = ''; });
    }
    document.querySelectorAll('figure.chart').forEach(function (fig) {
      if (!fig.querySelector('.js-plotly-plot, .plot')) return;
      var btn = document.createElement('button');
      btn.type = 'button'; btn.className = 'exp-btn'; btn.textContent = '⤢';
      btn.setAttribute('aria-label', T.abrir); btn.title = T.abrir;
      btn.addEventListener('click', function (ev) {
        ev.stopPropagation();
        if (activo && activo.fig === fig) cerrar(); else abrir(fig, btn);
      });
      fig.appendChild(btn);
    });
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') cerrar(); });
    window.addEventListener('resize', function () { if (activo) ajustar(); });
  }

  function dialogos() {
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('[data-dialog]');
      if (b) {
        var d = document.getElementById(b.getAttribute('data-dialog'));
        if (d && d.showModal) { d.showModal(); document.body.classList.add('con-dialogo'); var x = d.querySelector('[data-cerrar]'); if (x) x.focus(); }
        return;
      }
      if (e.target.closest && e.target.closest('dialog [data-cerrar]')) { e.target.closest('dialog').close(); return; }
      if (e.target.tagName === 'DIALOG' && e.target.open) {
        var r = e.target.getBoundingClientRect();
        if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) e.target.close();
      }
    });
    document.querySelectorAll('dialog').forEach(function (d) {
      d.addEventListener('close', function () { document.body.classList.remove('con-dialogo'); });
    });
  }

  function seguro(fn) { try { fn(); } catch (e) { if (window.console) console.error(e); } }

  function init() {
    seguro(cabecera);   // primero: el menu funciona aunque falle algun grafico
    seguro(botonTema);
    seguro(lectura);
    document.querySelectorAll('script[data-for]').forEach(function (s) {
      var el = document.getElementById(s.getAttribute('data-for'));
      if (!el) return;
      var fig = JSON.parse(s.textContent);
      try { Plotly.newPlot(el, fig.data, fig.layout, CONFIG); } catch (e) { if (window.console) console.error(e); return; }
      var notime = el.dataset.notime === '1';
      // el.data contiene los arreglos ya decodificados por Plotly (incluye datos binarios).
      var live = { data: el.data, layout: el.layout };
      var p = { el: el, fig: live, ext: notime ? null : extentX(live), notime: notime, noy: el.dataset.noy === '1' };
      if (el.dataset.rebase === '1') {
        // copia de los niveles originales de las series del panel principal
        p.orig = live.data.map(function (tr) {
          return (tr.yaxis || 'y') === 'y' ? { x: Array.prototype.slice.call(tr.x), y: Array.prototype.slice.call(tr.y) } : null;
        });
      }
      plots.push(p);
    });
    var saved = 10;
    try { saved = parseInt(localStorage.getItem('cm-horizonte') || '10', 10); } catch (e) {}
    var buttons = document.querySelectorAll('.horizon button');
    function select(years) {
      buttons.forEach(function (b) { b.classList.toggle('on', parseInt(b.dataset.years, 10) === years); });
      applyHorizon(years);
      try { localStorage.setItem('cm-horizonte', String(years)); } catch (e) {}
    }
    buttons.forEach(function (b) { b.addEventListener('click', function () { select(parseInt(b.dataset.years, 10)); }); });
    select(isNaN(saved) ? 10 : saved);
    seguro(curvaTES);
    seguro(relojCiclo);
    seguro(sectoresSelector);
    seguro(mapaRegiones);
    seguro(ampliar);
    seguro(dialogos);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
