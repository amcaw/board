import os
import requests
import json
import unicodedata
from datetime import datetime, timedelta

def normalize(text: str) -> str:
    """
    Normalise une chaîne :
      - suppression des accents
      - passage en minuscules
      - strip des espaces en début/fin
    """
    nfkd = unicodedata.normalize('NFD', text)
    no_accents = nfkd.encode('ascii', 'ignore').decode('utf-8')
    return no_accents.strip().lower()

def main():
    # Chargement des variables d'environnement
    try:
        API_URL        = os.environ['API_URL']
        ZIPCODE_ID     = os.environ['ZIPCODE_ID']
        STREET         = os.environ['STREET']
        HOUSE_NUMBER   = os.environ['HOUSE_NUMBER']
        X_SECRET       = os.environ['X_SECRET']
        X_CONSUMER     = os.environ['X_CONSUMER']
        REFERER        = os.environ['REFERER']
    except KeyError as e:
        print(json.dumps({"error": f"Missing environment variable: {str(e)}"}, indent=2))
        return

    # Préparation de la date de demain
    tomorrow = datetime.now()
    date_str = tomorrow.strftime('%Y-%m-%d') + timedelta(days=-1)

    params = {
        'zipcodeId':    ZIPCODE_ID,
        'streetId':     STREET,
        'houseNumber':  HOUSE_NUMBER,
        'fromDate':     date_str,
        'untilDate':    date_str,
        'size':         '3'
    }
    headers = {
        'x-secret':     X_SECRET,
        'x-consumer':   X_CONSUMER,
        'User-Agent':   'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept':       'application/json, text/plain, */*',
        'Referer':      REFERER
    }

    # Appel API
    try:
        resp = requests.get(API_URL, params=params, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        data = {"error": str(e)}

    # Mapping original
    icon_map = {
        "ordures menageres residuelles": "<i class='fas fa-trash'></i>",
        "pmc":                            "<i class='fa-solid fa-recycle'></i>",
        "papiers-cartons":                "<i class='fa-solid fa-box-open'></i>"
    }
    # Création du mapping normalisé
    normalized_map = {
        normalize(k): v
        for k, v in icon_map.items()
    }
    skip_key = normalize("Déchets organiques")

    icons = []
    for item in data.get("items", []):
        name_fr = item.get("fraction", {}).get("name", {}).get("fr", "")
        norm = normalize(name_fr)
        # Debug (optionnel) : 
        # print(f"Fraction reçue: {name_fr!r} -> normalisée: {norm!r}")
        if norm == skip_key:
            continue
        if norm in normalized_map:
            icons.append(normalized_map[norm])

    icons_str = " ".join(icons)
    if not icons_str:
        # fallback si aucune icône valide
        icons_str = "<i class='fa-solid fa-ban'></i>"

    output = [{
        "name":  "trash",
        "to_do": icons_str
    }]

    # Sauvegarde et affichage
    with open("trash.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
