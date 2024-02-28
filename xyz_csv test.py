import json
import csv

# Load JSON data from the data.json file
with open('saved.json', 'r') as json_file:
    data = json.load(json_file)

# Extract information
skus_info = data['skus_info']
additional_info = data['additional_info']

# Create a list of dictionaries for CSV rows
csv_rows = []
for i, sku_info in enumerate(skus_info):
    row = {
        'ID': i + 1,  # Assuming an ID starting from 1 for each SKU
        'Typ': 'variation' if i > 0 else 'variable',  # 'variable' for the main product, 'variation' for variations
        'Artikelnummer': additional_info['num_iid'],  # Assuming this field corresponds to item ID
        'Name': additional_info['title'],
        'Veröffentlicht': 1,  # Assuming products are published
        'Sichtbarkeit im Katalog': 'visible',  # Assuming products are visible
        'Beschreibung': additional_info['desc_short'],  # Assuming short description
        'Gewicht (g)': additional_info['weight'],
        'Länge (cm)':  additional_info.get('length', ''),
        'Breite (cm)': additional_info.get('width', ''),
        'Höhe (cm)': additional_info.get('height', ''),
        'Kategorien': '',  # Add your categories if available
        'Bilder': sku_info['image_url'],
        # Add other fields as needed
    }
    csv_rows.append(row)

# Define CSV field names
field_names = [
    'ID', 'Typ', 'Artikelnummer', 'Name', 'Veröffentlicht', 'Sichtbarkeit im Katalog',
    'Beschreibung', 'Gewicht (g)', 'Länge (cm)', 'Breite (cm)', 'Höhe (cm)', 'Kategorien',
    'Bilder'
]

# Write to CSV file
csv_filename = 'converted_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Write header
    writer.writeheader()
    
    # Write rows
    writer.writerows(csv_rows)

print(f"Data converted and saved to '{csv_filename}'")
