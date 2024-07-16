import os
import json
import shutil

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def process_and_copy_folders(folders, output_folder):
    combined_data = {"licenses": [], "info": [], "categories": [], "images": [], "annotations": []}
    counter = 1

    for folder in folders:
        annotations_path = os.path.join(folder, "annotations", "instances_default.json")
        images_path = os.path.join(folder, "images")

        if not os.path.exists(annotations_path) or not os.path.exists(images_path):
            print(f"Annotations or images folder not found in: {folder}")
            continue

        data = load_json(annotations_path)
        images = data.get("images", [])
        annotations = data.get("annotations", [])
        image_files = set(os.listdir(images_path))

        if not combined_data["licenses"]:
            combined_data["licenses"] = data.get("licenses", [])
        if not combined_data["info"]:
            combined_data["info"] = data.get("info", [])
        if not combined_data["categories"]:
            combined_data["categories"] = data.get("categories", [])

        for image in images:
            if "file_name" in image and image["file_name"] in image_files:
                new_file_name = f"{counter}.PNG"
                image_copy_path = os.path.join(output_folder, "images", new_file_name)
                os.makedirs(os.path.dirname(image_copy_path), exist_ok=True)
                shutil.copy(os.path.join(images_path, image["file_name"]), image_copy_path)

                image["file_name"] = new_file_name
                image["id"] = counter

                for annotation in annotations:
                    if annotation["image_id"] == image["id"]:
                        annotation["id"] = counter
                        annotation["image_id"] = counter

                combined_data["images"].append(image)
                combined_data["annotations"].append(annotation)
                counter += 1

    os.makedirs(os.path.join(output_folder, "annotations"), exist_ok=True)
    save_json(combined_data, os.path.join(output_folder, "annotations", "instances_default.json"))

def main():
    main_folder = input("Enter the name of the main folder containing subfolders: ")
    output_folder = input("Enter the name of the output folder: ")

    subfolders = [os.path.join(main_folder, subfolder) for subfolder in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, subfolder))]

    process_and_copy_folders(subfolders, output_folder)

if __name__ == "__main__":
    main()
