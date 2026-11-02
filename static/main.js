(function () {
  var root = document.documentElement;

  // Light / dark toggle, remembered per browser.
  function currentTheme() {
    var t = root.getAttribute('data-theme');
    if (t === 'light' || t === 'dark') return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  var toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* private mode */ }
    });
  }

  // External links open in a new tab.
  var links = document.querySelectorAll('a[href^="http"]');
  for (var i = 0; i < links.length; i++) {
    if (links[i].hostname && links[i].hostname !== location.hostname) {
      links[i].target = '_blank';
      links[i].rel = 'noopener';
    }
  }

  // Topic filter on the projects page.
  var filters = document.querySelector('[data-filters]');
  if (filters) {
    var cards = document.querySelectorAll('[data-tags]');
    filters.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-tag]');
      if (!btn) return;
      var tag = btn.getAttribute('data-tag');
      var all = filters.querySelectorAll('button[data-tag]');
      for (var j = 0; j < all.length; j++) all[j].setAttribute('aria-pressed', all[j] === btn ? 'true' : 'false');
      for (var k = 0; k < cards.length; k++) {
        var tags = ' ' + cards[k].getAttribute('data-tags') + ' ';
        cards[k].hidden = !(tag === '*' || tags.indexOf(' ' + tag + ' ') !== -1);
      }
    });
  }
})();
