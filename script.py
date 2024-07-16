#!/usr/bin/env python3

import os
import json
import shutil

def update_file_names(folder, counter):
    # Paths to the annotations file and images folder
    annotations_path = os.path.join(folder, "annotations", "instances_default.json")
    images_path = os.path.join(folder, "images")

    # Check if the annotations file exists
    if not os.path.exists(annotations_path):
        print(f"Annotations file not found: {annotations_path}")
        return counter

    # Check if the images folder exists
    if not os.path.exists(images_path):
        print(f"Images folder not found: {images_path}")
        return counter

    # Load the annotations file
    with open(annotations_path, "r") as file:
        data = json.load(file)

    images = data.get("images", [])
    annotations = data.get("annotations", [])
    image_files = os.listdir(images_path)  # List all files in the images directory

    # Update file names and ids
    for image, annotation in zip(images, annotations):
        if "file_name" in image and image_files:
            current_value = image["file_name"]
            new_value = f"{counter}.PNG"

            if current_value in image_files:
                os.rename(
                    os.path.join(images_path, current_value),
                    os.path.join(images_path, new_value),
                )
                # Update the file_name and id values in the JSON data
                image["file_name"] = new_value
                image["id"] = counter
                annotation["id"] = counter
                annotation["image_id"] = counter
                counter += 1

    # Save the modified data back to the JSON file
    with open(annotations_path, "w") as file:
        json.dump(data, file, indent=4)

    return counter

def create_new_json(folder, output_folder):
    # Specify the keys to extract from the original JSON
    keys = ["licenses", "info", "categories"]
    annotations_path = os.path.join(folder, "annotations", "instances_default.json")

    # Read the original annotations JSON file
    with open(annotations_path, "r") as file:
        data = json.load(file)

    # Create a new data dictionary with the specified keys
    new_data = {}
    for key in keys:
        if key in data:
            new_data[key] = data[key]

    # Write the extracted data to a new JSON file in the output folder
    output_path = os.path.join(output_folder, "annotations", "instances_default.json")
    with open(output_path, "w") as file:
        json.dump(new_data, file, indent=4)

def combine_json_and_images(folders, output_folder):
    combined_data = {"images": [], "annotations": []}

    # Load the initial JSON data from the output folder
    output_annotations = os.path.join(output_folder, "annotations", "instances_default.json")
    with open(output_annotations, "r") as file:
        combined_data.update(json.load(file))

    for folder in folders:
        annotations_path = os.path.join(folder, "annotations", "instances_default.json")
        images_path = os.path.join(folder, "images")

        # Read the annotations JSON file for the current folder
        with open(annotations_path, "r") as file:
            data = json.load(file)

        # Append images and annotations to the combined data
        combined_data["images"].extend(data.get("images", []))
        combined_data["annotations"].extend(data.get("annotations", []))

        # Copy images to the output folder
        for image in data.get("images", []):
            image_file = os.path.join(images_path, image["file_name"])
            if os.path.exists(image_file):
                shutil.copy(
                    image_file,
                    os.path.join(output_folder, "images", image["file_name"]),
                )

    # Save the combined data to the output annotations file
    with open(output_annotations, "w") as file:
        json.dump(combined_data, file, indent=4)

def main(folders, output_folder):
    counter = 1
    for folder in folders:
        counter = update_file_names(folder, counter)
    combine_json_and_images(folders, output_folder)

if __name__ == "__main__":
    # Get the number of folders to process and their names from the user
    num_of_files = int(input("How many folders do you want to process? "))
    folders = [input(f"Enter the name of folder {i + 1}: ") for i in range(num_of_files)]
    output_folder = input("Enter the name of the output folder: ")

    # Create necessary directories in the output folder if they don't exist
    if not os.path.exists(output_folder):
        os.makedirs(os.path.join(output_folder, "annotations"))
        os.makedirs(os.path.join(output_folder, "images"))

    # Create a new JSON file in the output folder with the necessary keys
    create_new_json(folders[0], output_folder)
    # Process all folders and combine their data into the output folder
    main(folders, output_folder)
