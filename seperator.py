import json

def separate_colors_and_sizes(file_path):
    # Read JSON data from the external file
    with open(file_path, 'r') as file:
        data = json.load(file)

    color_variations = {}

    # Iterate through skus_info in the data
    for sku in data["skus_info"]:
        # Extract color from properties_name
        color = sku["properties_name"].split(",")[-2].strip()

        # If color is not already a key, create an empty list
        if color not in color_variations:
            color_variations[color] = []

        # Append the current sku to the corresponding color
        color_variations[color].append(sku)

    # Convert each color variation to JSON and print
    for color, skus in color_variations.items():
        output = {"skus_info": skus}
        output_file_path = f"{color}_output.json"

        # Write the output JSON to a file
        with open(output_file_path, 'w') as output_file:
            json.dump(output, output_file, indent=2)

        print(f"Successfully created {output_file_path}")

# Replace 'your_input_file.json' with the path to your external JSON file
separate_colors_and_sizes('data.json')
