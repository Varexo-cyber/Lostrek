# Lostrek

Website van Lostrek: hulp bij een vastgereden auto in modder, zand, sneeuw of
de berm. Lostrek is een handelsnaam van D&D Mobiliteit B.V.

- **Domein:** lostrek.nl
- **Telefoon en WhatsApp:** 085 744 4166

## Inhoud

| Pagina | Wat het is |
|---|---|
| `/` | Home: situaties, werkwijze, wat u wel en niet doet als u vastzit, werkgebied, vragen |
| `/situaties.html` | Modder, weiland en festival, strand en wad, berm, sneeuw, camper en caravan |
| `/hulp-aanvragen.html` | Hulpmelder: ondergrond, voertuig, locatie via GPS, verstuurd via WhatsApp |
| `/veelgestelde-vragen.html` | Vragen en antwoorden |
| `/contact.html` | Gegevens, adres, KvK, bereikbaarheid |
| `/werkgebied/` en `/werkgebied/{provincie}/` | Provincies en gemeenten |
| `/auto-vast/{gemeente}/` | Een eigen pagina voor elk van de 342 gemeenten |

Elke gemeentepagina heeft een eigen tekst, het landschap van de provincie, alle
woonplaatsen van de gemeente, de dichtstbijzijnde buurgemeenten met afstand en
eigen veelgestelde vragen. De 25 kustgemeenten krijgen extra inhoud over
vastzitten op het strand en het wad.

## Bouwen

```bash
python3 bron/bouw.py
```

- Bedrijfsgegevens: `bron/site.json`
- Gemeenten, woonplaatsen en buurgemeenten: `bron/data/gemeenten.json`
- Teksten en opbouw van de pagina's: `bron/bouw.py`
- Stijl en scripts: `site/assets/css/site.css` en `site/assets/js/app.js`

De generator maakt alle pagina's, `sitemap.xml`, `robots.txt` en de
gestructureerde gegevens voor Google opnieuw aan in `site/`.

## Publiceren

De site staat op Netlify en is gekoppeld aan deze repository. Bij elke push naar
`main` draait Netlify `python3 bron/bouw.py` en publiceert de map `site/`
(zie `netlify.toml`).

## Google

1. Search Console: property `https://lostrek.nl/`, verifiëren via DNS of via de
   HTML-tag (zet de code in `google.verificatie` in `bron/site.json`), daarna
   `sitemap.xml` indienen.
2. Bedrijfsprofiel: vul de profiellink in bij `google.profielUrl`, dan wordt die
   aan de bedrijfsgegevens voor Google gekoppeld.
3. E-mail: zodra het zakelijke adres er is, vul het in bij `email` in
   `bron/site.json` en bouw opnieuw. Zolang het leeg is, wordt er geen e-mail
   getoond.

## Beeld

Alle foto's zijn echte situaties onder een Creative Commons-licentie. Maker,
licentie en bron staan op `/beeldverantwoording.html` en bij elke foto.
