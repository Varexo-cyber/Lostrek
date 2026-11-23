/* Lostrek — menu, hulpmelder en kleine interacties.
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

  /* hulpmelder */
  var form = document.querySelector('[data-melder]');
  if (!form) return;
  var uitvoer = document.querySelector('[data-bericht]');
  var waKnop = document.querySelector('[data-verstuur]');
  var status = form.querySelector('[data-locatie-status]');
  var locInput = form.querySelector('[name=locatie]');
  var coords = null;

  /* voorinvullen vanuit de url, bv. ?ondergrond=sneeuw&plaats=Assen */
  var params = new URLSearchParams(location.search);
  ['ondergrond', 'voertuig'].forEach(function (naam) {
    var w = params.get(naam);
    if (!w) return;
    var el = form.querySelector('input[name="' + naam + '"][value="' + CSS.escape(w) + '"]');
    if (el) el.checked = true;
  });
  if (params.get('plaats') && locInput && !locInput.value) locInput.value = params.get('plaats');

  function waarde(naam) {
    var el = form.querySelector('input[name="' + naam + '"]:checked');
    return el ? el.value : '';
  }
  function veld(naam) {
    var el = form.querySelector('[name="' + naam + '"]');
    return el ? el.value.trim() : '';
  }

  function bericht() {
    var r = ['Hulp gevraagd via de website van ' + (SITE.naam || 'Lostrek'), ''];
    var o = waarde('ondergrond'), v = waarde('voertuig'), s = waarde('vast'), a = waarde('aandrijving');
    if (o) r.push('Vast in: ' + o);
    if (v) r.push('Voertuig: ' + v);
    if (a) r.push('Aandrijving: ' + a);
    if (s) r.push('Situatie: ' + s);
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
