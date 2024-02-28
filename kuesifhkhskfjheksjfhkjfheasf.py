import json
import os
import urllib.request

def download_image(image_url, destination_path):
    urllib.request.urlretrieve(image_url, destination_path)

def detect_variation_types(data):
    variation_types = set()
    for sku_info in data['skus_info']:
        properties_name = sku_info['properties_name']
        variations = [prop.strip() for prop in properties_name.split(',')]
        variation_types.update(variations)
    return list(variation_types)

def select_superior_variation(variation_types):
    print("Select the superior variation type:")
    for index, var_type in enumerate(variation_types, start=1):
        print(f"{index}. {var_type}")

    superior_variation_index = int(input("Enter the number of the superior variation: ")) - 1
    return list(variation_types)[superior_variation_index]

def split_products(data, superior_variation):
    product_1 = {'skus_info': [], 'additional_info': data['additional_info'].copy()}
    product_2 = {'skus_info': [], 'additional_info': data['additional_info'].copy()}

    for sku_info in data['skus_info']:
        properties_name = sku_info['properties_name']
        variations = [prop.strip() for prop in properties_name.split(',')]
        if superior_variation in variations:
            product_1['skus_info'].append(sku_info)
        else:
            product_2['skus_info'].append(sku_info)

    return product_1, product_2

def handle_inferior_variation_prices(product_2):
    inferior_variation_prices = set()
    for sku_info in product_2['skus_info']:
        total_price = sku_info['total_price']
        inferior_variation_prices.add(total_price)

    if all(price == 0 for price in inferior_variation_prices):
        new_price = float(input("Enter the price for all variations of the inferior variation: "))
        for sku_info in product_2['skus_info']:
            sku_info['total_price'] = new_price
    else:
        print("Prices for inferior variations differ:")
        print("1. Set a single price for all variations")
        print("2. Set individual prices for each variation")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            new_price = float(input("Enter the price for all variations of the inferior variation: "))
            for sku_info in product_2['skus_info']:
                sku_info['total_price'] = new_price
        elif choice == 2:
            for sku_info in product_2['skus_info']:
                print(f"Current price for {sku_info['properties_name']}: {sku_info['total_price']}")
                new_price = float(input("Enter the new price: "))
                sku_info['total_price'] = new_price
        else:
            print("Invalid choice. Prices will not be updated.")

def handle_props_img(data):
    for sku_info in data['skus_info']:
        props_img = sku_info.get('props_img', {})
        if not props_img:
            sku_info['props_img'] = {f"{prop['propId']}:{prop['valueId']}": image['url'] for prop, image in zip(data['translate_prop_arr'], data['additional_info']['images'])}

def save_updated_data(data):
    with open('updated_data.json', 'w') as updated_json_file:
        json.dump(data, updated_json_file, indent=2)

def main():
    # Load data from the previous JSON file
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    # Detect variation types
    variation_types = detect_variation_types(data)

    # Ask user to choose the superior variation type
    superior_variation = select_superior_variation(variation_types)

    # Split into two products based on the superior variation
    product_1, product_2 = split_products(data, superior_variation)

    # Handle prices for inferior variations in product_2
    handle_inferior_variation_prices(product_2)

    # Handle props_img
    handle_props_img(data)

    # Save the updated information to a new JSON file
    save_updated_data(data)

    print("\nData updated and saved to 'updated_data.json'.")

if __name__ == "__main__":
    main()
