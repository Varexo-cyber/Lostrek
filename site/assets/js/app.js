/* Mobiele Autobanden — menu, bandenmaat, hulpmelder en kleine interacties.
   Bedrijfsgegevens komen uit window.SITE (assets/js/config.js). */
(function () {
  'use strict';
  var SITE = window.SITE || {};

  /* mobiel menu */
  var burger = document.querySelector('.burger');
  var mnav = document.querySelector('.mnav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var open = mnav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { mnav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
    });
  }

  /* blokken laten verschijnen bij scrollen */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && rv.length) {
    var io = new IntersectionObserver(function (items) {
      items.forEach(function (it) { if (it.isIntersecting) { it.target.classList.add('in'); io.unobserve(it.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* vragen: er staat er steeds één open */
  document.querySelectorAll('.faq').forEach(function (faq) {
    faq.addEventListener('toggle', function (e) {
      if (!e.target.open) return;
      faq.querySelectorAll('details[open]').forEach(function (d) { if (d !== e.target) d.open = false; });
    }, true);
  });

  /* bandenmaat in de hero: direct naar WhatsApp */
  document.querySelectorAll('[data-maat]').forEach(function (m) {
    var invoer = m.querySelector('[name=maat]'), dienst = m.querySelector('[name=dienst]'), knop = m.querySelector('[data-maat-wa]');
    function maatBericht() {
      var r = ['Hallo, ik heb een vraag over mijn autobanden.', '', 'Ik zoek: ' + dienst.value];
      var w = invoer.value.trim().toUpperCase();
      r.push('Bandenmaat: ' + (w || 'weet ik niet, ik stuur een foto'));
      if (knop.dataset.plaats) r.push('Plaats: ' + knop.dataset.plaats);
      return r.join('\n');
    }
    function zet() { knop.href = 'https://wa.me/' + SITE.whatsapp + '?text=' + encodeURIComponent(maatBericht()); }
    invoer.addEventListener('input', zet); dienst.addEventListener('change', zet); zet();
    invoer.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); knop.click(); } });
  });

  /* hulpmelder */
  var form = document.querySelector('[data-melder]');
  if (!form) return;
  var uitvoer = document.querySelector('[data-bericht]');
  var waKnop = document.querySelector('[data-verstuur]');
  var status = form.querySelector('[data-locatie-status]');
  var locInput = form.querySelector('[name=locatie]');
  var coords = null;

  /* voorinvullen vanuit de url, bv. ?dienst=Lekke%20band&plaats=Assen&maat=205/55%20R16 */
  var params = new URLSearchParams(location.search);
  ['dienst'].forEach(function (naam) {
    var w = params.get(naam);
    if (!w) return;
    var el = form.querySelector('input[name="' + naam + '"][value="' + CSS.escape(w) + '"]');
    if (el) el.checked = true;
  });
  if (params.get('plaats') && locInput && !locInput.value) locInput.value = params.get('plaats');
  var maatVeld = form.querySelector('[name=maat]');
  if (params.get('maat') && maatVeld) maatVeld.value = params.get('maat');

  function waarde(naam) {
    var el = form.querySelector('input[name="' + naam + '"]:checked');
    return el ? el.value : '';
  }
  function veld(naam) {
    var el = form.querySelector('[name="' + naam + '"]');
    return el ? el.value.trim() : '';
  }

  function bericht() {
    var r = ['Aanvraag via de website van ' + (SITE.naam || 'Mobiele Autobanden'), ''];
    var d = waarde('dienst'), so = waarde('soort'), pl = waarde('plek');
    if (d) r.push('Ik zoek: ' + d);
    var m = veld('maat'); r.push('Bandenmaat: ' + (m ? m.toUpperCase() : 'weet ik niet, ik stuur een foto'));
    var aantal = veld('aantal'); if (aantal) r.push('Aantal banden: ' + aantal);
    if (so) r.push('Soort band: ' + so);
    if (pl) r.push('De auto staat: ' + pl.toLowerCase());
    var k = veld('kenteken'); if (k) r.push('Kenteken: ' + k.toUpperCase());
    var l = veld('locatie'); if (l) r.push('Locatie: ' + l);
    if (coords) r.push('GPS: https://maps.google.com/?q=' + coords.lat.toFixed(6) + ',' + coords.lon.toFixed(6));
    var t = veld('toelichting'); if (t) { r.push(''); r.push(t); }
    var n = veld('naam'), tel = veld('telefoon');
    if (n || tel) { r.push(''); r.push('Naam: ' + (n || '-') + (tel ? ' · tel. ' + tel : '')); }
    return r.join('\n');
  }

  function bijwerken() {
    var tekst = bericht();
    if (uitvoer) uitvoer.textContent = tekst;
    if (waKnop) waKnop.href = 'https://wa.me/' + SITE.whatsapp + '?text=' + encodeURIComponent(tekst);
  }
  form.addEventListener('input', bijwerken);
  form.addEventListener('change', bijwerken);
  bijwerken();

  /* locatie via gps */
  var locKnop = form.querySelector('[data-locatie]');
  if (locKnop) {
    locKnop.addEventListener('click', function () {
      if (!('geolocation' in navigator)) { zetStatus('Uw browser kan geen locatie delen. Typ de plaats of straat.', 'fout'); return; }
      zetStatus('Locatie wordt opgehaald…', '');
      navigator.geolocation.getCurrentPosition(function (pos) {
        coords = { lat: pos.coords.latitude, lon: pos.coords.longitude };
        zetStatus('Locatie gevonden (nauwkeurig tot ongeveer ' + Math.round(pos.coords.accuracy) + ' meter).', 'ok');
        bijwerken();
      }, function (err) {
        zetStatus(err.code === 1 ? 'Locatie delen is geweigerd. Typ de plaats, straat of een herkenningspunt.' : 'Locatie niet gevonden. Typ de plaats of straat.', 'fout');
      }, { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 });
    });
  }
  function zetStatus(t, soort) {
    if (!status) return;
    status.textContent = t;
    status.className = 'locatie__status' + (soort ? ' ' + soort : '');
  }

  /* controle voor versturen: locatie is nodig */
  if (waKnop) {
    waKnop.addEventListener('click', function (e) {
      var wrap = locInput ? locInput.closest('.veld') : null;
      if (!coords && !veld('locatie')) {
        e.preventDefault();
        if (wrap) wrap.classList.add('fout');
        if (locInput) locInput.focus();
        return;
      }
      if (wrap) wrap.classList.remove('fout');
    });
  }
  if (locInput) locInput.addEventListener('input', function () { var w = locInput.closest('.veld'); if (w) w.classList.remove('fout'); });
})();

/* ---------- Soepel inladen: blokken en foto's ---------- */
(function () {
  'use strict';
  var root = document.documentElement;
  if (!root.classList.contains('anim') || !('IntersectionObserver' in window)) return;

  /* rijen met kaarten: de kaarten zelf verschijnen kort na elkaar */
  var RIJEN = '.diensten, .situaties, .stappen, .aanpak, .provkaarten, .faq, .plekken, .feiten__wrap, .kaarten, .regels, .veilig__lijst, .gemlijst, .buren, .kernen';
  var kandidaten = [];
  document.querySelectorAll('main > section:not(.hero):not(.pkop) .wrap > *, main > section.wrap > *, .feiten__wrap > *, .ftr__grid > *').forEach(function (el) {
    if (el.matches(RIJEN)) {
      Array.prototype.forEach.call(el.children, function (k, i) { kandidaten.push([k, Math.min(i, 8) * 0.07]); });
    } else {
      var rij = el.querySelector(RIJEN);
      kandidaten.push([el, 0]);
      if (rij && rij.children.length > 1 && rij.children.length <= 24) {
        Array.prototype.forEach.call(rij.children, function (k, i) { kandidaten.push([k, 0.1 + Math.min(i, 8) * 0.07]); });
      }
    }
  });

  var io = new IntersectionObserver(function (items) {
    items.forEach(function (it) {
      if (it.isIntersecting) { it.target.classList.add('in'); io.unobserve(it.target); }
    });
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });

  var hoogte = window.innerHeight;
  kandidaten.forEach(function (paar) {
    var el = paar[0];
    if (el.classList.contains('sv')) return;
    /* wat al in beeld staat bij het openen, laten we met rust: geen flits */
    if (el.getBoundingClientRect().top < hoogte * 0.92) return;
    el.classList.add('sv');
    if (paar[1]) el.style.setProperty('--sv-vertraging', paar[1] + 's');
    io.observe(el);
  });

  /* foto's die nog laden, faden in zodra ze er zijn */
  document.querySelectorAll('main img').forEach(function (img) {
    if (img.complete && img.naturalWidth) return;
    img.classList.add('laadt');
    var klaar = function () { img.classList.add('geladen'); img.classList.remove('laadt'); };
    img.addEventListener('load', klaar, { once: true });
    img.addEventListener('error', klaar, { once: true });
  });
})();
