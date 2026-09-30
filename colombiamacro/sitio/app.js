// ColombiaMacro: dibuja los graficos y aplica el horizonte temporal en el navegador.
(function () {
  var CONFIG = { displayModeBar: false, responsive: true, scrollZoom: false };
  var plots = [];

  function toDate(v) { return new Date(v).getTime(); }

  function extentX(fig) {
    var lo = Infinity, hi = -Infinity;
    fig.data.forEach(function (tr) {
      Array.prototype.forEach.call(tr.x || [], function (x) { var t = toDate(x); if (t < lo) lo = t; if (t > hi) hi = t; });
    });
    return [lo, hi];
  }

  function yRange(fig, x0, x1) {
    var lo = Infinity, hi = -Infinity, bars = false;
    fig.data.forEach(function (tr) {
      if (tr.type === 'bar') bars = true;
      var xs = tr.x || [], ys = tr.y || [];
      for (var i = 0; i < xs.length; i++) {
        var t = toDate(xs[i]), y = ys[i];
        if (y === null || y === undefined || t < x0 || t > x1) continue;
        if (y < lo) lo = y; if (y > hi) hi = y;
      }
    });
    (fig.layout.shapes || []).forEach(function (s) {
      if (s.yref === 'y' || s.yref === undefined) {
        [s.y0, s.y1].forEach(function (v) { if (typeof v === 'number') { if (v < lo) lo = v; if (v > hi) hi = v; } });
      }
    });
    if (bars) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
    if (!isFinite(lo)) return null;
    var pad = (hi - lo) * 0.08 || 1;
    return [lo - pad, hi + pad];
  }

  function applyHorizon(years) {
    plots.forEach(function (p) {
      if (p.notime) return;
      var ext = p.ext, x1 = ext[1] + 25 * 864e5, x0;
      if (years === 0) { x0 = ext[0] - 25 * 864e5; }
      else { var d = new Date(ext[1]); d.setFullYear(d.getFullYear() - years); x0 = d.getTime(); }
      var upd = { 'xaxis.range': [new Date(x0).toISOString().slice(0, 10), new Date(x1).toISOString().slice(0, 10)] };
      if (!p.yfijo) { var yr = yRange(p.fig, x0, x1); if (yr) upd['yaxis.range'] = yr; }
      Plotly.relayout(p.el, upd);
    });
  }


  // ---------------------------------------------------------------- curva TES
  var PALETA = ['#eb6834', '#1baf7a', '#eda100', '#4a3aa7', '#d6457a', '#0f8fa3', '#8a6d3b', '#6b6a66'];
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
    var src = document.querySelector('script[src$="app.js"]').src.replace(/app\.js$/, 'curva_tes.json');
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

  function init() {
    document.querySelectorAll('script[data-for]').forEach(function (s) {
      var el = document.getElementById(s.getAttribute('data-for'));
      if (!el) return;
      var fig = JSON.parse(s.textContent);
      Plotly.newPlot(el, fig.data, fig.layout, CONFIG);
      var notime = el.dataset.notime === '1';
      // el.data contiene los arreglos ya decodificados por Plotly (incluye datos binarios).
      var live = { data: el.data, layout: el.layout };
      plots.push({ el: el, fig: live, ext: notime ? null : extentX(live), notime: notime, yfijo: el.dataset.yfijo === '1' });
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
    curvaTES();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
