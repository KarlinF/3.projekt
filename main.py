import csv
import sys
from typing import Optional
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://volby.cz/pls/ps2017nss/"

def validate_args() -> tuple[str, str]:
    if len(sys.argv) != 3:
        print("CHYBA: Zadejte přesně 2 argumenty: <odkaz> <soubor.csv>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

def get_soup(url: str) -> Optional[BeautifulSoup]:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"CHYBA: Nepodařilo se stáhnout stránku {url}: {e}")
        return None

def get_municipalities(soup: BeautifulSoup) -> list[dict]:
    municipalities = []
    for td_cislo in soup.find_all("td", class_="cislo"):
        a_tag = td_cislo.find("a", href=True)
        if not a_tag:
            continue
        code = a_tag.get_text(strip=True)
        link = BASE_URL + a_tag["href"]
        tr_parent = td_cislo.find_parent("tr")
        name_td = tr_parent.find("td", class_="overflow_name")
        name = name_td.get_text(strip=True) if name_td else "Neznámý"
        municipalities.append({"code": code, "name": name, "link": link})
    return municipalities

def get_municipality_data(url: str) -> dict:
    soup = get_soup(url)
    if not soup:
        return {}
    data = {}
    try:
        data['voliči v seznamu'] = soup.find("td", headers="sa2").get_text(strip=True).replace('\xa0', '')
        data['vydané obálky'] = soup.find("td", headers="sa3").get_text(strip=True).replace('\xa0', '')
        data['platné hlasy'] = soup.find("td", headers="sa6").get_text(strip=True).replace('\xa0', '')
    except AttributeError:
        data['voliči v seznamu'] = data['vydané obálky'] = data['platné hlasy'] = "0"
    for tr in soup.find_all("tr"):
        party_td = tr.find("td", class_="overflow_name")
        if party_td:
            party_name = party_td.get_text(strip=True)
            if party_name and party_name != "-":
                cisla = tr.find_all("td", class_="cislo")
                if len(cisla) >= 2:
                    data[party_name] = cisla[1].get_text(strip=True).replace('\xa0', '')
    return data

def scrape_all(url: str) -> tuple[list[str], list[dict]]:
    soup = get_soup(url)
    if not soup:
        sys.exit(1)
    municipalities = get_municipalities(soup)
    if not municipalities:
        sys.exit(1)
    print(f"Nalezeno {len(municipalities)} obcí. Začínám stahovat data...")
    results = []
    party_names = []
    for i, muni in enumerate(municipalities):
        muni_data = get_municipality_data(muni["link"])
        row = {
            "kód obce": muni["code"],
            "název obce": muni["name"],
            "voliči v seznamu": muni_data.get("voliči v seznamu", "0"),
            "vydané obálky": muni_data.get("vydané obálky", "0"),
            "platné hlasy": muni_data.get("platné hlasy", "0")
        }
        for key, value in muni_data.items():
            if key not in ["voliči v seznamu", "vydané obálky", "platné hlasy"]:
                row[key] = value
                if key not in party_names:
                    party_names.append(key)
        results.append(row)
        if (i + 1) % 10 == 0 or i == 0:
            print(f" [{i + 1}/{len(municipalities)}] Zpracováno: {muni['name']}")
    return party_names, results

def save_to_csv(party_names: list[str], results: list[dict], output_file: str):
    fieldnames = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + party_names
    try:
        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(results)
        print(f"\nHOTOVO! Data byla úspěšně uložena do souboru: {output_file}")
    except IOError as e:
        print(f"CHYBA: Nepodařilo se zapsat do souboru {output_file}: {e}")

def main():
    url, output_file = validate_args()
    party_names, results = scrape_all(url)
    save_to_csv(party_names, results, output_file)

if __name__ == "__main__":
    main()