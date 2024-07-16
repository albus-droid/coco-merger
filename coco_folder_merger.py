#!/usr/bin/env python3

import os
import json
import shutil


def update_file_names(folder, counter, image_id_map):
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

    for image in images:
        if "file_name" in image:
            current_value = image["file_name"]
            new_value = f"{counter}.PNG"
            image_id_map[current_value] = new_value

            image["file_name"] = new_value
            image["id"] = counter
            counter += 1

    for annotation in annotations:
        annotation["id"] = counter
        annotation["image_id"] = counter

    # Save the modified data back to the JSON file
    with open(annotations_path, "w") as file:
        json.dump(data, file, indent=4)

    return counter


def create_new_json(folder, output_folder):
    keys = ["licenses", "info", "categories"]
    with open(f"{folder}/annotations/instances_default.json", "r") as file:
        data = json.load(file)

    new_data = {key: data[key] for key in keys if key in data}

    with open(
        os.path.join(output_folder, "annotations/instances_default.json"), "w"
    ) as file:
        json.dump(new_data, file, indent=4)


def combine_json_and_images(folders, output_folder, image_id_map):
    combined_data = {"images": [], "annotations": []}

    with open(
        os.path.join(output_folder, "annotations/instances_default.json"), "r"
    ) as file:
        combined_data.update(json.load(file))

    for folder in folders:
        annotations_path = os.path.join(folder, "annotations", "instances_default.json")
        images_path = os.path.join(folder, "images")

        with open(annotations_path, "r") as file:
            data = json.load(file)

        combined_data["images"].extend(data.get("images", []))
        combined_data["annotations"].extend(data.get("annotations", []))

        for image in data.get("images", []):
            original_file_name = [
                k for k, v in image_id_map.items() if v == image["file_name"]
            ][0]
            image_file = os.path.join(images_path, original_file_name)
            if os.path.exists(image_file):
                shutil.copy(
                    image_file,
                    os.path.join(f"{output_folder}/images", image["file_name"]),
                )

    with open(
        os.path.join(output_folder, "annotations/instances_default.json"), "w"
    ) as file:
        json.dump(combined_data, file, indent=4)


def main(folders, output_folder):
    counter = 1
    image_id_map = {}
    for folder in folders:
        counter = update_file_names(folder, counter, image_id_map)
    combine_json_and_images(folders, output_folder, image_id_map)


if __name__ == "__main__":
    num_of_files = int(input("How many folders do you want to process? "))
    folders = [
        input(f"Enter the name of folder {i + 1}: ") for i in range(num_of_files)
    ]
    output_folder = input("Enter the name of the output folder: ")

    if not os.path.exists(output_folder):
        os.makedirs(f"{output_folder}/annotations")
        os.makedirs(f"{output_folder}/images")

    create_new_json(folders[0], output_folder)
    main(folders, output_folder)
