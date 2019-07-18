# dsop-api-spesifikasjoner

Ei samling script som henter informasjon om organisasjoner frå Enhetsregisteret, transformerer disse og laster de opp i Felles datakatalog sin interne publiser-katalog.

Organisasjoner er gitt i fila banker.csv.

## Bakgrunn
Et utvalg av disse opplysningene fra Enhetsregisteret må inn i FDKs publishers-tabell.

For å hente opplysninger fra Enhetsregisteret om gitt virksomhet og skrive til fil:

```
curl -H "Accept: application/json"  https://data.brreg.no/enhetsregisteret/enhet/837884942 |jq '.' > Sparebank1_837884942_Enhetsregisteret.json
```

Et utvalg av disse opplysningene legges inn på følgende format:

```
{
    "organisasjonsform": "SPA",
    "naeringskode": {
        "uri": "http://www.ssb.no/nace/sn2007/84.110",
        "code": "84.110",
        "prefLabel": {
            "no": "Bankvirksomhet ellers"
        }
    },
    "sektorkode": {
        "uri": "http://www.brreg.no/sektorkode/3200",
        "code": "3200",
        "prefLabel": {
            "no": "Banker"
        }
    },
    "valid": true,
    "uri": "http://data.brreg.no/enhetsregisteret/enhet/837884942",
    "id": "837884942",
    "name": "SPAREBANK 1 ØSTFOLD AKERSHUS",
    "orgPath": "/PRIVAT/837884942",
    "prefLabel": {
        "no": "SPAREBANK 1 ØSTFOLD AKERSHUS"
    }
}
```

Dette json-objektet bør legges inn i en fil, feks `Sparebank1_837884942_Publisher.json`.

For å få den nye publisher inn i FDKs publisher-database, må følgende POST gjøres, her i curl-versjon:

```
curl -H "Content-Type: application/json" -X POST https://<url>/dcat/publisher/<orgnr> --data @Sparebank1_837884942_Publisher.json
```
