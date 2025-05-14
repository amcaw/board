import os
import requests
import json
from datetime import datetime, timedelta

def main():
    try:
        API_URL = os.environ['API_URL']
        ZIPCODE_ID = os.environ['ZIPCODE_ID']
        STREET = os.environ['STREET']
        HOUSE_NUMBER = os.environ['HOUSE_NUMBER']
        X_SECRET = os.environ['X_SECRET']
        X_CONSUMER = os.environ['X_CONSUMER']
        REFERER = os.environ['REFERER']
    except KeyError as e:
        print(json.dumps({"error": f"Missing environment variable: {str(e)}"}, indent=2))
        return

    # Use tomorrow's date for both fromDate and untilDate 
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime('%Y-%m-%d')
    
    params = {
        'zipcodeId': ZIPCODE_ID,
        'streetId': STREET,
        'houseNumber': HOUSE_NUMBER,
        'fromDate': date_str,
        'untilDate': date_str,
        'size': '3'
    }
    
    headers = {
        'x-secret': X_SECRET,
        'x-consumer': X_CONSUMER,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json, text/plain, */*',
        'Referer': REFERER
    }
    
    try:
        response = requests.get(API_URL, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"error": str(e)}
    
    # Mapping of French waste types to Font Awesome icon markup
    icon_map = {
        "Déchets ménagers résiduels": "<i class='fas fa-trash'></i>",
        "PMC": "<i class='fa-solid fa-recycle'></i>",
        "Papiers-cartons": "<i class='fa-solid fa-box-open'></i>"
    }
    
    icons = []
    for item in data.get("items", []):
        fraction = item.get("fraction", {})
        name_fr = fraction.get("name", {}).get("fr", "")
        # Skip "Déchets organiques"
        if name_fr == "Déchets organiques":
            continue
        if name_fr in icon_map:
            icons.append(icon_map[name_fr])
    
    icons_str = " ".join(icons)
    
    # If no icons are collected, display the "fa-ban" icon using single quotes
    if not icons_str:
        icons_str = "<i class='fa-solid fa-ban'></i>"
    
    output_array = [{
        "name": "trash",
        "to_do": icons_str
    }]
    
    with open("trash.json", "w", encoding="utf-8") as f:
        json.dump(output_array, f, indent=2, ensure_ascii=False)
    
    print(json.dumps(output_array, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
