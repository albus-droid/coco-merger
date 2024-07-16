#!/usr/bin/env python3

import os
import json
import shutil


def update_file_names(folder, counter):
    annotations_path = os.path.join(folder, "annotations", "instances_default.json")
    images_path = os.path.join(folder, "images")

    if not os.path.exists(annotations_path):
        print(f"Annotations file not found: {annotations_path}")
        return counter

    if not os.path.exists(images_path):
        print(f"Images folder not found: {images_path}")
        return counter

    with open(annotations_path, "r") as file:
        data = json.load(file)

    images = data.get("images", [])
    annotations = data.get("annotations", [])
    image_files = os.listdir(images_path)  # List all files in the images directory

    for image, annotation in zip(images, annotations):
        if "file_name" in image and image_files:
            current_value = image["file_name"]
            new_value = f"{counter}.PNG"

            if current_value in image_files:
                os.rename(
                    os.path.join(images_path, current_value),
                    os.path.join(images_path, new_value),
                )
                # Update the file_name value in the JSON data

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
    # Function to extract specific keys from a JSON object
    # Specify the keys you want to extract
    keys = ["licenses", "info", "categories"]
    annotations_path = os.path.join(folder, "annotations", "instances_default.json")
    # Read JSON file
    with open(annotations_path, "r") as file:
        data = json.load(file)

    new_data = {}
    # Extract specified keys
    for key in keys:
        if key in data:
            new_data[key] = data[key]

    output_path = os.path.join(output_folder, "annotations", "instances_default.json")
    # Write the extracted data to a new JSON file
    with open(output_path, "w") as file:
        json.dump(new_data, file, indent=4)


def combine_json_and_images(folders, output_folder):
    combined_data = {"images": [], "annotations": []}

    output_annotations = os.path.join(
        output_folder, "annotations", "instances_default.json"
    )
    with open(output_annotations, "r") as file:
        combined_data.update(json.load(file))

    for folder in folders:
        annotations_path = os.path.join(folder, "annotations", "instances_default.json")
        images_path = os.path.join(folder, "images")

        with open(annotations_path, "r") as file:
            data = json.load(file)

        combined_data["images"].extend(data.get("images", []))
        combined_data["annotations"].extend(data.get("annotations", []))

        for image in data.get("images", []):
            image_file = os.path.join(images_path, image["file_name"])
            if os.path.exists(image_file):
                shutil.copy(
                    image_file,
                    os.path.join(output_folder, "images", image["file_name"]),
                )

    with open(output_annotations, "w") as file:
        json.dump(
            combined_data,
            file,
            indent=4,
        )


def main(folders, output_folder):
    counter = 1
    for folder in folders:
        counter = update_file_names(folder, counter)
    combine_json_and_images(folders, output_folder)


if __name__ == "__main__":
    num_of_files = int(input("How many folders do you want to process? "))
    folders = [
        input(f"Enter the name of folder {i + 1}: ") for i in range(num_of_files)
    ]
    output_folder = input("Enter the name of the output folder: ")

    if not os.path.exists(output_folder):
        os.makedirs(os.path.join(output_folder, "annotations"))
        os.makedirs(os.path.join(output_folder, "images"))

    create_new_json(folders[0], output_folder)
    main(folders, output_folder)
