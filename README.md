Projekt 3: Elections Scraper

## Popis projektu
Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace knihoven
Knihovny, které jsou použity v kódu, jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

    pip3 --version                     # overim verzi manazeru
    pip3 install -r requirements.txt   # nainstalujeme knihovny

## Spuštění projektu
Spuštění souboru `main.py` v rámci příkazového řádku požaduje dva povinné argumenty.

    python main.py <odkaz-uzemniho-celku> <vysledny-soubor>

Následně se vám stáhnou výsledky jako soubor s příponou `.csv`.

## Ukázka projektu
Výsledky hlasování pro okres Blansko:

1. argument: `"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6101"`
2. argument: `"vysledky_blansko.csv"`

Spuštění programu:

    python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6101" "vysledky_blansko.csv"

Průběh stahování:

    Nalezeno 116 obcí. Začínám stahovat data...
    [1/116] Zpracováno: Adamov
    [10/116] Zpracováno: Borotín
    ...
    HOTOVO! Data byla úspěšně uložena do souboru: vysledky_blansko.csv

Částečný výstup:

    kód obce;název obce;voliči v seznamu;vydané obálky;platné hlasy;Občanská demokratická strana...
    546194;Bačkov;100;64;64;6;0;0;5;0;3;8;2;0;2;0;0...
    548260;Bartoušov;127;84;83;11;0;0;12;0;0;13;0;0;2;0...
    ...