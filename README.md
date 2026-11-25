# Mobiele Autobanden

Website van Mobiele Autobanden: mobiele bandenservice voor personenauto's.
Lekke band, nieuwe banden en de seizoenswissel, thuis, op het werk of langs de
weg. Mobiele Autobanden is een handelsnaam van D&D Mobiliteit B.V.

- **Domein:** mobieleautobanden.nl
- **Telefoon en WhatsApp:** 085 744 4166

## Inhoud

| Pagina | Wat het is |
|---|---|
| `/` | Home: bandenmaat-invoer met directe knop naar WhatsApp, diensten, op locatie, werkwijze, bandenmaat lezen, werkgebied, vragen |
| `/diensten.html` | Lekke band, nieuwe banden, seizoenswissel en lekke band onderweg |
| `/hulp-aanvragen.html` | Aanvraag met dienst, bandenmaat, aantal, soort band en locatie via GPS, verstuurd via WhatsApp |
| `/veelgestelde-vragen.html` | Vragen en antwoorden |
| `/contact.html` | Gegevens, adres, KvK, bereikbaarheid |
| `/werkgebied/` en `/werkgebied/{provincie}/` | Provincies en gemeenten |
| `/mobiele-bandenservice/{gemeente}/` | Een eigen pagina voor elk van de 342 gemeenten |

Elke gemeentepagina heeft een eigen tekst, alle woonplaatsen van de gemeente,
de dichtstbijzijnde buurgemeenten met afstand en eigen veelgestelde vragen.

## Bouwen

```bash
python3 bron/bouw.py
```

- Bedrijfsgegevens: `bron/site.json`
- Gemeenten, woonplaatsen en buurgemeenten: `bron/data/gemeenten.json`
- Teksten en opbouw van de pagina's: `bron/bouw.py`
- Stijl en scripts: `site/assets/css/site.css` en `site/assets/js/app.js`

## Publiceren

Bij elke push naar `main` draait Netlify `python3 bron/bouw.py` en publiceert
daarna de map `site/` (zie `netlify.toml`).

## Google

1. Search Console: property `https://mobieleautobanden.nl/`, verifiëren via DNS
   of via de HTML-tag (zet de code in `google.verificatie` in `bron/site.json`),
   daarna `sitemap.xml` indienen.
2. Bedrijfsprofiel: vul de profiellink in bij `google.profielUrl`.
3. E-mail: vul het zakelijke adres in bij `email` in `bron/site.json` en bouw
   opnieuw. Zolang het leeg is, wordt er geen e-mail getoond.

## Modderservice

De eerdere website voor hulp bij een vastgereden auto staat op de branch
`modderservice`. Die volgt als aparte opdracht.
