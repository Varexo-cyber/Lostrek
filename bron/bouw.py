"""Lostrek — bouwt de complete website in ../site.

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
    'band': '<path d="M3 17c3-1 4-4 9-4s6 3 9 4"/><path d="M12 13V4M8.5 7.5 12 4l3.5 3.5"/>',
}


def icon(naam, extra=''):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true"{extra}>{ICONEN[naam]}</svg>')


LOGO_MERK = ('<svg class="logo__merk" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="6" fill="#E8590C"/>'
             '<path d="M7 29.5c3.2-2.4 5.8-2.4 9 0s5.8 2.4 9 0 4.6-2.2 8-.4" fill="none" stroke="#15120E" stroke-width="3" stroke-linecap="round"/>'
             '<path d="M12.5 23.5 27 9M17.5 9H27v9.5" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="square"/></svg>')


def logo(r):
    return (f'<a class="logo" href="{r}./" aria-label="{E(C["naam"])}, naar de homepage">{LOGO_MERK}'
            f'<div><b>{E(C["naam"]).upper()}</b><span>{E(C["ondertitel"])}</span></div></a>')


# ---------------------------------------------------------------- data
PROVINCIES = {}
for g in GEMEENTEN:
    PROVINCIES.setdefault(g['prov_slug'], {'naam': g['prov'], 'slug': g['prov_slug'], 'gemeenten': []})['gemeenten'].append(g)
PROVINCIES = dict(sorted(PROVINCIES.items()))
PER_SLUG = {g['slug']: g for g in GEMEENTEN}

KUST = set('texel vlieland terschelling ameland schiermonnikoog den-helder schagen bergen-noord-holland castricum heemskerk '
           'velsen zandvoort bloemendaal noordwijk katwijk wassenaar den-haag westland voorne-aan-zee goeree-overflakkee '
           'schouwen-duiveland noord-beveland veere vlissingen sluis'.split())

LANDSCHAP = {
    'drenthe': ('zandwegen, bospaden en heide',
                'In Drenthe raken auto\'s vooral vast op zandwegen en bospaden die na een regenbui of dooi zacht worden, en in de drassige bermen langs smalle landwegen. Een voorwielaangedreven auto graaft zich in los zand snel in.',
                ['Zandwegen en bospaden', 'Drassige bermen langs smalle landwegen', 'Parkeren op gras bij recreatieparken en evenementen']),
    'flevoland': ('zware polderklei',
                  'De Flevolandse klei wordt na regen spekglad. Langs lange, rechte polderwegen liggen zachte bermen en akkerranden waar een wiel zo wegzakt, en wie uitwijkt voor een tegenligger staat sneller in de berm dan gedacht.',
                  ['Zachte bermen langs polderwegen', 'Akkerranden en kavelpaden', 'Gras- en evenemententerreinen']),
    'fryslan': ('klei, weilanden en dijkwegen',
                'In Fryslân liggen veel smalle wegen tussen de weilanden, met zachte kleibermen en sloten ernaast. Na een natte periode zakt een auto in de berm of op een erf zomaar weg.',
                ['Zachte bermen langs smalle polderwegen', 'Weilanden en boerenerven', 'Dijkwegen en parkeren op gras']),
    'gelderland': ('bospaden, uiterwaarden en zandwegen',
                   'In Gelderland ligt het tussen de Veluwse bospaden, de uiterwaarden langs Rijn, Waal en IJssel en de zandwegen in de Achterhoek. Na hoogwater of een natte week staan daar regelmatig auto\'s vast.',
                   ['Bospaden en zandwegen', 'Uiterwaarden en dijken', 'Weilanden bij evenementen en festivals']),
    'groningen': ('zware klei en landwegen',
                  'De Groninger klei is na regen glad en zwaar. Landwegen tussen de akkers hebben vaak zachte bermen, en langs maren en kanalen is de grond drassig.',
                  ['Bermen langs landwegen', 'Akkerpaden en erven', 'Parkeren op gras bij evenementen']),
    'limburg': ('heuvels en lössgrond',
                'In Zuid-Limburg maken de hellingen het lastig: lössgrond en graspaden worden na regen glibberig, en een auto die op een helling geen grip meer heeft schuift zo de berm in.',
                ['Hellende graspaden en holle wegen', 'Onverharde wegen in het heuvelland', 'Weilanden en parkeerterreinen bij evenementen']),
    'noord-brabant': ('zandpaden, bossen en evenemententerreinen',
                      'Brabant heeft veel zandpaden en bossen, en ieder seizoen grote evenementen waar op gras wordt geparkeerd. Na een paar dagen regen verandert zo\'n parkeerweiland in een modderbad.',
                      ['Festival- en evenementenparkeren op gras', 'Zandpaden en bosranden', 'Bermen langs landwegen']),
    'noord-holland': ('duinen, strand en veenweide',
                      'In Noord-Holland staan auto\'s vast in het mulle zand bij strandopgangen, op het strand zelf en in de natte veenweidebermen langs polderwegen.',
                      ['Strand en strandopgangen', 'Veenweidebermen langs polderwegen', 'Parkeren op gras bij evenementen']),
    'overijssel': ('zandwegen en boerenland',
                   'In Twente en Salland liggen veel zandwegen en kavelpaden, en ook de Sallandse Heuvelrug heeft onverharde wegen. Na regen of dooi zijn de randen zacht en zakt een auto snel weg.',
                   ['Zandwegen en kavelpaden', 'Bosranden en onverharde wegen', 'Boerenerven en weilanden']),
    'utrecht': ('Heuvelrug, veenweide en uiterwaarden',
                'Van de bospaden op de Utrechtse Heuvelrug tot de veenweiden in het westen en de uiterwaarden langs de Lek: in de provincie Utrecht is de grond na regen vaak zacht.',
                ['Bospaden op de Heuvelrug', 'Veenweidebermen langs polderwegen', 'Uiterwaarden en dijkwegen']),
    'zeeland': ('strand, dijken en klei',
                'Zeeland combineert stranden en strandopgangen met kleiakkers en smalle dijkwegen. In de zomer wordt bij de kust vaak op gras geparkeerd, en dat gaat na een onweersbui snel mis.',
                ['Strand en strandopgangen', 'Bermen langs dijkwegen', 'Parkeren op gras bij campings en de kust']),
    'zuid-holland': ('veenweide, duinen en strand',
                     'In Zuid-Holland ligt veel veenweide met natte bermen langs smalle polderwegen, en aan de kust duinen en strand waar auto\'s zich in het mulle zand vastrijden.',
                     ['Natte bermen langs polderwegen', 'Strand en duinovergangen', 'Weilanden bij evenementen']),
}

# beeld: (bestand, alt, maker, licentie, licentie-url, bron-url, titel)
BEELD = {
    'bmw-modder': ('BMW X5 tot over de wielen weggezakt in de modder', 'Joost J. Bakker', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/', 'https://commons.wikimedia.org/wiki/File:BMW_X_5_car_bogged_down.jpg', 'BMW X 5 car bogged down'),
    'festival-passat': ('Personenauto vast in de modder op een parkeerweiland', 'Stephen West', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/', 'https://commons.wikimedia.org/wiki/File:Volkswagen_Passat_stuck_in_mud_at_Isle_of_Wight_Festival_2012.jpg', 'Volkswagen Passat stuck in mud'),
    'trekker-avond': ('Trekker op een modderig parkeerterrein in de avond', 'Stephen West', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/', 'https://commons.wikimedia.org/wiki/File:Tractor_pulling_car_through_mud_at_Isle_of_Wight_Festival_2012.jpg', 'Tractor pulling car through mud'),
    'trekker-uittrekken': ('Auto wordt door de modder getrokken', 'Stephen West', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/', 'https://commons.wikimedia.org/wiki/File:Tractor_pulling_car_through_mud_at_Isle_of_Wight_Festival_2012_4.jpg', 'Tractor pulling car through mud (4)'),
    'wad-auto': ('Auto vastgereden in de natte modder van het wad', 'Charlie, Verenigd Koninkrijk', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/', 'https://commons.wikimedia.org/wiki/File:Oh_dear........._(12568437524).jpg', 'Oh dear'),
    'wad-wiel': ('Voorwiel weggezakt in natte modder', 'Charlie, Verenigd Koninkrijk', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/', "https://commons.wikimedia.org/wiki/File:You're_not_a_boat!_(12568118423).jpg", "You're not a boat!"),
    'sneeuw-a38': ('Auto vast in de sneeuw langs een weg', 'Richard Park', 'CC BY-SA 2.0', 'https://creativecommons.org/licenses/by-sa/2.0/', 'https://commons.wikimedia.org/wiki/File:A38_at_Barrow_Fountain_-_car_stuck_in_snow_-_geograph.org.uk_-_6773608.jpg', 'A38 at Barrow Fountain, car stuck in snow'),
    'defender-berm': ('Terreinwagen in een modderige berm', 'AliV', 'CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0/', 'https://commons.wikimedia.org/wiki/File:Land_Rover_Defender_covered_with_mud_after_driving_in_rough_terrain.jpg', 'Land Rover Defender covered with mud'),
    'discovery-band': ('Terreinwagen vol modder met een bergingsband op de motorkap', 'Paul Bryan', 'CC BY-SA 2.0', 'https://creativecommons.org/licenses/by-sa/2.0/', 'https://commons.wikimedia.org/wiki/File:Heavily_mud-spattered_Land_Rover_Discovery,_Winchmore_Hill_-_geograph.org.uk_-_5081807.jpg', 'Heavily mud-spattered Land Rover Discovery'),
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
NAV = [('', 'Home', 'home'), ('situaties.html', 'Situaties', 'situaties'), ('hulp-aanvragen.html', 'Hulp aanvragen', 'hulp'),
       ('werkgebied/', 'Werkgebied', 'werkgebied'), ('veelgestelde-vragen.html', 'Vragen', 'vragen'), ('contact.html', 'Contact', 'contact')]


def header(r, pagina):
    links = ''.join(f'<a href="{r}{u}"' + (' aria-current="page"' if k == pagina else '') + f'>{t}</a>' for u, t, k in NAV)
    mlinks = ''.join(f'<a href="{r}{u}">{t}</a>' for u, t, k in NAV)
    return (f'<a class="skip" href="#main">Direct naar de inhoud</a>\n'
            f'<header class="hdr"><div class="wrap hdr__in">{logo(r)}'
            f'<nav class="nav" aria-label="Hoofdmenu">{links}</nav>'
            f'<div class="hdr__knop"><a class="btn btn--wa" href="{wa("Hallo, mijn auto staat vast.")}">{icon("wa")}WhatsApp</a>'
            f'<a class="btn" href="tel:{C["telefoonLink"]}">{icon("tel")}{TELNR}</a></div>'
            f'<button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav">{icon("menu")}</button></div></header>\n'
            f'<nav class="mnav" id="mnav" aria-label="Menu">{mlinks}'
            f'<a class="btn btn--vol btn--groot" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel {TELNR}</a>'
            f'<a class="btn btn--wa btn--vol btn--groot" href="{wa("Hallo, mijn auto staat vast.")}">{icon("wa")}WhatsApp</a></nav>\n'
            f'<div class="belbalk"><a class="btn" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel direct</a>'
            f'<a class="btn btn--wa" href="{wa("Hallo, mijn auto staat vast.")}">{icon("wa")}WhatsApp</a></div>\n')


def footer(r):
    provs = ''.join(f'<li><a href="{r}werkgebied/{p["slug"]}/">{E(p["naam"])}</a></li>' for p in PROVINCIES.values())
    return (f'<footer class="ftr"><div class="wrap"><div class="ftr__grid">'
            f'<div>{logo(r)}<p>Vastgereden in modder, zand of sneeuw? Wij komen met een terreinwagen, lier en bergingsbanden naar u toe en trekken uw auto los.</p>'
            f'<p class="ftr__adres">{E(C["bedrijf"])}<br>{E(C["straat"])}<br>{E(C["postcode"])} {E(C["plaats"])}<br>KvK {E(C["kvk"])}</p></div>'
            f'<div><h2 class="ftr__kop">Situaties</h2><ul>'
            f'<li><a href="{r}situaties.html#modder">Vast in de modder</a></li><li><a href="{r}situaties.html#weiland">Weiland en festival</a></li>'
            f'<li><a href="{r}situaties.html#strand">Strand en wad</a></li><li><a href="{r}situaties.html#berm">Berm en greppel</a></li>'
            f'<li><a href="{r}situaties.html#sneeuw">Sneeuw en ijzel</a></li><li><a href="{r}situaties.html#camper">Camper en caravan</a></li></ul></div>'
            f'<div><h2 class="ftr__kop">Werkgebied</h2><ul class="ftr__provs">{provs}</ul></div>'
            f'<div><h2 class="ftr__kop">Contact</h2><ul><li><a href="tel:{C["telefoonLink"]}">{TELNR}</a></li>'
            f'<li><a href="{wa()}">WhatsApp</a></li><li><a href="{r}hulp-aanvragen.html">Hulp aanvragen</a></li>'
            f'<li><a href="{r}veelgestelde-vragen.html">Veelgestelde vragen</a></li><li><a href="{r}contact.html">Contact</a></li></ul></div>'
            f'</div><div class="ftr__onder"><span>&copy; {time.strftime("%Y")} {E(C["naam"])} · {E(C["bedrijf"])} · KvK {E(C["kvk"])}</span>'
            f'<span><a href="{r}privacy.html">Privacy</a><a href="{r}beeldverantwoording.html">Beeldverantwoording</a></span></div></div></footer>\n')


def cta(r, titel='Vastgereden?', tekst='Bel of app ons direct. We zeggen eerlijk wanneer we er kunnen zijn.', plaats=''):
    msg = 'Hallo, mijn auto staat vast' + (f' in {plaats}' if plaats else '') + '.'
    return (f'<section class="wrap" style="margin-top:clamp(64px,9vw,120px)"><div class="cta rv"><div><h2>{titel}</h2><p>{tekst}</p></div>'
            f'<div><a class="cta__tel" href="tel:{C["telefoonLink"]}">{TELNR}</a><div class="cta__knoppen">'
            f'<a class="btn btn--groot" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel direct</a>'
            f'<a class="btn btn--wa btn--groot" href="{wa(msg)}">{icon("wa")}WhatsApp</a></div></div></div></section>\n')


def bedrijf_schema():
    s = {'@context': 'https://schema.org', '@type': 'AutomotiveBusiness', '@id': DOMEIN + '/#bedrijf', 'name': C['naam'],
         'description': 'Hulp bij een vastgereden auto in modder, zand, sneeuw of de berm. Wij trekken uw auto los, in heel Nederland.',
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
    knop = (f'<a class="wa-knop" href="{wa("Hallo, mijn auto staat vast.")}" aria-label="Stuur ons een WhatsApp-bericht">'
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
    msg = 'Hallo, mijn auto staat vast' + (f' in {plaats}' if plaats else '') + '.'
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
SITUATIES = [
    ('modder', 'Vast in de modder', 'bmw-modder',
     'Wielen die doorslaan en een auto die steeds dieper wegzakt: in natte klei of modder komt u op eigen kracht vaak niet meer los.',
     'Modder is verraderlijk. Hoe langer de wielen doordraaien, hoe dieper de auto zakt, tot de bodemplaat op de grond rust en de wielen geen gewicht meer dragen. Wij trekken de auto rustig en recht terug naar vaste grond, met een bergingsband aan het trekoog en waar nodig met de lier.',
     ['Personenauto\'s, SUV\'s en bestelbussen', 'Ook als de auto tot de as is weggezakt', 'Rustig en recht trekken, zonder rukken aan de auto']),
    ('weiland', 'Weiland, festival en evenement', 'festival-passat',
     'Parkeren op gras gaat goed tot het gaat regenen. Bij festivals, bruiloften, open dagen en evenementen staan dan tientallen auto\'s vast.',
     'Een parkeerweiland verandert na een bui in een modderbad. Wij helpen losse bezoekers, maar ook organisatoren die meerdere auto\'s van het terrein willen hebben. Bel ons vooraf als u een evenement organiseert en het weer omslaat: dan kunnen we afspreken wanneer we klaarstaan.',
     ['Losse bezoekers op een parkeerweiland', 'Organisatoren met meerdere vastgereden auto\'s', 'Afspraken vooraf als er regen wordt verwacht']),
    ('strand', 'Strand, duin en wad', 'wad-auto',
     'Mul zand bij een strandopgang of natte slik bij laagwater: wie daar vastrijdt, wil snel weg voordat het tij of de drukte komt.',
     'In los zand graaft een auto zich razendsnel in. Op slik of wad speelt bovendien het tij mee. Wij komen met zandplaten en bergingsbanden en halen de auto terug naar vaste grond. Staat het water al bij de wielen, bel dan meteen en blijf zelf op een veilige plek.',
     ['Strandopgangen en strandparkeren', 'Duinpaden en mul zand', 'Slik en wad bij laagwater: bel zo vroeg mogelijk']),
    ('berm', 'Berm en greppel', 'defender-berm',
     'Even uitwijken voor een tegenligger en het wiel zakt weg in de zachte berm. Of de auto glijdt half de greppel in.',
     'Een auto die scheef in de berm of greppel staat, trekken we gecontroleerd terug op de weg. Op een doorgaande weg zetten we de werkplek af en werken we zo kort mogelijk naast het verkeer. Ligt de auto in een sloot met water, dan is er meestal een kraanwagen nodig. Dat zeggen we u dan eerlijk.',
     ['Wiel in de zachte berm', 'Auto scheef in een droge greppel', 'Veilig werken naast het verkeer']),
    ('sneeuw', 'Sneeuw en ijzel', 'sneeuw-a38',
     'Een helling op die niet lukt, een oprit vol sneeuw of een auto die op ijzel van de weg is gegleden: in de winter staan auto\'s overal vast.',
     'Bij sneeuw en ijzel draaien de wielen zonder grip, en elke poging om weg te rijden maakt de ondergrond gladder. Wij trekken de auto los en zetten hem terug op een plek waar u weer grip heeft. Bij gladheid zijn we druk: bel of app op tijd, dan plannen we u zo snel mogelijk in.',
     ['Vast op een helling, oprit of parkeerplaats', 'Van de weg gegleden in de sneeuw', 'Winterse drukte: bel of app op tijd']),
    ('camper', 'Camper, caravan en aanhanger', 'trekker-uittrekken',
     'Een camper op een natte camping, een caravan op het gras of een auto met aanhanger die het talud niet op komt.',
     'Zwaardere combinaties vragen om een andere aanpak. Soms koppelen we de caravan of aanhanger eerst los, soms trekken we het geheel in één keer naar vaste grond. Vertel ons vooraf het type en ongeveer het gewicht, dan komen we met het juiste materiaal.',
     ['Campers op een natte camping of standplaats', 'Caravans en aanhangers op gras', 'Geef type en gewicht door, dan komen we goed voorbereid']),
]

ALGEMENE_VRAGEN = [
    ('Hoe snel kunnen jullie er zijn?', 'Dat hangt af van waar u staat en hoe druk het is, bijvoorbeeld bij sneeuw of na een regenachtig festivalweekend. Bij uw melding zeggen we eerlijk hoe laat we er kunnen zijn.'),
    ('Wat kost het om mijn auto los te trekken?', 'Dat hangt af van de afstand, de situatie en hoe diep de auto vastzit. U hoort de prijs voordat we beginnen, zodat u niet voor verrassingen komt te staan.'),
    ('Kan mijn auto beschadigd raken?', 'We bevestigen de bergingsband aan het trekoog of de bergingspunten van uw auto, nooit aan de bumper of de wielophanging, en trekken rustig en recht. Bij een auto die heel diep vastzit kan er altijd modder of druk op een bumper of de bodem komen. Zien we een risico, dan bespreken we dat met u voordat we trekken.'),
    ('Moet ik lid zijn van een pechhulpdienst?', 'Nee. Iedereen kan ons bellen of appen, u hoeft nergens lid van te zijn en er is geen abonnement nodig.'),
    ('Welke voertuigen kunnen jullie lostrekken?', 'Personenauto\'s, SUV\'s en terreinwagens, bestelbussen, campers en auto\'s met een caravan of aanhanger. Gaat het om een vrachtwagen of zwaar landbouwvoertuig, vraag het ons dan even: soms is daar ander materieel voor nodig.'),
    ('Wat moet ik doorgeven als ik vastzit?', 'Uw locatie (het liefst via GPS of WhatsApp), het type voertuig, waar u in vastzit (modder, gras, zand, sneeuw of berm) en hoe diep. Een foto helpt ons enorm om met het juiste materiaal te komen.'),
    ('Wat als mijn auto in een sloot met water ligt?', 'Zijn er mensen in gevaar, bel dan eerst 112. Ligt de auto in het water of op zijn kant, dan is er meestal een kraanwagen nodig. Wij zeggen u dan eerlijk of wij kunnen helpen of dat een bergingsbedrijf met kraan sneller is.'),
    ('Helpen jullie ook organisatoren van evenementen?', 'Ja. Organiseert u een festival, bruiloft of open dag met parkeren op gras en slaat het weer om? Bel ons vooraf, dan spreken we af wanneer we klaarstaan om vastgereden auto\'s van het terrein te halen.'),
    ('Wat doe ik zolang ik op jullie wacht?', 'Stop met gas geven, zet de wielen recht en schroef het trekoog alvast in als u weet waar het zit (meestal bij het reservewiel of de krik). Staat u langs een doorgaande weg, zet dan de alarmlichten aan en wacht op een veilige plek, niet vlak naast de auto.'),
    ('Hoe betaal ik?', 'Na afloop betaalt u ter plekke met de pin, of op factuur als u zakelijk klant bent.'),
]


def pagina_home():
    r = ''
    sit_kaarten = ''
    for i, (sid, titel, beeld, kort, *_rest) in enumerate(SITUATIES[:5]):
        breed = ' situatie--breed' if i == 0 else ''
        sit_kaarten += (f'<a class="situatie rv{breed}" href="situaties.html#{sid}">{img(r, beeld, "(max-width: 640px) 100vw, (max-width: 960px) 50vw, 33vw")}'
                        f'<div class="situatie__tekst"><h3>{titel}</h3><p>{kort}</p><span class="pijl">Zo helpen wij {icon("pijl")}</span></div></a>')
    body = f'''<section class="hero">
  <div class="hero__beeld">{img(r, 'bmw-modder', '100vw', lui=False, alt='')}</div>
  <div class="wrap"><div class="hero__in">
    <span class="boven">Vastgereden in modder, zand of sneeuw</span>
    <h1>Vast in de modder? <em>Wij trekken u los.</em></h1>
    <p class="lead">Doorslaande wielen op een nat weiland, een wiel in de berm of vast in de sneeuw: wij komen met een terreinwagen, lier en bergingsbanden naar u toe en trekken uw auto zorgvuldig los.</p>
    <div class="hero__knoppen">
      <a class="btn btn--groot" href="tel:{C['telefoonLink']}">{icon('tel')}Bel {TELNR}</a>
      <a class="btn btn--wa btn--groot" href="{wa('Hallo, mijn auto staat vast.')}">{icon('wa')}WhatsApp</a>
      <a class="btn btn--rand btn--groot" href="hulp-aanvragen.html">Hulp aanvragen</a>
    </div>
    <ul class="hero__punten"><li>{icon('pin')}In heel Nederland</li><li>{icon('auto')}Auto, bus, camper en caravan</li><li>{icon('vink')}Prijs vooraf</li></ul>
  </div></div>
  <span class="hero__bron">Foto: Joost J. Bakker, CC BY 2.0</span>
</section>
<div class="strip"><div class="strip__in"><span>Modder</span><span>Weiland</span><span>Strand en wad</span><span>Berm</span><span>Sneeuw en ijzel</span></div></div>

<section class="sec">
  <div class="wrap">
    <div class="kop rv"><div><span class="boven">Situaties</span><h2>Waar wij u uit halen</h2></div>
      <p class="lead">Van een parkeerweiland na een regenbui tot een auto die tot de as in de klei staat. Elke situatie vraagt een andere aanpak, en die kennen we.</p></div>
    <div class="situaties">{sit_kaarten}</div>
  </div>
</section>

<section class="sec sec--wit">
  <div class="wrap">
    <div class="kop rv"><div><span class="boven">Werkwijze</span><h2>Zo trekken wij u los</h2></div>
      <p class="lead">Geen geforceerd getrek aan uw auto, maar een rustige, vaste aanpak die we bij elke klus volgen.</p></div>
    <div class="aanpak rv">
      <div class="stap"><b>01</b><h3>Bel of app</h3><p>Deel uw locatie, het type auto en waar u in vastzit. Een foto helpt ons om met het juiste materiaal te komen.</p></div>
      <div class="stap"><b>02</b><h3>Wij komen eraan</h3><p>Met een terreinwagen, lier, bergingsbanden en zandplaten. U hoort vooraf hoe laat we er zijn en wat het kost.</p></div>
      <div class="stap"><b>03</b><h3>Losgetrokken</h3><p>We bevestigen de band aan het trekoog en trekken rustig en recht, tot uw auto weer op vaste grond staat.</p></div>
      <div class="stap"><b>04</b><h3>Weer op weg</h3><p>We lopen samen de auto na en wijzen u de veiligste route terug naar de verharde weg.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap twee">
    <figure class="foto foto--hoog rv" style="margin:0">{img(r, 'wad-wiel', '(max-width: 960px) 100vw, 50vw')}<figcaption>Foto: Charlie, CC BY 2.0</figcaption></figure>
    <div class="rv">
      <span class="boven">Vastgereden?</span>
      <h2>Dit doet u beter wel en niet</h2>
      <p class="lead" style="margin-top:16px">De eerste minuten bepalen vaak hoe diep de auto uiteindelijk vastzit. Met deze vijf punten maakt u het niet erger.</p>
      <ul class="regels">
        <li class="niet"><i>{icon('kruis')}</i><div><b>Blijf niet gas geven</b><span>Doordraaiende wielen graven zich dieper in en de koppeling en banden worden heet.</span></div></li>
        <li class="niet"><i>{icon('kruis')}</i><div><b>Niemand achter een draaiend wiel</b><span>Laat niemand duwen achter of naast een wiel dat doorslaat: modder en stenen schieten weg.</span></div></li>
        <li class="wel"><i>{icon('vink')}</i><div><b>Zet de wielen recht</b><span>Met rechte wielen komt de auto het makkelijkst los, ook als wij straks trekken.</span></div></li>
        <li class="wel"><i>{icon('vink')}</i><div><b>Zoek het trekoog alvast op</b><span>Het ligt meestal bij het reservewiel of de krik en schroeft u voor of achter in de bumper.</span></div></li>
        <li class="wel"><i>{icon('vink')}</i><div><b>Langs een doorgaande weg? Veiligheid eerst</b><span>Zet de alarmlichten aan en wacht op een veilige plek, niet vlak naast de auto.</span></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--donker">
  <div class="wrap gebied">
    <div class="rv">
      <span class="boven">Werkgebied</span>
      <h2>Overal in Nederland</h2>
      <p class="lead" style="margin-top:16px">Van de zandwegen in Drenthe tot de stranden in Zeeland en de polderklei in Flevoland: wij komen naar u toe, in alle 342 gemeenten van Nederland.</p>
      <div class="hero__knoppen" style="margin-top:28px"><a class="btn" href="tel:{C['telefoonLink']}">{icon('tel')}Bel {TELNR}</a><a class="btn btn--rand" href="werkgebied/">Bekijk alle gemeenten</a></div>
    </div>
    <figure class="foto foto--breed rv" style="margin:0">{img(r, 'trekker-avond')}<figcaption>Foto: Stephen West, CC BY 2.0</figcaption></figure>
  </div>
  <div class="wrap rv" style="margin-top:clamp(40px,5vw,64px)">{provkaarten(r)}</div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="kop kop--midden rv"><div><span class="boven">Veelgestelde vragen</span><h2>Goed om te weten</h2></div></div>
    <div class="rv">{faq(ALGEMENE_VRAGEN[:6])}</div>
    <p style="text-align:center;margin:28px 0 0"><a class="pijl" href="veelgestelde-vragen.html">Alle vragen bekijken {icon('pijl')}</a></p>
  </div>
</section>
{cta(r)}'''
    schrijf('', r, 'Auto vast in de modder? Wij trekken u los | Lostrek',
            'Vastgereden in modder, zand, sneeuw of de berm? Lostrek trekt uw auto zorgvuldig los, in heel Nederland. Bel of app 085 744 4166.',
            'home', body, prioriteit='1.0')


def pagina_situaties():
    r = ''
    rijen = ''
    for sid, titel, beeld, kort, lang, punten in SITUATIES:
        maker = BEELD[beeld][1]; lic = BEELD[beeld][2]
        rijen += (f'<div class="sit-rij" id="{sid}"><figure class="foto foto--breed rv" style="margin:0">{img(r, beeld)}<figcaption>Foto: {E(maker)}, {lic}</figcaption></figure>'
                  f'<div class="rv"><h2>{titel}</h2><p class="lead">{kort}</p><p>{lang}</p>{vinkjes(punten)}'
                  f'<div class="hero__knoppen" style="margin-top:26px"><a class="btn" href="hulp-aanvragen.html?ondergrond={quote(ONDERGROND_VOOR[sid])}">Hulp aanvragen</a>'
                  f'<a class="btn btn--licht" href="tel:{C["telefoonLink"]}">Bel {TELNR}</a></div></div></div>')
    body = (pkop(r, 'Situaties waarin wij u lostrekken', 'Modder, gras, zand, sneeuw of een zachte berm: elke ondergrond vraagt een eigen aanpak. Hieronder leest u hoe wij te werk gaan en waar u op kunt letten.',
                 'festival-passat', [('Home', ''), ('Situaties', 'situaties.html')])
            + f'<section class="sec" style="padding-top:clamp(24px,4vw,48px)"><div class="wrap">{rijen}</div></section>\n' + cta(r))
    schrijf('situaties.html', r, 'Auto vast in modder, zand of sneeuw: zo helpen wij | Lostrek',
            'Vast in de modder, op een weiland, het strand, in de berm of de sneeuw? Lees hoe Lostrek uw auto, camper of caravan zorgvuldig lostrekt.',
            'situaties', body, [('Home', '/'), ('Situaties', '/situaties.html')], prioriteit='0.9')


ONDERGROND_VOOR = {'modder': 'Modder', 'weiland': 'Gras of weiland', 'strand': 'Zand of strand', 'berm': 'Berm of greppel', 'sneeuw': 'Sneeuw of ijs', 'camper': 'Gras of weiland'}


def keuzes(naam, opties):
    return '<div class="keuzes">' + ''.join(f'<label class="keuze"><input type="radio" name="{naam}" value="{E(o)}"><span>{E(o)}</span></label>' for o in opties) + '</div>'


def pagina_hulp():
    r = ''
    body = (pkop(r, 'Hulp aanvragen', 'Vul in wat u weet en verstuur alles in één WhatsApp-bericht. Hoe meer we vooraf weten, hoe beter we voorbereid komen. Liever direct iemand spreken? Bel '
                 f'<a href="tel:{C["telefoonLink"]}">{TELNR}</a>.', 'wad-auto', [('Home', ''), ('Hulp aanvragen', 'hulp-aanvragen.html')], knoppen=False)
            + f'''<section class="sec" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap">
<div class="melder" data-melder>
  <div class="melder__links">
    <fieldset class="vraag"><legend><i>1</i>Waar staat u vast?</legend>{keuzes('ondergrond', ['Modder', 'Gras of weiland', 'Zand of strand', 'Sneeuw of ijs', 'Berm of greppel'])}</fieldset>
    <fieldset class="vraag"><legend><i>2</i>Welk voertuig?</legend>{keuzes('voertuig', ['Personenauto', 'SUV of terreinwagen', 'Bestelbus', 'Camper', 'Auto met caravan of aanhanger'])}</fieldset>
    <fieldset class="vraag"><legend><i>3</i>Aandrijving</legend>{keuzes('aandrijving', ['Voorwiel', 'Achterwiel', 'Vierwiel', 'Weet ik niet'])}</fieldset>
    <fieldset class="vraag"><legend><i>4</i>Hoe vast staat de auto?</legend>{keuzes('vast', ['Wielen slaan door', 'Tot de as weggezakt', 'Scheef in de berm of greppel', 'Komt niet van zijn plek'])}</fieldset>
    <div class="vraag"><p class="vraag__titel"><i>5</i>Waar bent u?</p>
      <div class="veld"><label for="locatie">Plaats, straat of herkenningspunt</label>
        <div class="locatie"><input class="inp" id="locatie" name="locatie" type="text" autocomplete="off" placeholder="Bijvoorbeeld: weiland achter de Dorpsstraat, Lunteren"><button class="btn btn--donker" type="button" data-locatie>{icon('pin')}Mijn locatie</button></div>
        <span class="veld__fout">Vul uw locatie in of deel uw GPS-locatie, dan weten we waar we moeten zijn.</span>
        <p class="locatie__status" data-locatie-status aria-live="polite"></p></div>
    </div>
    <div class="vraag"><p class="vraag__titel"><i>6</i>Uw gegevens</p>
      <div class="velden">
        <div class="veld"><label for="naam">Naam</label><input class="inp" id="naam" name="naam" type="text" autocomplete="name"></div>
        <div class="veld"><label for="telefoon">Telefoon</label><input class="inp" id="telefoon" name="telefoon" type="tel" autocomplete="tel" inputmode="tel"></div>
        <div class="veld"><label for="kenteken">Kenteken (als u het weet)</label><input class="inp" id="kenteken" name="kenteken" type="text" autocomplete="off" spellcheck="false"></div>
        <div class="veld veld--vol"><label for="toelichting">Toelichting</label><textarea class="inp" id="toelichting" name="toelichting" placeholder="Bijvoorbeeld: helling op, aanhanger zit vast, er staat water bij de wielen"></textarea></div>
      </div>
    </div>
  </div>
  <div class="melder__rechts">
    <h2>Uw bericht</h2>
    <pre class="bericht" data-bericht aria-live="polite"></pre>
    <a class="btn btn--wa btn--vol btn--groot" data-verstuur href="{wa()}">{icon('wa')}Verstuur via WhatsApp</a>
    <a class="btn btn--licht btn--vol" href="tel:{C['telefoonLink']}">{icon('tel')}Of bel {TELNR}</a>
    <p class="melder__noot">Stuur na het bericht een foto van de auto en de ondergrond via WhatsApp. Uw gegevens gebruiken we alleen om u te helpen, zie onze <a href="privacy.html">privacyverklaring</a>.</p>
  </div>
</div>
</div></section>
''' + cta(r, 'Liever direct bellen?', 'Dan helpen we u telefonisch verder en sturen we iemand naar u toe.'))
    schrijf('hulp-aanvragen.html', r, 'Hulp aanvragen bij een vastgereden auto | Lostrek',
            'Vastgereden? Vul in waar u vastzit, deel uw locatie en verstuur alles via WhatsApp naar Lostrek. Of bel direct 085 744 4166.',
            'hulp', body, [('Home', '/'), ('Hulp aanvragen', '/hulp-aanvragen.html')], prioriteit='0.9')


def pagina_vragen():
    r = ''
    body = (pkop(r, 'Veelgestelde vragen', 'Wat kost het, hoe snel zijn we er en wat doet u zolang u wacht? Hier vindt u de antwoorden. Staat uw vraag er niet bij, bel of app ons gerust.',
                 'discovery-band', [('Home', ''), ('Veelgestelde vragen', 'veelgestelde-vragen.html')])
            + f'<section class="sec"><div class="wrap">{faq(ALGEMENE_VRAGEN)}</div></section>\n' + cta(r))
    schrijf('veelgestelde-vragen.html', r, 'Veelgestelde vragen over een vastgereden auto | Lostrek',
            'Wat kost het om uw auto los te laten trekken, hoe snel zijn we er en wat doet u zolang u wacht? Antwoorden op de meestgestelde vragen.',
            'vragen', body, [('Home', '/'), ('Veelgestelde vragen', '/veelgestelde-vragen.html')], prioriteit='0.7')


def pagina_contact():
    r = ''
    tijden = ''.join(f'<li><span>{E(d)}</span><b>{E(t)}</b></li>' for d, t in C['openingstijden'])
    email = f'<li><span>E-mail</span><b><a href="mailto:{E(C["email"])}">{E(C["email"])}</a></b></li>' if C['email'] else ''
    body = (pkop(r, 'Neem direct contact op', 'Staat u vast? Bellen of appen is het snelst. Voor een vraag, een afspraak voor een evenement of zakelijke afspraken kunt u ons ook bellen of een WhatsApp sturen.',
                 'trekker-avond', [('Home', ''), ('Contact', 'contact.html')])
            + f'''<section class="sec"><div class="wrap kaarten">
  <div class="kaart"><h2 style="font-size:1.6rem;margin-bottom:12px">Bedrijfsgegevens</h2><ul class="rij-lijst">
    <li><span>Telefoon</span><b><a href="tel:{C['telefoonLink']}">{TELNR}</a></b></li>
    <li><span>WhatsApp</span><b><a href="{wa()}">Stuur een bericht</a></b></li>{email}
    <li><span>Werkgebied</span><b>Heel Nederland</b></li>
    <li><span>Bedrijf</span><b>{E(C['bedrijf'])}</b></li>
    <li><span>Adres</span><b>{E(C['straat'])}<br>{E(C['postcode'])} {E(C['plaats'])}</b></li>
    <li><span>KvK</span><b>{E(C['kvk'])}</b></li></ul></div>
  <div class="kaart"><h2 style="font-size:1.6rem;margin-bottom:12px">Bereikbaarheid</h2><ul class="rij-lijst">{tijden}</ul>
    <p class="zacht" style="margin:14px 0 0;color:var(--zacht)">Bij sneeuw, ijzel of na een nat festivalweekend is het druk. Bel of app dan op tijd, dan plannen we u zo snel mogelijk in.</p></div>
  <div class="kaart kaart--donker"><h2 style="font-size:1.6rem;margin-bottom:12px;color:#fff">Vastgereden?</h2><p>Geef door waar u vastzit en deel uw locatie. Dan komen we met het juiste materiaal.</p>
    <a class="btn btn--vol" href="hulp-aanvragen.html">Hulp aanvragen</a><a class="btn btn--wa btn--vol" href="{wa('Hallo, mijn auto staat vast.')}">{icon('wa')}WhatsApp</a></div>
</div></section>
''' + cta(r))
    schrijf('contact.html', r, 'Contact | Lostrek', 'Bel of app Lostrek op 085 744 4166 als uw auto vastzit in modder, zand of sneeuw. Lostrek is een handelsnaam van D&D Mobiliteit B.V.',
            'contact', body, [('Home', '/'), ('Contact', '/contact.html')], prioriteit='0.6')


def pagina_privacy():
    r = ''
    body = (pkop(r, 'Privacyverklaring', 'Wij gaan zorgvuldig met uw gegevens om. Hieronder leest u welke gegevens wij gebruiken, waarvoor en hoe lang.', None, [('Home', ''), ('Privacy', 'privacy.html')], knoppen=False)
            + f'''<section class="sec"><div class="wrap tekstpagina">
<h2>Wie zijn wij</h2><p>{E(C['naam'])} is een handelsnaam van {E(C['bedrijf'])}, gevestigd aan de {E(C['straat'])}, {E(C['postcode'])} {E(C['plaats'])}, ingeschreven bij de Kamer van Koophandel onder nummer {E(C['kvk'])}. Wij zijn verantwoordelijk voor de verwerking van uw gegevens zoals beschreven in deze verklaring.</p>
<h2>Welke gegevens wij gebruiken</h2><p>Als u ons belt, een WhatsApp-bericht stuurt of het formulier op deze website gebruikt, ontvangen wij de gegevens die u zelf doorgeeft: uw naam, telefoonnummer, locatie, kenteken, gegevens over uw voertuig en eventuele foto's.</p>
<h2>Het formulier op deze website</h2><p>Het formulier stelt een WhatsApp-bericht voor u op. Er wordt niets via deze website opgeslagen of verstuurd: pas als u zelf op versturen tikt, gaat het bericht via WhatsApp naar ons. Uw GPS-locatie wordt alleen opgehaald als u daar zelf op tikt en uw browser toestemming geeft.</p>
<h2>Waarvoor</h2><p>Wij gebruiken uw gegevens om u te helpen, contact met u op te nemen, de klus uit te voeren en te factureren. Wij verkopen uw gegevens niet en delen ze alleen als dat nodig is voor de uitvoering, bijvoorbeeld met onze boekhouder, of als de wet ons daartoe verplicht.</p>
<h2>Hoe lang</h2><p>Gegevens voor de facturatie bewaren wij zeven jaar, omdat de wet dat vraagt. Overige gegevens verwijderen wij zodra ze niet meer nodig zijn.</p>
<h2>Cookies en statistieken</h2><p>Deze website plaatst geen trackingcookies en gebruikt geen advertentienetwerken.</p>
<h2>Uw rechten</h2><p>U kunt ons altijd vragen welke gegevens wij van u hebben, en vragen om ze te verbeteren of te verwijderen. Neem daarvoor contact op via {TELNR}. Bent u het niet eens met hoe wij met uw gegevens omgaan, dan kunt u een klacht indienen bij de Autoriteit Persoonsgegevens.</p>
</div></section>
''')
    schrijf('privacy.html', r, 'Privacyverklaring | Lostrek', 'Lees hoe Lostrek, een handelsnaam van D&D Mobiliteit B.V., omgaat met uw gegevens.',
            'privacy', body, [('Home', '/'), ('Privacy', '/privacy.html')], prioriteit='0.2')


def pagina_beeld():
    r = ''
    rijen = ''.join(f'<tr><td><img src="assets/img/{n}-640.webp" alt="" loading="lazy" width="96" height="64"></td><td><b>{E(b[5])}</b></td><td>{E(b[1])}</td>'
                    f'<td><a href="{b[3]}" rel="noopener">{b[2]}</a></td><td><a href="{E(b[4])}" rel="noopener">Bron</a></td></tr>\n' for n, b in BEELD.items())
    body = (pkop(r, 'Beeldverantwoording', 'De foto\'s op deze website zijn echte situaties, gedeeld onder een Creative Commons-licentie. Hieronder staan per foto de maker, de licentie en de bron. Waar nodig is de foto bijgesneden.',
                 None, [('Home', ''), ('Beeldverantwoording', 'beeldverantwoording.html')], knoppen=False)
            + f'<section class="sec"><div class="wrap"><div class="tabelwrap"><table class="credits"><thead><tr><th><span class="sr">Foto</span></th><th>Titel</th><th>Maker</th><th>Licentie</th><th>Bron</th></tr></thead>\n<tbody>{rijen}</tbody></table></div>'
            f'<p style="margin-top:20px;color:var(--zacht)">Lettertype: Barlow en Barlow Condensed van Jeremy Tribby, onder de SIL Open Font License.</p></div></section>\n')
    schrijf('beeldverantwoording.html', r, 'Beeldverantwoording | Lostrek', 'Makers, licenties en bronnen van de foto\'s op de website van Lostrek.',
            'beeld', body, [('Home', '/'), ('Beeldverantwoording', '/beeldverantwoording.html')], prioriteit='0.1')


def pagina_404():
    r = '/'
    body = (f'<section class="pkop"><div class="wrap"><div class="pkop__in"><h1>Deze pagina bestaat niet</h1>'
            f'<p class="lead">De link klopt niet meer, of er zit een typfout in het adres. Staat u vast? Bel of app ons direct.</p>'
            f'<div class="hero__knoppen" style="margin-top:28px"><a class="btn btn--groot" href="tel:{C["telefoonLink"]}">{icon("tel")}Bel {TELNR}</a>'
            f'<a class="btn btn--wa btn--groot" href="{wa("Hallo, mijn auto staat vast.")}">{icon("wa")}WhatsApp</a>'
            f'<a class="btn btn--rand btn--groot" href="/">Naar de homepage</a></div></div></div></section>\n')
    schrijf('404.html', r, 'Pagina niet gevonden | Lostrek', 'Deze pagina bestaat niet. Staat u vast? Bel of app Lostrek op 085 744 4166.', '404', body, noindex=True)


INTRO = [
    'Staat uw auto vast in {G}? Door modder, een nat weiland, zand of sneeuw komt u niet meer op eigen kracht weg. Bel of app ons: we komen naar uw locatie in de gemeente {G} en trekken uw auto zorgvuldig los.',
    'Vastgereden in {G}? Wij komen met een terreinwagen, lier en bergingsbanden naar u toe, waar in de gemeente {G} u ook staat: op een weiland, in de berm of op een onverharde weg.',
    'Een wiel in de berm, doorslaande wielen op het gras of vast in de sneeuw: in {G} en omgeving trekken wij uw auto los en zetten we hem terug op vaste grond.',
    'Zit uw auto vast in de modder in {G}? Stop met gas geven en bel of app ons. Wij komen naar u toe in heel {P} en halen uw auto rustig en recht terug naar de verharde weg.',
]


def gemeente_pagina(i, g):
    r = '../../'
    G, P = g['naam'], g['prov']
    land, land_tekst, plekken = LANDSCHAP[g['prov_slug']]
    kust = g['slug'] in KUST
    if kust:
        plekken = ['Strand, strandopgangen en mul zand'] + [p for p in plekken if 'trand' not in p][:2]
    beeld = 'wad-auto' if kust else ['bmw-modder', 'festival-passat', 'defender-berm', 'trekker-uittrekken'][i % 4]
    intro = INTRO[i % 4].format(G=E(G), P=E(P))
    woonpl = [w for w in g['woonplaatsen']]
    kernen = ''
    if len(woonpl) > 1:
        kernen = (f'<h3>Woonplaatsen in de gemeente {E(G)}</h3><p>Wij komen in alle {len(woonpl)} woonplaatsen van de gemeente, en in het buitengebied daaromheen:</p>'
                  f'<ul class="kernen">' + ''.join(f'<li>{E(w)}</li>' for w in woonpl) + '</ul>')
    buren = g['buren'][:8]
    burenlijst = ''.join(f'<li><a href="{r}auto-vast/{b["slug"]}/">{E(b["naam"])}</a><span>{b["km"]} km</span></li>' for b in buren)
    b1, b2 = buren[0]['naam'], buren[1]['naam']
    vragen = [
        (f'Mijn auto staat vast in {E(G)}. Hoe snel kunnen jullie er zijn?', f'Dat hangt af van waar in de gemeente {E(G)} u staat en hoe druk het op dat moment is. Bij uw melding zeggen we eerlijk hoe laat we er kunnen zijn. Deel uw locatie via WhatsApp, dan rijden we direct de goede kant op.'),
        (f'Helpen jullie ook in {E(b1)} en {E(b2)}?', f'Ja. Naast {E(G)} komen we ook in {E(b1)}, {E(b2)} en de rest van {E(P)}. Wij werken in heel Nederland.'),
        (f'Wat moet ik doorgeven als ik vastzit in {E(G)}?', 'Uw locatie (het liefst via GPS of WhatsApp), het type voertuig, waar u in vastzit en hoe diep. Een foto van de auto en de ondergrond helpt ons om met het juiste materiaal te komen.'),
        (f'Mijn auto staat vast op het strand bij {E(G)}. Wat nu?', 'Stop met gas geven, want in mul zand graaft de auto zich snel in. Staat u op nat zand of slik en komt het water op, bel dan meteen en blijf zelf op een veilige plek. Wij komen met zandplaten en bergingsbanden.')
        if kust else
        (f'Wat kost het om mijn auto los te laten trekken in {E(G)}?', 'Dat hangt af van de afstand, de situatie en hoe diep de auto vastzit. U hoort de prijs voordat we beginnen, zodat u niet voor verrassingen komt te staan.'),
    ]
    sit_links = ''.join(f'<li><a href="{r}situaties.html#{sid}">{t}</a></li>' for sid, t, *_ in SITUATIES)
    body = (pkop(r, f'Auto vast in de modder in {E(G)}?', intro, beeld,
                 [('Home', ''), ('Werkgebied', 'werkgebied/'), (P, f'werkgebied/{g["prov_slug"]}/'), (G, '')], plaats=G)
            + f'''<section class="sec"><div class="wrap regio">
<div class="regio__tekst">
  <h2>Losgetrokken in {E(G)} en omgeving</h2>
  <p class="lead">Modder, gras, zand, sneeuw of een zachte berm: wij trekken personenauto's, bestelbussen, campers en auto's met aanhanger los in de hele gemeente {E(G)}.</p>
  <div class="landschap"><p><b>{E(P)}: {E(land)}.</b> {E(land_tekst)}</p></div>
  <h3>Waar wij in {E(G)} vaak helpen</h3>
  {vinkjes([E(p) for p in plekken] + ['Op uw eigen oprit, erf of parkeerplaats'])}
  {kernen}
  <h3>Situaties</h3>
  <ul class="vinkjes">{''.join(f'<li>{icon("vink")}<a href="{r}situaties.html#{sid}">{t}</a></li>' for sid, t, *_ in SITUATIES)}</ul>
</div>
<aside class="regio__zij">
  <div class="kaart kaart--donker"><h3>Vast in {E(G)}?</h3><p>Geef door waar u vastzit, deel uw locatie en verstuur alles in één WhatsApp-bericht.</p>
    <a class="btn btn--vol" href="{r}hulp-aanvragen.html?plaats={quote(G)}">Hulp aanvragen</a><a class="btn btn--rand btn--vol" href="tel:{C['telefoonLink']}">{icon('tel')}Bel {TELNR}</a></div>
  <div class="kaart"><h3>Ook in de buurt</h3><ul class="buren">{burenlijst}</ul>
    <p style="margin:14px 0 0"><a class="pijl" href="{r}werkgebied/{g['prov_slug']}/">Alle gemeenten in {E(P)} {icon('pijl')}</a></p></div>
</aside>
</div></section>
<section class="sec sec--wit"><div class="wrap"><div class="kop kop--midden"><div><span class="boven">Veelgestelde vragen</span><h2>Vastgereden in {E(G)}</h2></div></div>{faq(vragen)}</div></section>
''' + cta(r, f'Vast in {E(G)}?', 'Bel of app ons direct. We zeggen eerlijk wanneer we er kunnen zijn.', plaats=G))
    titel = f'Auto vast in de modder in {G}? | Lostrek'
    if len(titel) > 60:
        titel = f'Auto vast in {G}? | Lostrek'
    besch = f'Vastgereden in modder, zand of sneeuw in {G}? Lostrek trekt uw auto los, in heel {P}. Bel of app 085 744 4166 en deel uw locatie.'
    if len(besch) > 160:
        besch = f'Vastgereden in {G}? Lostrek trekt uw auto los uit modder, zand of sneeuw. Bel of app 085 744 4166.'
    pad = f'auto-vast/{g["slug"]}/'
    dienst = {'@context': 'https://schema.org', '@type': 'Service', 'name': f'Vastgereden auto lostrekken in {G}', 'serviceType': 'Lostrekken van vastgereden voertuigen',
              'provider': {'@id': DOMEIN + '/#bedrijf'}, 'areaServed': {'@type': 'City', 'name': G, 'containedInPlace': {'@type': 'AdministrativeArea', 'name': P}},
              'url': DOMEIN + '/' + pad}
    schrijf(pad, r, titel, besch, 'werkgebied', body,
            [('Home', '/'), ('Werkgebied', '/werkgebied/'), (P, f'/werkgebied/{g["prov_slug"]}/'), (G, '/' + pad)], [dienst], prioriteit='0.7')


def provincie_pagina(p):
    r = '../../'
    land, land_tekst, plekken = LANDSCHAP[p['slug']]
    lijst = ''.join(f'<li><a href="{r}auto-vast/{g["slug"]}/">{E(g["naam"])}</a></li>' for g in sorted(p['gemeenten'], key=lambda g: g['naam']))
    body = (pkop(r, f'Auto vast in de provincie {E(p["naam"])}?', f'Wij trekken vastgereden auto\'s los in alle {len(p["gemeenten"])} gemeenten van {E(p["naam"])}. {E(land_tekst)}',
                 'trekker-avond', [('Home', ''), ('Werkgebied', 'werkgebied/'), (p['naam'], '')])
            + f'''<section class="sec"><div class="wrap">
<div class="kop"><div><span class="boven">{E(p['naam'])}</span><h2>Kies uw gemeente</h2></div><p class="lead">Op elke gemeentepagina vindt u de woonplaatsen, de buurgemeenten en antwoord op de vragen die we daar het vaakst krijgen.</p></div>
<ul class="gemlijst">{lijst}</ul>
<h3 style="margin:48px 0 12px">Waar wij in {E(p['naam'])} vaak helpen</h3>{vinkjes([E(x) for x in plekken])}
</div></section>
''' + cta(r, f'Vast in {E(p["naam"])}?', 'Bel of app ons direct. We zeggen eerlijk wanneer we er kunnen zijn.'))
    pad = f'werkgebied/{p["slug"]}/'
    schrijf(pad, r, f'Auto vast in de provincie {p["naam"]}? | Lostrek',
            f'Vastgereden in {p["naam"]}? Lostrek trekt uw auto los uit modder, zand of sneeuw, in alle {len(p["gemeenten"])} gemeenten. Bel of app 085 744 4166.',
            'werkgebied', body, [('Home', '/'), ('Werkgebied', '/werkgebied/'), (p['naam'], '/' + pad)], prioriteit='0.7')


def werkgebied_pagina():
    r = '../'
    blokken = ''.join(f'<div class="provblok"><h2><a href="{p["slug"]}/" style="text-decoration:none">{E(p["naam"])}</a></h2><ul class="gemlijst">'
                      + ''.join(f'<li><a href="{r}auto-vast/{g["slug"]}/">{E(g["naam"])}</a></li>' for g in sorted(p['gemeenten'], key=lambda g: g['naam']))
                      + '</ul></div>' for p in PROVINCIES.values())
    body = (pkop(r, 'Werkgebied: heel Nederland', f'Wij trekken vastgereden auto\'s los in alle {len(GEMEENTEN)} gemeenten van Nederland. Kies uw provincie of gemeente voor de woonplaatsen en de buurgemeenten bij u in de buurt.',
                 'trekker-avond', [('Home', ''), ('Werkgebied', 'werkgebied/')])
            + f'<section class="sec"><div class="wrap">{provkaarten(r, licht=True)}</div></section>\n'
            + f'<section class="sec sec--wit"><div class="wrap provblokken">{blokken}</div></section>\n' + cta(r))
    schrijf('werkgebied/', r, 'Werkgebied: auto vast in heel Nederland | Lostrek',
            f'Lostrek trekt vastgereden auto\'s los in alle {len(GEMEENTEN)} gemeenten van Nederland. Bekijk uw provincie of gemeente.',
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
    for oud in list((SITE / 'auto-vast').glob('*')) if (SITE / 'auto-vast').exists() else []:
        if oud.is_dir() and oud.name not in PER_SLUG:
            for f in oud.iterdir():
                f.unlink()
            oud.rmdir()
    pagina_home(); pagina_situaties(); pagina_hulp(); pagina_vragen(); pagina_contact(); pagina_privacy(); pagina_beeld(); pagina_404()
    werkgebied_pagina()
    for p in PROVINCIES.values():
        provincie_pagina(p)
    for i, g in enumerate(GEMEENTEN):
        gemeente_pagina(i, g)
    overig()
    print(f'klaar: {len(SITEMAP)} pagina\'s in de sitemap, {len(GEMEENTEN)} gemeenten, {sum(1 for g in GEMEENTEN if g["slug"] in KUST)} aan de kust')
