/* Offshore wind LCOE calculator with a tornado chart.
   Mounted on any element with [data-lcoe]. Labels follow <html lang> (en, vi).
   LCOE = (CAPEX x (1 + r)^delay x CRF + OPEX) / (8.76 MWh per kW-year x capacity factor) */
(function () {
  var mount = document.querySelector('[data-lcoe]');
  if (!mount) return;
  var vi = (document.documentElement.lang || '').indexOf('vi') === 0;
  var locale = vi ? 'vi-VN' : 'en-GB';

  var T = vi ? {
    result: 'Chi phí điện quy dẫn (LCOE)',
    unit: 'USD/MWh',
    reset: 'Đặt lại mặc định',
    chart: 'Mỗi thay đổi kéo chi phí đi bao xa',
    chartNote: 'Mỗi thanh: chi phí khi chỉ một thông số thay đổi trong khoảng ghi bên cạnh. Vạch dọc là mức hiện tại.',
    table: 'Xem dạng bảng',
    colInput: 'Thông số', colLow: 'Chi phí thấp nhất', colHigh: 'Chi phí cao nhất', colSpread: 'Chênh lệch',
    current: 'Hiện tại',
    pp: 'điểm %', yr: 'năm'
  } : {
    result: 'Levelised cost of electricity (LCOE)',
    unit: 'USD/MWh',
    reset: 'Reset to defaults',
    chart: 'How far one change moves the cost',
    chartNote: 'Each bar: the cost when only one input moves across the range shown beside it. The vertical line is the current cost.',
    table: 'Show as table',
    colInput: 'Input', colLow: 'Lowest cost', colHigh: 'Highest cost', colSpread: 'Spread',
    current: 'Current',
    pp: 'pp', yr: 'years'
  };

  var INPUTS = [
    { key: 'capex', min: 1500, max: 5000, step: 50, def: 2850,
      name: vi ? 'Chi phí đầu tư (USD/kW)' : 'Installed cost (USD/kW)',
      span: '±20%', range: function (v) { return [v * 0.8, v * 1.2]; } },
    { key: 'cf', min: 25, max: 60, step: 1, def: 42,
      name: vi ? 'Hệ số công suất (%)' : 'Capacity factor (%)',
      span: '±7 ' + T.pp, range: function (v) { return [Math.max(15, v - 7), Math.min(70, v + 7)]; } },
    { key: 'wacc', min: 3, max: 15, step: 0.5, def: 8,
      name: vi ? 'Chi phí vốn, WACC (%)' : 'Cost of capital, WACC (%)',
      span: '±3 ' + T.pp, range: function (v) { return [Math.max(0.5, v - 3), v + 3]; } },
    { key: 'opex', min: 40, max: 160, step: 5, def: 90,
      name: vi ? 'Chi phí vận hành (USD/kW mỗi năm)' : 'Operating cost (USD/kW per year)',
      span: '±25%', range: function (v) { return [v * 0.75, v * 1.25]; } },
    { key: 'delay', min: 0, max: 5, step: 0.5, def: 0,
      name: vi ? 'Chậm trễ trước khi phát điện (năm)' : 'Delay before first power (years)',
      span: '+2 ' + T.yr, range: function (v) { return [v, v + 2]; } }
  ];
  var LIFE = 25;

  function lcoe(p) {
    var r = p.wacc / 100;
    var crf = r * Math.pow(1 + r, LIFE) / (Math.pow(1 + r, LIFE) - 1);
    var capex = p.capex * Math.pow(1 + r, p.delay);
    return (capex * crf + p.opex) / (8.76 * p.cf / 100);
  }
  function fmt(n, digits) {
    return n.toLocaleString(locale, { maximumFractionDigits: digits || 0, minimumFractionDigits: 0 });
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  // ---- Layout ----
  var state = {};
  INPUTS.forEach(function (i) { state[i.key] = i.def; });

  var result = el('div', 'lcoe-result');
  result.setAttribute('aria-live', 'polite');
  var resultLabel = el('span', 'lcoe-result-label', T.result);
  var resultValue = el('strong', 'lcoe-result-value');
  var resultUnit = el('span', 'lcoe-result-unit', T.unit);
  result.append(resultLabel, resultValue, resultUnit);

  var form = el('div', 'lcoe-inputs');
  var outputs = {}, sliders = {};
  INPUTS.forEach(function (i) {
    var id = 'lcoe-' + i.key;
    var row = el('div', 'lcoe-input');
    var label = el('label', null, i.name);
    label.htmlFor = id;
    var out = el('output', 'lcoe-input-value');
    out.htmlFor = id;
    var slider = el('input');
    slider.type = 'range'; slider.id = id;
    slider.min = i.min; slider.max = i.max; slider.step = i.step; slider.value = i.def;
    slider.addEventListener('input', function () { state[i.key] = parseFloat(slider.value); update(); });
    row.append(label, out, slider);
    form.append(row);
    outputs[i.key] = out; sliders[i.key] = slider;
  });
  var reset = el('button', 'lcoe-reset', T.reset);
  reset.type = 'button';
  reset.addEventListener('click', function () {
    INPUTS.forEach(function (i) { state[i.key] = i.def; sliders[i.key].value = i.def; });
    update();
  });
  form.append(reset);

  var figure = el('figure', 'lcoe-chart');
  var caption = el('figcaption');
  caption.append(el('span', 'lcoe-chart-title', T.chart), el('span', 'lcoe-chart-note', T.chartNote));
  var rowsBox = el('div', 'tn-rows');
  var axis = el('div', 'tn-axis');
  axis.setAttribute('aria-hidden', 'true');
  var tip = el('div', 'tn-tip');
  tip.setAttribute('role', 'tooltip');
  tip.hidden = true;
  figure.append(caption, rowsBox, axis, tip);

  var details = el('details', 'lcoe-table');
  details.append(el('summary', null, T.table));
  var table = el('table');
  details.append(table);

  mount.append(result, form, figure, details);

  function inputLabel(i, v) {
    if (i.key === 'cf' || i.key === 'wacc') return fmt(v, 1) + '%';
    if (i.key === 'delay') return fmt(v, 1) + ' ' + T.yr;
    return fmt(v);
  }

  function update() {
    var base = lcoe(state);
    resultValue.textContent = fmt(base);
    INPUTS.forEach(function (i) { outputs[i.key].textContent = inputLabel(i, state[i.key]); });

    var rows = INPUTS.map(function (i) {
      var rg = i.range(state[i.key]);
      var a = Object.assign({}, state), b = Object.assign({}, state);
      a[i.key] = rg[0]; b[i.key] = rg[1];
      var la = lcoe(a), lb = lcoe(b);
      return { i: i, inLow: rg[0], inHigh: rg[1], costAtLow: la, costAtHigh: lb,
               lo: Math.min(la, lb), hi: Math.max(la, lb) };
    }).sort(function (x, y) { return (y.hi - y.lo) - (x.hi - x.lo); });

    var minV = Math.min(base, Math.min.apply(null, rows.map(function (r) { return r.lo; })));
    var maxV = Math.max(base, Math.max.apply(null, rows.map(function (r) { return r.hi; })));
    var stepT = niceStep((maxV - minV) / 5);
    var d0 = Math.floor(minV / stepT) * stepT, d1 = Math.ceil(maxV / stepT) * stepT;
    function pct(v) { return ((v - d0) / (d1 - d0)) * 100; }

    rowsBox.textContent = '';
    rows.forEach(function (r) {
      var row = el('div', 'tn-row');
      row.tabIndex = 0;
      var name = el('div', 'tn-name');
      name.append(el('span', null, r.i.name.replace(/ \(.*\)$/, '')), el('span', 'tn-span', r.i.span));
      var track = el('div', 'tn-track');
      var bar = el('div', 'tn-bar');
      bar.style.left = pct(r.lo) + '%';
      bar.style.width = Math.max(pct(r.hi) - pct(r.lo), 0.6) + '%';
      var baseLine = el('div', 'tn-base');
      baseLine.style.left = pct(base) + '%';
      var lo = el('span', 'tn-lo', fmt(r.lo));
      lo.style.right = (100 - pct(r.lo)) + '%';
      var hi = el('span', 'tn-hi', fmt(r.hi));
      hi.style.left = pct(r.hi) + '%';
      track.append(bar, baseLine, lo, hi);
      row.append(name, track);
      var text = r.i.name + ': ' + inputLabel(r.i, r.inLow) + ' → ' + fmt(r.costAtLow) + ' · ' +
                 inputLabel(r.i, r.inHigh) + ' → ' + fmt(r.costAtHigh) + ' ' + T.unit;
      row.setAttribute('aria-label', text);
      function show() {
        tip.textContent = text;
        tip.hidden = false;
        var fb = figure.getBoundingClientRect(), rb = track.getBoundingClientRect();
        tip.style.top = (rb.bottom - fb.top + 6) + 'px';
        tip.style.left = Math.max(0, Math.min(rb.left - fb.left + (pct(r.lo) / 100) * rb.width, fb.width - 260)) + 'px';
      }
      function hide() { tip.hidden = true; }
      row.addEventListener('mouseenter', show);
      row.addEventListener('mouseleave', hide);
      row.addEventListener('focus', show);
      row.addEventListener('blur', hide);
      rowsBox.append(row);
    });

    axis.textContent = '';
    var ticks = el('div', 'tn-ticks');
    for (var v = d0; v <= d1 + 1e-9; v += stepT) {
      var t = el('span', null, fmt(v));
      t.style.left = pct(v) + '%';
      ticks.append(t);
    }
    axis.append(el('div', 'tn-axis-unit', T.unit), ticks);
    rowsBox.style.setProperty('--tn-grid', stepT / (d1 - d0) * 100 + '%');

    table.textContent = '';
    var head = el('tr');
    [T.colInput, T.colLow, T.colHigh, T.colSpread].forEach(function (h) { head.append(el('th', null, h)); });
    var thead = el('thead'); thead.append(head);
    var tbody = el('tbody');
    rows.forEach(function (r) {
      var tr = el('tr');
      tr.append(el('td', null, r.i.name + ' (' + r.i.span + ')'), el('td', null, fmt(r.lo)),
                el('td', null, fmt(r.hi)), el('td', null, fmt(r.hi - r.lo)));
      tbody.append(tr);
    });
    var cur = el('tr', 'lcoe-table-current');
    cur.append(el('td', null, T.current), el('td', null, fmt(base)), el('td'), el('td'));
    tbody.append(cur);
    table.append(thead, tbody);
  }

  function niceStep(raw) {
    var p = Math.pow(10, Math.floor(Math.log10(raw)));
    var n = raw / p;
    return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * p;
  }

  update();
})();
