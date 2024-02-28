from pandalib import pandalib, pandautilities
import json

bearertoken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpblRpbWUiOjE3MDQ3MTk0NDY1NDEsInVzZXJfbmFtZSI6InNpbHZhbmJlbHRlbkBnbWFpbC5jb20iLCJzY29wZSI6WyJhbGwiXSwibG9naW5JcCI6Ijc5LjIwNi4xMi4xNjYiLCJpZCI6ODA5MjI5MzM1LCJleHAiOjE3MDY4Nzk0NDYsImp0aSI6ImJhMjBlYTAzLTQ0ODgtNGJjYi1iMTlkLWYyN2Y1M2VjMTcyNCIsImNsaWVudF9pZCI6InBvcnRhbC1wYyIsInBsYXRmb3JtIjpudWxsfQ.RYq_A2NzQ77RZBwhTNpY3QsOhkAES_jFSceoi79ibQxOY26Rfqjyk8r-wlOHtq6LvG5BFnFMd-V1u_nXb4x5m4nEqIQ8wm67JfVfcCNA1EZnewD5q0TLLOhrbLEMMWQdNe6VAB7c-h_N3_I2-mofZPI2LWyUBVDRVnLGxStOePs"
item_link = "https://detail.tmall.com/item.htm?id=702820303183"
lib = pandalib(bearertoken, "809229335")

# Fetch item data and save it to a JSON file
item = lib.get_item(item_link)
file_path = "data_raw.json"
with open(file_path, 'w') as json_file:
    json.dump(item, json_file)
print(f'Data has been saved to {file_path}')

# Process and extract information from the saved JSON file
with open('data_raw.json', 'r') as json_file:
    data = json.load(json_file)

# Extract property information from prop_arr
prop_arr = data['data']['item']['prop_arr']

# Extract required information
skus_info = []
for sku in data['data']['item']['skus']['sku']:
    properties_name = sku['properties_name']
    properties = sku['properties']

    # Extract property names based on prop_arr
    prop_names = []
    for prop in prop_arr:
        prop_id = prop['propId']
        value_id = prop['valueId']
        # Check if the property exists in the sku, if not set it to "0"
        if properties and f"{prop_id}:{value_id}" in properties:
            prop_names.append(prop['valueName'])
        else:
            prop_names.append("0")

    sku_info = {
        'total_price': sku['total_price'],
        'properties_name': ', '.join(prop_names),
        'properties': properties,
        'image_url': data['data']['item']['props_img'].get(properties, '')
    }
    skus_info.append(sku_info)

# Extract additional information
additional_info = {
    'weight': data['data']['item']['timeInfo'].get('weight', '0'),
    'volume': data['data']['item']['timeInfo'].get('volume', '0'),
    'post_fee': data['data']['item'].get('post_fee', '0'),
    'title': data['data']['item'].get('title', '0'),
    'price': data['data']['item'].get('price', '0'),
    'images': data['data']['item'].get('item_imgs', '0')
}

# Print extracted information
print("SKU Information:")
for sku_info in skus_info:
    print(f"Total Price: {sku_info['total_price']}, Properties Name: {sku_info['properties_name']}, Properties: {sku_info['properties']}, Image URL: {sku_info['image_url']}")

print("\nAdditional Information:")
print(f"Weight: {additional_info['weight']}")
print(f"Volume: {additional_info['volume']}")
print(f"Post Fee: {additional_info['post_fee']}")
print(f"Title: {additional_info['title']}")
print(f"Price: {additional_info['price']}")
print(f"Images URL : {additional_info['images']}")

# Save the information to a new JSON file
output_data = {
    'skus_info': skus_info,
    'additional_info': additional_info
}

with open('data.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=2)

print("\nData saved to 'data.json'")
