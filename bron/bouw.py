"""Mobiele Autobanden — bouwt de complete website in ../site.

    python3 bron/bouw.py

Bedrijfsgegevens staan in bron/site.json, de gemeenten in bron/data/gemeenten.json.
Na het bouwen staat alles wat online moet in de map site/.
"""
import html
import json
import pathlib
import re
import time
from urllib.parse import quote

BRON = pathlib.Path(__file__).resolve().parent
SITE = BRON.parent / 'site'
C = json.loads((BRON / 'site.json').read_text(encoding='utf-8'))
GEMEENTEN = json.loads((BRON / 'data' / 'gemeenten.json').read_text(encoding='utf-8'))
DOMEIN = C['domein'].rstrip('/')
VERSIE = time.strftime('%Y%m%d%H%M')
VANDAAG = time.strftime('%Y-%m-%d')

E = lambda s: html.escape(str(s), quote=True)
TEL = C['telefoon']
TELNR = TEL.replace(' ', '&nbsp;')
WA = C['whatsapp']


def wa(tekst=''):
    from urllib.parse import quote
    return f'https://wa.me/{WA}' + (f'?text={quote(tekst)}' if tekst else '')


# ---------------------------------------------------------------- iconen
ICONEN = {
    'tel': '<path d="M5 3.5h3.2l1.6 4.2-2.1 1.5a11 11 0 0 0 7.1 7.1l1.5-2.1 4.2 1.6V19a1.8 1.8 0 0 1-1.9 1.8A16.2 16.2 0 0 1 3.2 5.4 1.8 1.8 0 0 1 5 3.5z"/>',
    'wa': '<path d="M4 20.5l1.2-4.1A8.4 8.4 0 1 1 8.4 19.5z"/><path d="M9.2 8.6c.2-.6.5-.7.9-.7h.5l.9 2-.7.9c.6 1.2 1.5 2.1 2.7 2.7l.9-.7 2 .9v.5c0 .4-.2.8-.7 1-1.8.7-6.9-3.6-6.5-6.6z"/>',
    'pijl': '<path d="M4 12h15M13 6l6 6-6 6"/>',
    'vink': '<path d="M4.5 12.5l4.5 4.5 10.5-11"/>',
    'kruis': '<path d="M6 6l12 12M18 6L6 18"/>',
    'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0C18.5 15.4 12 21 12 21z"/><circle cx="12" cy="10" r="2.4"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'auto': '<path d="M3.5 15.5v-3l2-5h13l2 5v3"/><path d="M3.5 15.5h17v2h-17z"/><circle cx="7.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/>',
    'band': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.6"/><path d="M12 3v3.4M12 17.6V21M3 12h3.4M17.6 12H21"/>',
}


def icon(naam, extra=''):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"{extra}>{ICONEN[naam]}</svg>')


LOGO_MERK = ('<svg class="logo__merk" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="6" fill="#E8590C"/>'
             '<rect x="12" y="5" width="16" height="30" rx="7" fill="#fff"/>'
             '<path d="M12 13.5l8-4.5 8 4.5M12 20.5l8-4.5 8 4.5M12 27.5l8-4.5 8 4.5" fill="none" stroke="#E8590C" stroke-width="2.6"/></svg>')


def logo(r):
    return (f'<a class="logo" href="{r}./" aria-label="{E(C["naam"])}, naar de homepage">{LOGO_MERK}'
            f'<div><b>{E(C["naam"]).upper()}</b><span>{E(C["ondertitel"])}</span></div></a>')


# ---------------------------------------------------------------- data
PROVINCIES = {}
for g in GEMEENTEN:
    PROVINCIES.setdefault(g['prov_slug'], {'naam': g['prov'], 'slug': g['prov_slug'], 'gemeenten': []})['gemeenten'].append(g)
PROVINCIES = dict(sorted(PROVINCIES.items()))
PER_SLUG = {g['slug']: g for g in GEMEENTEN}
GEMPAD = 'mobiele-bandenservice'

# beeld: (bestand, alt, maker, licentie, licentie-url, bron-url, titel)
BEELD = {
    'wiel-wisselen': ('Wiel van een personenauto wordt gewisseld met een krik', 'Santeri Viinamäki', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/', 'https://commons.wikimedia.org/wiki/File:Changing_car_tire_20170513_01.jpg', 'Changing car tire 20170513 01'),
    'wiel-krik': ('Auto op de krik met het wiel eraf', 'Santeri Viinamäki', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/', 'https://commons.wikimedia.org/wiki/File:Changing_car_tire_20170513_02.jpg', 'Changing car tire 20170513 02'),
    'lekke-band': ('Platte band aan een personenauto', 'Flyerwe', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/', 'https://commons.wikimedia.org/wiki/File:Deflated_car_tire.jpg', 'Deflated car tire'),
    'winterband': ('Winterband met de bandenmaat 195/55 R16 op de zijkant', 'GT1976', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/', 'https://commons.wikimedia.org/wiki/File:2017-10-19_(355)_Pirelli_Cinturato_Winter_195-55_R_16_91_H_tire_at_Bahnhof_Tulln_an_der_Donau,_Austria.jpg', 'Pirelli Cinturato Winter 195/55 R16'),
    'winter-auto': ('Personenauto met winterbanden op een besneeuwde weg', 'Michael, Calgary', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/', 'https://commons.wikimedia.org/wiki/File:Winter_Tires_FTW_(6556993959).jpg', 'Winter Tires FTW'),
    'balanceren': ('Band op een balanceermachine', 'ProjectManhattan', 'CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0/', 'https://commons.wikimedia.org/wiki/File:Wheel_balancing.jpg', 'Wheel balancing'),
    'thuiskomer': ('Auto met een thuiskomer als reservewiel', 'paul_houle', 'CC BY-SA 2.0', 'https://creativecommons.org/licenses/by-sa/2.0/', 'https://commons.wikimedia.org/wiki/File:Spare_Tire_On_Car_(3580447792).jpg', 'Spare Tire On Car'),
}

MATEN = {}


def maat(naam):
    if naam not in MATEN:
        p = SITE / 'assets' / 'img' / f'{naam}.webp'
        data = p.read_bytes()
        # VP8X / VP8 / VP8L kop uitlezen
        if data[12:16] == b'VP8X':
            w = int.from_bytes(data[24:27], 'little') + 1; h = int.from_bytes(data[27:30], 'little') + 1
        elif data[12:16] == b'VP8 ':
            w = int.from_bytes(data[26:28], 'little') & 0x3fff; h = int.from_bytes(data[28:30], 'little') & 0x3fff
        else:
            b = int.from_bytes(data[21:25], 'little'); w = (b & 0x3fff) + 1; h = ((b >> 14) & 0x3fff) + 1
        MATEN[naam] = (w, h)
    return MATEN[naam]


def img(r, naam, sizes='(max-width: 960px) 100vw, 50vw', lui=True, alt=None, extra=''):
    w, h = maat(naam)
    alt = BEELD[naam][0] if alt is None else alt
    laad = ' loading="lazy" decoding="async"' if lui else ' fetchpriority="high" decoding="async"'
    midden = f'{r}assets/img/{naam}-1024.webp 1024w, ' if (SITE / 'assets' / 'img' / f'{naam}-1024.webp').exists() else ''
    return (f'<img src="{r}assets/img/{naam}.webp" srcset="{r}assets/img/{naam}-640.webp 640w, {midden}{r}assets/img/{naam}.webp {w}w" '
            f'sizes="{sizes}" alt="{E(alt)}" width="{w}" height="{h}"{laad}{extra}>')



# ---------------------------------------------------------------- vaste delen
NAV = [('', 'Home', 'home'), ('diensten.html', 'Diensten', 'diensten'), ('hulp-aanvragen.html', 'Hulp aanvragen', 'hulp'),
       ('werkgebied/', 'Werkgebied', 'werkgebied'), ('veelgestelde-vragen.html', 'Vragen', 'vragen'), ('contact.html', 'Contact', 'contact')]
WA_STANDAARD = 'Hallo, ik heb een vraag over mijn autobanden.'


def header(r, pagina):
    links = ''.join(f'<a href="{r}{u}"' + (' aria-current="page"' if k == pagina else '') + f'>{t}</a>' for u, t, k in NAV)
    mlinks = ''.join(f'<a href="{r}{u}">{t}</a>' for u, t, k in NAV)
    return (f'<a class="skip" href="#main">Direct naar de inhoud</a>\n'
            f'<header class="hdr"><div class="wrap hdr__in">{logo(r)}'
            f'<nav class="nav" aria-label="Hoofdmenu">{links}</nav>'
            f'<div class="hdr__knop"><a class="btn btn--wa" href="{wa(WA_STANDAARD)}">{icon("wa")}WhatsApp</a>'
            f'<a class="btn" href="tel:{C["telefoonLink"]}">{icon("tel")}{TELNR}</a></div>'
            f'<button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav">{icon("menu")}</button></div></header>\n'
            f'<nav class="mnav" id="mnav" aria-label="Menu">{mlinks}'
            f'<a class="btn btn--vol btn--groot" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel {TELNR}</a>'
            f'<a class="btn btn--wa btn--vol btn--groot" href="{wa(WA_STANDAARD)}">{icon("wa")}WhatsApp</a></nav>\n'
            f'<div class="belbalk"><a class="btn" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel direct</a>'
            f'<a class="btn btn--wa" href="{wa(WA_STANDAARD)}">{icon("wa")}WhatsApp</a></div>\n')


def footer(r):
    provs = ''.join(f'<li><a href="{r}werkgebied/{p["slug"]}/">{E(p["naam"])}</a></li>' for p in PROVINCIES.values())
    diensten = ''.join(f'<li><a href="{r}diensten.html#{d[0]}">{d[1]}</a></li>' for d in DIENSTEN)
    return (f'<footer class="ftr"><div class="wrap"><div class="ftr__grid">'
            f'<div>{logo(r)}<p>Mobiele bandenservice voor personenauto\'s. Lekke band, nieuwe banden of de seizoenswissel: wij komen naar u toe, thuis, op het werk of langs de weg.</p>'
            f'<p class="ftr__adres">{E(C["bedrijf"])}<br>{E(C["straat"])}<br>{E(C["postcode"])} {E(C["plaats"])}<br>KvK {E(C["kvk"])}</p></div>'
            f'<div><h2 class="ftr__kop">Diensten</h2><ul>{diensten}<li><a href="{r}hulp-aanvragen.html">Hulp aanvragen</a></li></ul></div>'
            f'<div><h2 class="ftr__kop">Werkgebied</h2><ul class="ftr__provs">{provs}</ul></div>'
            f'<div><h2 class="ftr__kop">Contact</h2><ul><li><a href="tel:{C["telefoonLink"]}">{TELNR}</a></li>'
            f'<li><a href="{wa(WA_STANDAARD)}">WhatsApp</a></li><li><a href="{r}hulp-aanvragen.html">Hulp aanvragen</a></li>'
            f'<li><a href="{r}veelgestelde-vragen.html">Veelgestelde vragen</a></li><li><a href="{r}contact.html">Contact</a></li></ul></div>'
            f'</div><div class="ftr__onder"><span>&copy; {time.strftime("%Y")} {E(C["naam"])} is een handelsnaam van {E(C["bedrijf"])}, KvK {E(C["kvk"])}</span>'
            f'<span><a href="{r}privacy.html">Privacy</a><a href="{r}beeldverantwoording.html">Beeldverantwoording</a></span></div></div></footer>\n')


def cta(r, titel='Lekke band of nieuwe banden nodig?', tekst='Bel of app ons direct. We zeggen eerlijk wanneer we er kunnen zijn en wat het kost.', plaats=''):
    msg = 'Hallo, ik heb een vraag over mijn autobanden' + (f' in {plaats}' if plaats else '') + '.'
    return (f'<section class="wrap" style="margin-top:clamp(64px,9vw,120px)"><div class="cta rv"><div><h2>{titel}</h2><p>{tekst}</p></div>'
            f'<div><a class="cta__tel" href="tel:{C["telefoonLink"]}">{TELNR}</a><div class="cta__knoppen">'
            f'<a class="btn btn--groot" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel direct</a>'
            f'<a class="btn btn--wa btn--groot" href="{wa(msg)}">{icon("wa")}WhatsApp</a></div></div></div></section>\n')



def bedrijf_schema():
    s = {'@context': 'https://schema.org', '@type': 'TireShop', '@id': DOMEIN + '/#bedrijf', 'name': C['naam'],
         'description': 'Mobiele bandenservice voor personenauto\'s: lekke band, nieuwe banden en seizoenswissel, thuis, op het werk of langs de weg, in heel Nederland.',
         'url': DOMEIN + '/', 'telephone': C['telefoonLink'], 'image': DOMEIN + '/assets/img/og.jpg', 'logo': DOMEIN + '/icon-512.png',
         'legalName': C['bedrijf'], 'identifier': {'@type': 'PropertyValue', 'propertyID': 'KvK', 'value': C['kvk']},
         'address': {'@type': 'PostalAddress', 'streetAddress': C['straat'], 'postalCode': C['postcode'], 'addressLocality': C['plaats'], 'addressCountry': 'NL'},
         'areaServed': {'@type': 'Country', 'name': 'Nederland'}, 'openingHours': C['openingstijdenSchema'],
         'contactPoint': {'@type': 'ContactPoint', 'telephone': C['telefoonLink'], 'contactType': 'customer service', 'areaServed': 'NL', 'availableLanguage': ['nl', 'en']}}
    if C['email']:
        s['email'] = C['email']
    if C['google'].get('profielUrl'):
        s['sameAs'] = [C['google']['profielUrl']]
    return s


def kruimel_schema(stappen):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': DOMEIN + u} for i, (n, u) in enumerate(stappen)]}


def faq_schema(body):
    vragen = re.findall(r'<details><summary>(.*?)<i></i></summary><div class="a">(.*?)</div></details>', body, re.S)
    if not vragen:
        return None
    schoon = lambda t: html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))).strip()
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': schoon(q), 'acceptedAnswer': {'@type': 'Answer', 'text': schoon(a)}} for q, a in vragen]}


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>\n'


def head(r, titel, beschrijving, pad, schemas, og_beeld='og.jpg', noindex=False):
    canon = DOMEIN + '/' + pad
    verif = f'<meta name="google-site-verification" content="{E(C["google"]["verificatie"])}">\n' if C['google'].get('verificatie') else ''
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    return (f'<!DOCTYPE html>\n<html lang="nl">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<script>if(!window.matchMedia||!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("anim")</script>\n'
            f'<title>{E(titel)}</title>\n<meta name="description" content="{E(beschrijving)}">\n{robots}'
            f'<link rel="canonical" href="{canon}">\n{verif}'
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="nl_NL">\n'
            f'<meta property="og:site_name" content="{E(C["naam"])}">\n<meta property="og:title" content="{E(titel)}">\n'
            f'<meta property="og:description" content="{E(beschrijving)}">\n<meta property="og:url" content="{canon}">\n'
            f'<meta property="og:image" content="{DOMEIN}/assets/img/{og_beeld}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="theme-color" content="#15120E">\n'
            f'<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">\n<link rel="icon" href="{r}favicon-32.png" sizes="32x32" type="image/png">\n'
            f'<link rel="apple-touch-icon" href="{r}apple-touch-icon.png">\n<link rel="manifest" href="{r}site.webmanifest">\n'
            f'<link rel="preload" href="{r}assets/fonts/barlow-condensed-800.woff2" as="font" type="font/woff2" crossorigin>\n'
            f'<link rel="preload" href="{r}assets/fonts/barlow-400.woff2" as="font" type="font/woff2" crossorigin>\n'
            f'<link rel="stylesheet" href="{r}assets/css/site.css?v={VERSIE}">\n'
            + ''.join(ld(s) for s in schemas if s) +
            f'</head>\n<body>\n')


WA_LOGO = 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z'


def scripts(r):
    knop = (f'<a class="wa-knop" href="{wa(WA_STANDAARD)}" aria-label="Stuur ons een WhatsApp-bericht">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{WA_LOGO}"/></svg><span>WhatsApp ons</span></a>\n')
    return (knop + f'<script src="{r}assets/js/config.js?v={VERSIE}"></script>\n'
            f'<script src="{r}assets/js/app.js?v={VERSIE}" defer></script>\n</body>\n</html>\n')


SITEMAP = []


def schrijf(pad, r, titel, beschrijving, pagina, body, kruimels=None, extra_schema=None, prioriteit='0.6', og='og.jpg', noindex=False):
    schemas = [bedrijf_schema()] if pagina == 'home' else [{'@context': 'https://schema.org', '@type': 'WebPage', 'name': titel, 'url': DOMEIN + '/' + pad,
                                                             'isPartOf': {'@type': 'WebSite', 'name': C['naam'], 'url': DOMEIN + '/'}, 'publisher': {'@id': DOMEIN + '/#bedrijf'}}]
    if kruimels:
        schemas.append(kruimel_schema(kruimels))
    schemas += (extra_schema or [])
    schemas.append(faq_schema(body))
    doel = SITE / (pad + 'index.html' if pad.endswith('/') or pad == '' else pad)
    doel.parent.mkdir(parents=True, exist_ok=True)
    doel.write_text(head(r, titel, beschrijving, pad, schemas, og, noindex) + header(r, pagina) + '<main id="main">\n' + body + '</main>\n' + footer(r) + scripts(r), encoding='utf-8')
    if not noindex:
        SITEMAP.append((DOMEIN + '/' + pad, prioriteit))


def kruimelpad(r, stappen):
    delen = []
    for i, (naam, url) in enumerate(stappen):
        delen.append(f'<span>{E(naam)}</span>' if i == len(stappen) - 1 else f'<a href="{r}{url}">{E(naam)}</a><span>/</span>')
    return '<nav class="kruimel" aria-label="Kruimelpad">' + ''.join(delen) + '</nav>'


def pkop(r, h1, lead, beeld, stappen=None, knoppen=True, plaats=''):
    msg = 'Hallo, ik heb een vraag over mijn autobanden' + (f' in {plaats}' if plaats else '') + '.'
    kn = (f'<div class="hero__knoppen" style="margin-top:28px"><a class="btn btn--groot" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel {TELNR}</a>'
          f'<a class="btn btn--wa btn--groot" href="{wa(msg)}">{icon("wa")}WhatsApp</a></div>') if knoppen else ''
    kr = kruimelpad(r, stappen) if stappen else ''
    bld = f'<div class="pkop__beeld">{img(r, beeld, "100vw", lui=False, alt="")}</div>' if beeld else ''
    return f'<section class="pkop">{bld}<div class="wrap"><div class="pkop__in">{kr}<h1>{h1}</h1><p class="lead">{lead}</p>{kn}</div></div></section>\n'


def faq(vragen):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}<i></i></summary><div class="a"><p>{a}</p></div></details>' for q, a in vragen) + '</div>'


def provkaarten(r, licht=False):
    k = ''.join(f'<a class="provkaart" href="{r}werkgebied/{p["slug"]}/"><div><b>{E(p["naam"])}</b><span>{len(p["gemeenten"])} gemeenten</span></div>{icon("pijl")}</a>'
                for p in PROVINCIES.values())
    return f'<div class="provkaarten{" provkaarten--licht" if licht else ""}">{k}</div>'


def vinkjes(items):
    return '<ul class="vinkjes">' + ''.join(f'<li>{icon("vink")}<span>{t}</span></li>' for t in items) + '</ul>'




# ---------------------------------------------------------------- inhoud
# (id, titel, foto, kort, lang, punten, keuze in de hulpmelder)
DIENSTEN = [
    ('lekke-band', 'Lekke band', 'lekke-band',
     'Een spijker in de band of een band die langzaam leegloopt. Wij repareren of vervangen hem op de plek waar uw auto staat.',
     'Zit er een spijker of schroef in het loopvlak, dan is de band vaak te repareren. Zit de schade in de zijkant, of is er met de lege band gereden, dan is een nieuwe band veiliger. Wij bekijken de band ter plekke en zeggen eerlijk wat er nodig is, voordat we beginnen.',
     ['Reparatie van het loopvlak, als dat veilig kan', 'Een nieuwe band als repareren niet verantwoord is', 'Thuis, op het werk of langs de weg'], 'Lekke band'),
    ('nieuwe-banden', 'Nieuwe banden', 'balanceren',
     'Nieuwe zomer-, winter- of all-seasonbanden, gemonteerd en gebalanceerd op uw eigen oprit.',
     'Geef uw bandenmaat door en vertel of u zomer-, winter- of all-seasonbanden wilt. U hoort vooraf wat de banden kosten, inclusief montage en balanceren. Wij komen met de banden naar u toe en monteren ze op de oprit, in de straat of op de parkeerplaats van uw werk.',
     ['Zomer-, winter- en all-seasonbanden', 'Montage en balanceren op locatie', 'Prijs vooraf, inclusief montage'], 'Nieuwe banden'),
    ('seizoenswissel', 'Seizoenswissel', 'winterband',
     'Van zomer- naar winterbanden en weer terug, zonder dat u naar de garage hoeft.',
     'In oktober en maart staat u bij de garage al snel in de rij. Wij wisselen uw wielen of banden bij u thuis of op het werk. Liggen de wielen met banden al in de schuur, dan zetten we ze om en controleren we meteen het profiel en de bandenspanning.',
     ['Complete wielen of alleen banden wisselen', 'Controle van profiel en bandenspanning', 'Thuis of op uw werkplek'], 'Seizoenswissel'),
    ('langs-de-weg', 'Lekke band onderweg', 'thuiskomer',
     'Een lekke band onderweg en geen reservewiel, of alleen een thuiskomer waar u niet ver mee komt? Wij komen naar u toe.',
     'Veel nieuwe auto\'s hebben geen reservewiel meer, en met een thuiskomer mag u maar kort en niet harder dan 80 kilometer per uur rijden. Staat u stil met een lekke band, bel of app ons dan met uw locatie en de bandenmaat. Dan komen we met de juiste band.',
     ['Geen reservewiel of alleen een thuiskomer', 'Deel uw locatie via WhatsApp', 'Wij komen met de band in de juiste maat'], 'Lekke band'),
]

ALGEMENE_VRAGEN = [
    ('Waar vind ik mijn bandenmaat?', 'Op de zijkant van de band, bijvoorbeeld 205/55 R16 91V. Het eerste getal is de breedte in millimeters, het tweede de hoogte van de zijkant als percentage van die breedte, en het getal na de R is de velgmaat in inches. Lukt het lezen niet, stuur dan een foto van de zijkant via WhatsApp.'),
    ('Hoe snel kunnen jullie er zijn?', 'Dat hangt af van waar u staat en hoe druk het is, bijvoorbeeld rond de seizoenswissel. Bij uw melding zeggen we eerlijk wanneer we er kunnen zijn.'),
    ('Wat kost een nieuwe band?', 'Dat hangt af van de maat, het merk en het type band. U hoort de prijs vooraf, inclusief montage en balanceren, zodat u niet voor verrassingen komt te staan.'),
    ('Kunnen jullie een lekke band repareren?', 'Een gaatje in het loopvlak is vaak te repareren. Zit de schade in de zijkant, of is er met de lege band gereden, dan raden we een nieuwe band aan. Dat bekijken we ter plekke.'),
    ('Wanneer wissel ik naar winterbanden?', 'In Nederland zijn winterbanden niet verplicht. Een goede vuistregel is: winterbanden van oktober tot Pasen, of zodra het overdag structureel kouder wordt dan zeven graden. Daaronder hebben winterbanden meer grip dan zomerbanden.'),
    ('Hoeveel profiel moet er op mijn banden zitten?', 'Wettelijk minimaal 1,6 millimeter. Voor zomerbanden adviseren we te vervangen bij 3 millimeter, voor winterbanden bij 4 millimeter. Wij meten het profiel bij elke klus gratis voor u na.'),
    ('Moet ik thuis zijn als jullie komen?', 'De auto moet bereikbaar zijn en we hebben de sleutel nodig. Heeft uw auto slotbouten, leg dan de bijbehorende sleuteldop klaar; die ligt meestal in het handschoenenkastje of bij de krik.'),
    ('Helpen jullie ook bij bestelbussen en vrachtwagens?', 'Wij werken aan personenauto\'s, SUV\'s en bestelbussen. Voor vrachtwagens, trailers en zwaar transport kunt u terecht bij onze zusterservice Truckbandenhulp, op hetzelfde nummer.'),
    ('Moet ik lid zijn van een pechhulpdienst?', 'Nee. Iedereen kan ons bellen of appen, u hoeft nergens lid van te zijn en er is geen abonnement nodig.'),
    ('Hoe betaal ik?', 'Na afloop betaalt u ter plekke met de pin, of op factuur als u zakelijk klant bent.'),
]

PLEKKEN = [
    ('Thuis', 'wiel-krik', 'Op uw oprit of in de straat voor de deur. U hoeft uw dag niet om te gooien en wacht gewoon binnen.'),
    ('Op het werk', 'winter-auto', 'Op de parkeerplaats van uw werk, terwijl u doorwerkt. Na uw werkdag rijdt u weg op de nieuwe banden.'),
    ('Langs de weg', 'lekke-band', 'Met een lekke band langs de weg of op een parkeerplaats. Deel uw locatie via WhatsApp, dan komen we naar u toe.'),
]


def maatwidget(r, plaats=''):
    """Invoerveld voor de bandenmaat met een directe knop naar WhatsApp."""
    return (f'<div class="maat" data-maat>'
            f'<p class="maat__titel">{icon("band")}Weet u uw bandenmaat?</p>'
            f'<div class="maat__rij"><label class="sr" for="maat-invoer">Bandenmaat</label>'
            f'<input class="maat__invoer" id="maat-invoer" name="maat" type="text" inputmode="text" autocomplete="off" spellcheck="false" placeholder="205/55 R16">'
            f'<label class="sr" for="maat-dienst">Wat heeft u nodig?</label>'
            f'<select class="maat__dienst" id="maat-dienst" name="dienst"><option>Lekke band</option><option>Nieuwe banden</option><option>Seizoenswissel</option></select>'
            f'<a class="btn btn--wa" data-maat-wa href="{wa(WA_STANDAARD)}"' + (f' data-plaats="{E(plaats)}"' if plaats else '') + f'>{icon("wa")}Stuur via WhatsApp</a></div>'
            f'<p class="maat__noot">De maat staat op de zijkant van de band, bijvoorbeeld <b>205/55 R16</b>. Weet u het niet? Stuur dan gewoon een foto.</p></div>')


def pagina_home():
    r = ''
    kaarten = ''
    for i, (did, titel, beeld, kort, *_rest) in enumerate(DIENSTEN):
        kaarten += (f'<a class="situatie rv" href="diensten.html#{did}">{img(r, beeld, "(max-width: 640px) 100vw, (max-width: 960px) 50vw, 25vw")}'
                    f'<div class="situatie__tekst"><h3>{titel}</h3><p>{kort}</p><span class="pijl">Meer over {titel.lower()} {icon("pijl")}</span></div></a>')
    plekken = ''.join(f'<div class="plek rv"><div class="foto foto--breed">{img(r, b, "(max-width: 960px) 100vw, 33vw")}</div><h3>{t}</h3><p>{tekst}</p></div>' for t, b, tekst in PLEKKEN)
    body = f'''<section class="hero">
  <div class="hero__beeld">{img(r, 'wiel-wisselen', '100vw', lui=False, alt='')}</div>
  <div class="wrap"><div class="hero__in">
    <span class="boven">Mobiele bandenservice voor personenauto's</span>
    <h1>Lekke band of nieuwe banden? <em>Wij komen naar u toe.</em></h1>
    <p class="lead">Thuis op de oprit, op de parkeerplaats van uw werk of langs de weg: wij repareren, vervangen en wisselen uw banden op de plek waar uw auto staat.</p>
    {maatwidget(r)}
    <ul class="hero__punten"><li>{icon('pin')}In heel Nederland</li><li>{icon('auto')}Thuis, op het werk of langs de weg</li><li>{icon('vink')}Prijs vooraf</li></ul>
  </div></div>
  <span class="hero__bron">Foto: Santeri Viinamäki, CC BY-SA 4.0</span>
</section>
<div class="strip"><div class="strip__in"><span>Lekke band</span><span>Nieuwe banden</span><span>Seizoenswissel</span><span>Aan huis</span><span>Op het werk</span></div></div>

<section class="sec">
  <div class="wrap">
    <div class="kop rv"><div><span class="boven">Diensten</span><h2>Waarmee wij u helpen</h2></div>
      <p class="lead">Van een spijker in de band tot vier nieuwe winterbanden: wij komen met de juiste band en het juiste gereedschap naar u toe.</p></div>
    <div class="situaties situaties--vier">{kaarten}</div>
  </div>
</section>

<section class="sec sec--wit">
  <div class="wrap">
    <div class="kop rv"><div><span class="boven">Op locatie</span><h2>Waar uw auto ook staat</h2></div>
      <p class="lead">U hoeft niet naar de garage en niet te wachten in een wachtruimte. Wij komen naar u toe.</p></div>
    <div class="plekken">{plekken}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="kop rv"><div><span class="boven">Werkwijze</span><h2>Zo werkt het</h2></div>
      <p class="lead">Geef de bandenmaat en uw locatie door, de rest regelen wij.</p></div>
    <div class="aanpak rv">
      <div class="stap"><b>01</b><h3>Bel of app</h3><p>Geef door wat u nodig heeft, uw bandenmaat en waar de auto staat. Een foto van de band is ook goed.</p></div>
      <div class="stap"><b>02</b><h3>Prijs vooraf</h3><p>U hoort wat het kost, inclusief montage en balanceren, en wanneer we er kunnen zijn.</p></div>
      <div class="stap"><b>03</b><h3>Wij komen eraan</h3><p>Met de banden in de juiste maat en al het gereedschap om ze ter plekke te monteren.</p></div>
      <div class="stap"><b>04</b><h3>Weer op weg</h3><p>We zetten de banden op spanning, controleren het profiel en u rijdt weer veilig verder.</p></div>
    </div>
  </div>
</section>

<section class="sec sec--wit">
  <div class="wrap twee">
    <figure class="foto foto--hoog rv" style="margin:0">{img(r, 'winterband', '(max-width: 960px) 100vw, 50vw')}<figcaption>Foto: GT1976, CC BY-SA 4.0</figcaption></figure>
    <div class="rv">
      <span class="boven">Bandenmaat</span>
      <h2>Zo leest u uw bandenmaat</h2>
      <p class="lead" style="margin-top:16px">Op de zijkant van elke band staat een code, bijvoorbeeld <b>195/55 R16 91H</b>. Met die code komen we met precies de goede band.</p>
      <ul class="regels">
        <li class="wel"><i>195</i><div><b>Breedte</b><span>De breedte van de band in millimeters.</span></div></li>
        <li class="wel"><i>55</i><div><b>Hoogte</b><span>De hoogte van de zijkant, als percentage van de breedte.</span></div></li>
        <li class="wel"><i>R16</i><div><b>Velgmaat</b><span>De diameter van de velg in inches. De R staat voor radiaalband.</span></div></li>
        <li class="wel"><i>91H</i><div><b>Draagvermogen en snelheid</b><span>Hoeveel gewicht de band mag dragen en hoe hard u ermee mag rijden.</span></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--donker">
  <div class="wrap gebied">
    <div class="rv">
      <span class="boven">Werkgebied</span>
      <h2>Overal in Nederland</h2>
      <p class="lead" style="margin-top:16px">Wij komen naar u toe in alle 342 gemeenten van Nederland, van de grote stad tot het kleinste dorp. Kies uw provincie voor de gemeenten en woonplaatsen bij u in de buurt.</p>
      <div class="hero__knoppen" style="margin-top:28px"><a class="btn" href="tel:{C['telefoonLink']}">{icon('tel')}Bel {TELNR}</a><a class="btn btn--rand" href="werkgebied/">Bekijk alle gemeenten</a></div>
    </div>
    <figure class="foto foto--breed rv" style="margin:0">{img(r, 'winter-auto')}<figcaption>Foto: Michael, CC BY 2.0</figcaption></figure>
  </div>
  <div class="wrap rv" style="margin-top:clamp(40px,5vw,64px)">{provkaarten(r)}</div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="kop kop--midden rv"><div><h2>Veelgestelde vragen</h2></div></div>
    <div class="rv">{faq(ALGEMENE_VRAGEN[:6])}</div>
    <p style="text-align:center;margin:28px 0 0"><a class="pijl" href="veelgestelde-vragen.html">Alle vragen bekijken {icon('pijl')}</a></p>
  </div>
</section>
{cta(r)}'''
    schrijf('', r, 'Mobiele bandenservice aan huis | Mobiele Autobanden',
            'Lekke band, nieuwe banden of de seizoenswissel? Mobiele Autobanden komt naar u toe: thuis, op het werk of langs de weg. Bel of app 085 744 4166.',
            'home', body, prioriteit='1.0')


def pagina_diensten():
    r = ''
    rijen = ''
    for did, titel, beeld, kort, lang, punten, keuze in DIENSTEN:
        maker = BEELD[beeld][1]; lic = BEELD[beeld][2]
        rijen += (f'<div class="sit-rij" id="{did}"><figure class="foto foto--breed rv" style="margin:0">{img(r, beeld)}<figcaption>Foto: {E(maker)}, {lic}</figcaption></figure>'
                  f'<div class="rv"><h2>{titel}</h2><p class="lead">{kort}</p><p>{lang}</p>{vinkjes(punten)}'
                  f'<div class="hero__knoppen" style="margin-top:26px"><a class="btn" href="hulp-aanvragen.html?dienst={quote(keuze)}">Hulp aanvragen</a>'
                  f'<a class="btn btn--licht" href="tel:{C["telefoonLink"]}">Bel {TELNR}</a></div></div></div>')
    body = (pkop(r, 'Onze diensten', 'Lekke band, nieuwe banden of de seizoenswissel: alles gebeurt op de plek waar uw auto staat. Hieronder leest u wat we doen en waar u op kunt letten.',
                 'wiel-krik', [('Home', ''), ('Diensten', 'diensten.html')])
            + f'<section class="sec" style="padding-top:clamp(24px,4vw,48px)"><div class="wrap">{rijen}</div></section>\n' + cta(r))
    schrijf('diensten.html', r, 'Diensten: lekke band, nieuwe banden en seizoenswissel',
            'Lekke band repareren, nieuwe banden monteren en balanceren of de seizoenswissel: Mobiele Autobanden doet het thuis, op het werk of langs de weg.',
            'diensten', body, [('Home', '/'), ('Diensten', '/diensten.html')], prioriteit='0.9')


def keuzes(naam, opties):
    return '<div class="keuzes">' + ''.join(f'<label class="keuze"><input type="radio" name="{naam}" value="{E(o)}"><span>{E(o)}</span></label>' for o in opties) + '</div>'


def pagina_hulp():
    r = ''
    body = (pkop(r, 'Hulp aanvragen', 'Vul in wat u weet en verstuur alles in één WhatsApp-bericht. Hoe meer we vooraf weten, hoe sneller we met de juiste band bij u zijn. Liever direct iemand spreken? Bel '
                 f'<a href="tel:{C["telefoonLink"]}">{TELNR}</a>.', 'lekke-band', [('Home', ''), ('Hulp aanvragen', 'hulp-aanvragen.html')], knoppen=False)
            + f'''<section class="sec" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap">
<div class="melder" data-melder>
  <div class="melder__links">
    <fieldset class="vraag"><legend><i>1</i>Wat heeft u nodig?</legend>{keuzes('dienst', ['Lekke band', 'Nieuwe banden', 'Seizoenswissel', 'Iets anders'])}</fieldset>
    <div class="vraag"><p class="vraag__titel"><i>2</i>Bandenmaat</p>
      <div class="velden">
        <div class="veld"><label for="maat">Bandenmaat (als u die weet)</label><input class="inp" id="maat" name="maat" type="text" autocomplete="off" spellcheck="false" placeholder="205/55 R16"></div>
        <div class="veld"><label for="aantal">Aantal banden</label><select class="inp" id="aantal" name="aantal"><option value="">Kies</option><option>1</option><option>2</option><option>4</option></select></div>
      </div>
      <p class="melder__noot">De maat staat op de zijkant van de band. Weet u hem niet, stuur dan na dit bericht een foto van de zijkant.</p>
    </div>
    <fieldset class="vraag"><legend><i>3</i>Soort band</legend>{keuzes('soort', ['Zomerband', 'Winterband', 'All-season', 'Weet ik niet'])}</fieldset>
    <fieldset class="vraag"><legend><i>4</i>Waar staat de auto?</legend>{keuzes('plek', ['Thuis', 'Op het werk', 'Langs de weg'])}</fieldset>
    <div class="vraag"><p class="vraag__titel"><i>5</i>Locatie</p>
      <div class="veld"><label for="locatie">Adres, plaats of herkenningspunt</label>
        <div class="locatie"><input class="inp" id="locatie" name="locatie" type="text" autocomplete="address-line1" placeholder="Bijvoorbeeld: Dorpsstraat 12, Lunteren"><button class="btn btn--donker" type="button" data-locatie>{icon('pin')}Mijn locatie</button></div>
        <span class="veld__fout">Vul uw adres in of deel uw GPS-locatie, dan weten we waar we moeten zijn.</span>
        <p class="locatie__status" data-locatie-status aria-live="polite"></p></div>
    </div>
    <div class="vraag"><p class="vraag__titel"><i>6</i>Uw gegevens</p>
      <div class="velden">
        <div class="veld"><label for="naam">Naam</label><input class="inp" id="naam" name="naam" type="text" autocomplete="name"></div>
        <div class="veld"><label for="telefoon">Telefoon</label><input class="inp" id="telefoon" name="telefoon" type="tel" autocomplete="tel" inputmode="tel"></div>
        <div class="veld"><label for="kenteken">Kenteken (als u het weet)</label><input class="inp" id="kenteken" name="kenteken" type="text" autocomplete="off" spellcheck="false"></div>
        <div class="veld veld--vol"><label for="toelichting">Toelichting</label><textarea class="inp" id="toelichting" name="toelichting" placeholder="Bijvoorbeeld: spijker in de linker voorband, of: ik heb de winterbanden al liggen"></textarea></div>
      </div>
    </div>
  </div>
  <div class="melder__rechts">
    <h2>Uw bericht</h2>
    <pre class="bericht" data-bericht aria-live="polite"></pre>
    <a class="btn btn--wa btn--vol btn--groot" data-verstuur href="{wa()}">{icon('wa')}Verstuur via WhatsApp</a>
    <a class="btn btn--licht btn--vol" href="tel:{C['telefoonLink']}">{icon('tel')}Of bel {TELNR}</a>
    <p class="melder__noot">Stuur na het bericht gerust een foto van de band via WhatsApp. Uw gegevens gebruiken we alleen om u te helpen, zie onze <a href="privacy.html">privacyverklaring</a>.</p>
  </div>
</div>
</div></section>
''' + cta(r, 'Liever direct bellen?', 'Dan helpen we u telefonisch verder en plannen we meteen een tijd in.'))
    schrijf('hulp-aanvragen.html', r, 'Hulp aanvragen voor uw autobanden | Mobiele Autobanden',
            'Lekke band, nieuwe banden of seizoenswissel? Geef uw bandenmaat en locatie door en verstuur alles via WhatsApp. Of bel direct 085 744 4166.',
            'hulp', body, [('Home', '/'), ('Hulp aanvragen', '/hulp-aanvragen.html')], prioriteit='0.9')


def pagina_vragen():
    r = ''
    body = (pkop(r, 'Veelgestelde vragen', 'Waar vind ik mijn bandenmaat, wat kost een nieuwe band en wanneer wissel ik naar winterbanden? Hier vindt u de antwoorden. Staat uw vraag er niet bij, bel of app ons gerust.',
                 'balanceren', [('Home', ''), ('Veelgestelde vragen', 'veelgestelde-vragen.html')])
            + f'<section class="sec"><div class="wrap">{faq(ALGEMENE_VRAGEN)}</div></section>\n' + cta(r))
    schrijf('veelgestelde-vragen.html', r, 'Veelgestelde vragen over autobanden | Mobiele Autobanden',
            'Waar vind ik mijn bandenmaat, wat kost een nieuwe band, hoeveel profiel is nodig en wanneer wissel ik naar winterbanden? Antwoorden op de meestgestelde vragen.',
            'vragen', body, [('Home', '/'), ('Veelgestelde vragen', '/veelgestelde-vragen.html')], prioriteit='0.7')


def pagina_contact():
    r = ''
    tijden = ''.join(f'<li><span>{E(d)}</span><b>{E(t)}</b></li>' for d, t in C['openingstijden'])
    email = f'<li><span>E-mail</span><b><a href="mailto:{E(C["email"])}">{E(C["email"])}</a></b></li>' if C['email'] else ''
    body = (pkop(r, 'Neem direct contact op', 'Bellen of appen is het snelst. Voor een lekke band, nieuwe banden, de seizoenswissel of zakelijke afspraken voor uw wagenpark kunt u ons bellen of een WhatsApp sturen.',
                 'wiel-krik', [('Home', ''), ('Contact', 'contact.html')])
            + f'''<section class="sec"><div class="wrap kaarten">
  <div class="kaart"><h2 style="font-size:1.6rem;margin-bottom:12px">Bedrijfsgegevens</h2><ul class="rij-lijst">
    <li><span>Telefoon</span><b><a href="tel:{C['telefoonLink']}">{TELNR}</a></b></li>
    <li><span>WhatsApp</span><b><a href="{wa(WA_STANDAARD)}">Stuur een bericht</a></b></li>{email}
    <li><span>Werkgebied</span><b>Heel Nederland</b></li>
    <li><span>Bedrijf</span><b>{E(C['bedrijf'])}</b></li>
    <li><span>Adres</span><b>{E(C['straat'])}<br>{E(C['postcode'])} {E(C['plaats'])}</b></li>
    <li><span>KvK</span><b>{E(C['kvk'])}</b></li></ul></div>
  <div class="kaart"><h2 style="font-size:1.6rem;margin-bottom:12px">Bereikbaarheid</h2><ul class="rij-lijst">{tijden}</ul>
    <p style="margin:14px 0 0;color:var(--zacht)">Rond de seizoenswissel in oktober en maart is het druk. Plan uw wissel op tijd, dan zijn we er wanneer het u uitkomt.</p></div>
  <div class="kaart kaart--donker"><h2 style="font-size:1.6rem;margin-bottom:12px;color:#fff">Hulp nodig?</h2><p>Geef uw bandenmaat en locatie door, dan komen we met de juiste band.</p>
    <a class="btn btn--vol" href="hulp-aanvragen.html">Hulp aanvragen</a><a class="btn btn--wa btn--vol" href="{wa(WA_STANDAARD)}">{icon('wa')}WhatsApp</a></div>
</div></section>
''' + cta(r))
    schrijf('contact.html', r, 'Contact | Mobiele Autobanden', 'Bel of app Mobiele Autobanden op 085 744 4166 voor een lekke band, nieuwe banden of de seizoenswissel. Een handelsnaam van D&D Mobiliteit B.V.',
            'contact', body, [('Home', '/'), ('Contact', '/contact.html')], prioriteit='0.6')


def pagina_privacy():
    r = ''
    body = (pkop(r, 'Privacyverklaring', 'Wij gaan zorgvuldig met uw gegevens om. Hieronder leest u welke gegevens wij gebruiken, waarvoor en hoe lang.', None, [('Home', ''), ('Privacy', 'privacy.html')], knoppen=False)
            + f'''<section class="sec"><div class="wrap tekstpagina">
<h2>Wie zijn wij</h2><p>{E(C['naam'])} is een handelsnaam van {E(C['bedrijf'])}, gevestigd aan de {E(C['straat'])}, {E(C['postcode'])} {E(C['plaats'])}, ingeschreven bij de Kamer van Koophandel onder nummer {E(C['kvk'])}. Wij zijn verantwoordelijk voor de verwerking van uw gegevens zoals beschreven in deze verklaring.</p>
<h2>Welke gegevens wij gebruiken</h2><p>Als u ons belt, een WhatsApp-bericht stuurt of het formulier op deze website gebruikt, ontvangen wij de gegevens die u zelf doorgeeft: uw naam, telefoonnummer, adres of locatie, kenteken, bandenmaat en eventuele foto's.</p>
<h2>Het formulier op deze website</h2><p>Het formulier stelt een WhatsApp-bericht voor u op. Er wordt niets via deze website opgeslagen of verstuurd: pas als u zelf op versturen tikt, gaat het bericht via WhatsApp naar ons. Uw GPS-locatie wordt alleen opgehaald als u daar zelf op tikt en uw browser toestemming geeft.</p>
<h2>Waarvoor</h2><p>Wij gebruiken uw gegevens om u te helpen, contact met u op te nemen, de klus uit te voeren en te factureren. Wij verkopen uw gegevens niet en delen ze alleen als dat nodig is voor de uitvoering, bijvoorbeeld met onze boekhouder, of als de wet ons daartoe verplicht.</p>
<h2>Hoe lang</h2><p>Gegevens voor de facturatie bewaren wij zeven jaar, omdat de wet dat vraagt. Overige gegevens verwijderen wij zodra ze niet meer nodig zijn.</p>
<h2>Cookies en statistieken</h2><p>Deze website plaatst geen trackingcookies en gebruikt geen advertentienetwerken.</p>
<h2>Uw rechten</h2><p>U kunt ons altijd vragen welke gegevens wij van u hebben, en vragen om ze te verbeteren of te verwijderen. Neem daarvoor contact op via {TELNR}. Bent u het niet eens met hoe wij met uw gegevens omgaan, dan kunt u een klacht indienen bij de Autoriteit Persoonsgegevens.</p>
</div></section>
''')
    schrijf('privacy.html', r, 'Privacyverklaring | Mobiele Autobanden', 'Lees hoe Mobiele Autobanden, een handelsnaam van D&D Mobiliteit B.V., omgaat met uw gegevens.',
            'privacy', body, [('Home', '/'), ('Privacy', '/privacy.html')], prioriteit='0.2')


def pagina_beeld():
    r = ''
    rijen = ''.join(f'<tr><td><img src="assets/img/{n}-640.webp" alt="" loading="lazy" width="96" height="64"></td><td><b>{E(b[5])}</b></td><td>{E(b[1])}</td>'
                    f'<td><a href="{b[3]}" rel="noopener">{b[2]}</a></td><td><a href="{E(b[4])}" rel="noopener">Bron</a></td></tr>\n' for n, b in BEELD.items())
    body = (pkop(r, 'Beeldverantwoording', 'De foto\'s op deze website zijn gedeeld onder een Creative Commons-licentie. Hieronder staan per foto de maker, de licentie en de bron. Waar nodig is de foto bijgesneden.',
                 None, [('Home', ''), ('Beeldverantwoording', 'beeldverantwoording.html')], knoppen=False)
            + f'<section class="sec"><div class="wrap"><div class="tabelwrap"><table class="credits"><thead><tr><th><span class="sr">Foto</span></th><th>Titel</th><th>Maker</th><th>Licentie</th><th>Bron</th></tr></thead>\n<tbody>{rijen}</tbody></table></div>'
            f'<p style="margin-top:20px;color:var(--zacht)">Lettertype: Barlow en Barlow Condensed van Jeremy Tribby, onder de SIL Open Font License.</p></div></section>\n')
    schrijf('beeldverantwoording.html', r, 'Beeldverantwoording | Mobiele Autobanden', 'Makers, licenties en bronnen van de foto\'s op de website van Mobiele Autobanden.',
            'beeld', body, [('Home', '/'), ('Beeldverantwoording', '/beeldverantwoording.html')], prioriteit='0.1')


def pagina_404():
    r = '/'
    body = (f'<section class="pkop"><div class="wrap"><div class="pkop__in"><h1>Deze pagina bestaat niet</h1>'
            f'<p class="lead">De link klopt niet meer, of er zit een typfout in het adres. Heeft u een lekke band of nieuwe banden nodig? Bel of app ons direct.</p>'
            f'<div class="hero__knoppen" style="margin-top:28px"><a class="btn btn--groot" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel {TELNR}</a>'
            f'<a class="btn btn--wa btn--groot" href="{wa(WA_STANDAARD)}">{icon("wa")}WhatsApp</a>'
            f'<a class="btn btn--rand btn--groot" href="/">Naar de homepage</a></div></div></div></section>\n')
    schrijf('404.html', r, 'Pagina niet gevonden | Mobiele Autobanden', 'Deze pagina bestaat niet. Bel of app Mobiele Autobanden op 085 744 4166.', '404', body, noindex=True)


INTRO = [
    'Een lekke band, nieuwe banden nodig of tijd voor de seizoenswissel in {G}? Wij komen naar u toe, thuis, op het werk of langs de weg, en doen het werk op de plek waar uw auto staat.',
    'In de hele gemeente {G} komen wij met de banden in de juiste maat naar u toe. U hoeft niet naar de garage en niet te wachten: wij monteren en balanceren op uw eigen oprit.',
    'Spijker in de band, profiel op of de winterbanden eronder? In {G} en omgeving regelen wij het aan huis of op de parkeerplaats van uw werk.',
    'Staat u in {G} met een lekke band, of wilt u zonder gedoe van zomer- naar winterbanden? Bel of app ons, dan komen we naar u toe, in heel {P}.',
]
SEIZOEN = [
    'Rond oktober en maart wil heel {G} tegelijk de banden wisselen. Plan uw seizoenswissel op tijd, dan komen we op een moment dat het u uitkomt.',
    'Liggen uw zomer- of winterbanden al klaar in de schuur? Dan zetten we ze in {G} gewoon voor u om en meten we meteen het profiel en de spanning na.',
    'Twijfelt u of uw banden nog goed zijn? Bij elke klus in {G} meten we het profiel gratis na en zeggen we eerlijk of vervangen nodig is.',
]


def gemeente_pagina(i, g):
    r = '../../'
    G, P = g['naam'], g['prov']
    beeld = ['wiel-wisselen', 'lekke-band', 'balanceren', 'wiel-krik'][i % 4]
    intro = INTRO[i % 4].format(G=E(G), P=E(P))
    seizoen = SEIZOEN[i % 3].format(G=E(G))
    woonpl = list(g['woonplaatsen'])
    kernen = ''
    if len(woonpl) > 1:
        kernen = (f'<h3>Woonplaatsen in de gemeente {E(G)}</h3><p>Wij komen in alle {len(woonpl)} woonplaatsen van de gemeente en in het buitengebied daaromheen:</p>'
                  f'<ul class="kernen">' + ''.join(f'<li>{E(w)}</li>' for w in woonpl) + '</ul>')
    buren = g['buren'][:8]
    burenlijst = ''.join(f'<li><a href="{r}{GEMPAD}/{b["slug"]}/">{E(b["naam"])}</a><span>{b["km"]} km</span></li>' for b in buren)
    b1, b2 = buren[0]['naam'], buren[1]['naam']
    vragen = [
        (f'Ik heb een lekke band in {E(G)}. Hoe snel kunnen jullie er zijn?', f'Dat hangt af van waar in de gemeente {E(G)} u staat en hoe druk het op dat moment is. Bij uw melding zeggen we eerlijk wanneer we er kunnen zijn. Deel uw locatie via WhatsApp, dan rijden we direct de goede kant op.'),
        (f'Komen jullie ook in {E(b1)} en {E(b2)}?', f'Ja. Naast {E(G)} komen we ook in {E(b1)}, {E(b2)} en de rest van {E(P)}. Wij werken in heel Nederland.'),
        (f'Kunnen jullie in {E(G)} ook bij mijn werk komen?', 'Ja. Wij monteren en wisselen banden ook op de parkeerplaats van uw werk, terwijl u doorwerkt. Zorg dat we bij de auto kunnen en dat de sleutel klaarligt.'),
        (f'Wat kosten nieuwe banden in {E(G)}?', 'Dat hangt af van de maat, het merk en het type band. U hoort de prijs vooraf, inclusief montage en balanceren, zodat u niet voor verrassingen komt te staan.'),
    ]
    body = (pkop(r, f'Bandenservice aan huis in {E(G)}', intro, beeld,
                 [('Home', ''), ('Werkgebied', 'werkgebied/'), (P, f'werkgebied/{g["prov_slug"]}/'), (G, '')], plaats=G)
            + f'''<section class="sec"><div class="wrap regio">
<div class="regio__tekst">
  <h2>Mobiele bandenservice in {E(G)}</h2>
  <p class="lead">Lekke band, nieuwe banden of de seizoenswissel: wij doen het in de hele gemeente {E(G)} op de plek waar uw auto staat.</p>
  <div class="landschap"><p>{seizoen}</p></div>
  <h3>Waar wij in {E(G)} komen</h3>
  {vinkjes(['Thuis, op uw oprit of in de straat', 'Op de parkeerplaats van uw werk', 'Langs de weg of op een parkeerplaats, bij een lekke band'])}
  {kernen}
  <h3>Onze diensten</h3>
  <ul class="vinkjes">{''.join(f'<li>{icon("vink")}<a href="{r}diensten.html#{d[0]}">{d[1]}</a></li>' for d in DIENSTEN)}</ul>
</div>
<aside class="regio__zij">
  <div class="kaart kaart--donker"><h3>Banden nodig in {E(G)}?</h3><p>Geef uw bandenmaat en adres door en verstuur alles in één WhatsApp-bericht.</p>
    <a class="btn btn--vol" href="{r}hulp-aanvragen.html?plaats={quote(G)}">Hulp aanvragen</a><a class="btn btn--rand btn--vol" href="tel:{C['telefoonLink']}">{icon('tel')}Bel {TELNR}</a></div>
  <div class="kaart"><h3>Ook in de buurt</h3><ul class="buren">{burenlijst}</ul>
    <p style="margin:14px 0 0"><a class="pijl" href="{r}werkgebied/{g['prov_slug']}/">Alle gemeenten in {E(P)} {icon('pijl')}</a></p></div>
</aside>
</div></section>
<section class="sec sec--wit"><div class="wrap"><div class="kop kop--midden"><div><span class="boven">Veelgestelde vragen</span><h2>Autobanden in {E(G)}</h2></div></div>{faq(vragen)}</div></section>
''' + cta(r, f'Banden nodig in {E(G)}?', 'Bel of app ons direct. We zeggen eerlijk wanneer we er kunnen zijn en wat het kost.', plaats=G))
    titel = f'Mobiele bandenservice in {G} | Mobiele Autobanden'
    if len(titel) > 60:
        titel = f'Bandenservice aan huis in {G}'
    if len(titel) > 60:
        titel = f'Bandenservice {G}'
    besch = f'Lekke band, nieuwe banden of seizoenswissel in {G}? Mobiele Autobanden komt naar u toe, thuis of op het werk. Bel of app 085 744 4166.'
    if len(besch) > 160:
        besch = f'Bandenservice aan huis in {G}: lekke band, nieuwe banden en seizoenswissel. Bel of app 085 744 4166.'
    pad = f'{GEMPAD}/{g["slug"]}/'
    dienst = {'@context': 'https://schema.org', '@type': 'Service', 'name': f'Mobiele bandenservice in {G}', 'serviceType': 'Mobiele bandenservice voor personenauto\'s',
              'provider': {'@id': DOMEIN + '/#bedrijf'}, 'areaServed': {'@type': 'City', 'name': G, 'containedInPlace': {'@type': 'AdministrativeArea', 'name': P}},
              'url': DOMEIN + '/' + pad}
    schrijf(pad, r, titel, besch, 'werkgebied', body,
            [('Home', '/'), ('Werkgebied', '/werkgebied/'), (P, f'/werkgebied/{g["prov_slug"]}/'), (G, '/' + pad)], [dienst], prioriteit='0.7')


def provincie_pagina(p):
    r = '../../'
    lijst = ''.join(f'<li><a href="{r}{GEMPAD}/{g["slug"]}/">{E(g["naam"])}</a></li>' for g in sorted(p['gemeenten'], key=lambda g: g['naam']))
    body = (pkop(r, f'Bandenservice aan huis in de provincie {E(p["naam"])}', f'Wij komen naar u toe in alle {len(p["gemeenten"])} gemeenten van {E(p["naam"])}: voor een lekke band, nieuwe banden of de seizoenswissel, thuis, op het werk of langs de weg.',
                 'winter-auto', [('Home', ''), ('Werkgebied', 'werkgebied/'), (p['naam'], '')])
            + f'''<section class="sec"><div class="wrap">
<div class="kop"><div><span class="boven">{E(p['naam'])}</span><h2>Kies uw gemeente</h2></div><p class="lead">Op elke gemeentepagina vindt u de woonplaatsen, de buurgemeenten en antwoord op de vragen die we daar het vaakst krijgen.</p></div>
<ul class="gemlijst">{lijst}</ul>
</div></section>
''' + cta(r, f'Banden nodig in {E(p["naam"])}?', 'Bel of app ons direct. We zeggen eerlijk wanneer we er kunnen zijn en wat het kost.'))
    pad = f'werkgebied/{p["slug"]}/'
    schrijf(pad, r, f'Bandenservice provincie {p["naam"]} | Mobiele Autobanden',
            f'Lekke band, nieuwe banden of seizoenswissel in {p["naam"]}? Mobiele Autobanden komt naar u toe in alle {len(p["gemeenten"])} gemeenten. Bel of app 085 744 4166.',
            'werkgebied', body, [('Home', '/'), ('Werkgebied', '/werkgebied/'), (p['naam'], '/' + pad)], prioriteit='0.7')


def werkgebied_pagina():
    r = '../'
    blokken = ''.join(f'<div class="provblok"><h2><a href="{p["slug"]}/" style="text-decoration:none">{E(p["naam"])}</a></h2><ul class="gemlijst">'
                      + ''.join(f'<li><a href="{r}{GEMPAD}/{g["slug"]}/">{E(g["naam"])}</a></li>' for g in sorted(p['gemeenten'], key=lambda g: g['naam']))
                      + '</ul></div>' for p in PROVINCIES.values())
    body = (pkop(r, 'Werkgebied: heel Nederland', f'Wij komen naar u toe in alle {len(GEMEENTEN)} gemeenten van Nederland. Kies uw provincie of gemeente voor de woonplaatsen en de buurgemeenten bij u in de buurt.',
                 'winter-auto', [('Home', ''), ('Werkgebied', 'werkgebied/')])
            + f'<section class="sec"><div class="wrap">{provkaarten(r, licht=True)}</div></section>\n'
            + f'<section class="sec sec--wit"><div class="wrap provblokken">{blokken}</div></section>\n' + cta(r))
    schrijf('werkgebied/', r, 'Werkgebied: heel Nederland | Mobiele Autobanden',
            f'Mobiele Autobanden komt naar u toe in alle {len(GEMEENTEN)} gemeenten van Nederland. Bekijk uw provincie of gemeente.',
            'werkgebied', body, [('Home', '/'), ('Werkgebied', '/werkgebied/')], prioriteit='0.8')



# ---------------------------------------------------------------- overige bestanden
def overig():
    (SITE / 'assets' / 'js' / 'config.js').write_text(
        'window.SITE = ' + json.dumps({k: C[k] for k in ('naam', 'telefoon', 'telefoonLink', 'whatsapp')}, ensure_ascii=False) + ';\n', encoding='utf-8')
    urls = ''.join(f'<url><loc>{u}</loc><lastmod>{VANDAAG}</lastmod><priority>{p}</priority></url>\n' for u, p in SITEMAP)
    (SITE / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n', encoding='utf-8')
    (SITE / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {DOMEIN}/sitemap.xml\n', encoding='utf-8')
    (SITE / 'site.webmanifest').write_text(json.dumps({'name': C['naam'], 'short_name': C['naam'], 'start_url': '/', 'display': 'standalone',
                                                        'background_color': '#15120E', 'theme_color': '#15120E',
                                                        'icons': [{'src': '/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                                  {'src': '/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, ensure_ascii=False, indent=1), encoding='utf-8')
    (SITE / 'favicon.svg').write_text(LOGO_MERK.replace(' class="logo__merk"', ' xmlns="http://www.w3.org/2000/svg"').replace(' aria-hidden="true"', ''), encoding='utf-8')


if __name__ == '__main__':
    import shutil
    for oud in ('auto-vast', 'situaties.html'):
        p = SITE / oud
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()
    pagina_home(); pagina_diensten(); pagina_hulp(); pagina_vragen(); pagina_contact(); pagina_privacy(); pagina_beeld(); pagina_404()
    werkgebied_pagina()
    for p in PROVINCIES.values():
        provincie_pagina(p)
    for i, g in enumerate(GEMEENTEN):
        gemeente_pagina(i, g)
    overig()
    print(f'klaar: {len(SITEMAP)} pagina\'s in de sitemap, {len(GEMEENTEN)} gemeenten')
