import json
import os
import urllib.request

def download_image(image_url, destination_path):
    urllib.request.urlretrieve(image_url, destination_path)

def main():
    # Load data from the previous JSON file
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    # Ask user if the title is okay
    new_title = input(f"Is the title okay? (y/n) Current title: {data['additional_info']['title']} ")
    if new_title.lower() == 'n':
        new_title = input("Enter a new title: ")
        data['additional_info']['title'] = new_title

    # Download and rename images
    img_download_error = False
    for sku_info in data['skus_info']:
        image_url = sku_info['image_url']
        image_name = f"{new_title.replace(' ', '-')}_{sku_info['properties_name']}.jpg"
        try:
            download_image(image_url, image_name)
        except:
            if not img_download_error:
                print("There was an error downloading the image.")
            img_download_error = True
    
    if img_download_error:
        imgd = input("Would you like to download regular images from the item? (y/n)")
        if imgd.lower() == 'y':
            index = 1
            new_title = input("Enter a new title: ")
            for url in data['additional_info']['images']:
                image_url = url['url']
                image_name = image_name + "-" + str(index) + ".jpg"
                download_image(image_url, image_name)
                index = index + 1

    # Ask user for a new price
    current_price = data['skus_info'][0]['total_price']
    new_price = input(f"Enter a new price (current price: {current_price}): ")
    data['skus_info'][0]['total_price'] = float(new_price)

    # Save available variations as a string
    variations_string = '|'.join([sku_info['properties_name'] for sku_info in data['skus_info']])
    data['variations'] = variations_string

    # Ask user for the type of variation
    variation_type = input("What kind of variation is this? (e.g., color): ")
    data['variation_type'] = variation_type

    # Ask user for weight and volume
    weight = data["additional_info"]["weight"]
    print(data['additional_info']['volume'])
    volume_parts = [int(float(num)) for num in data['additional_info']['volume'].split('*')]
    volume = '/'.join(map(str, volume_parts))

    # Update data with new information
    # data['additional_info']['weight'] = weight
    data['additional_info']['volume'] = volume

    # Save the updated information to a new JSON file
    with open('updated_data.json', 'w') as updated_json_file:
        json.dump(data, updated_json_file, indent=2)

    print("\nData updated and saved to 'updated_data.json'.")

if __name__ == "__main__":
    main()
