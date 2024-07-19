import os
import json
import shutil

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r") as file:
        return json.load(file)

def save_json(data, file_path):
    """Save JSON data to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def process_and_copy_folders(main_folders, output_folder):
    """
    Process subfolders in the main folders, merge annotations and images,
    and copy them to the output folder.
    """
    combined_data = {"licenses": [], "info": [], "categories": [], "images": [], "annotations": []}
    counter = 1
    image_id_map = {}
    cat_id_map = {}

    # Initialize combined_data with the first subfolder's licenses, info, and categories from each main folder
    for main_folder in main_folders:
        subfolders = [os.path.join(main_folder, subfolder) for subfolder in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, subfolder))]
        if subfolders:
            first_subfolder = subfolders[0]
            annotations_path = os.path.join(first_subfolder, "annotations", "instances_default.json")
            if os.path.exists(annotations_path):
                data = load_json(annotations_path)
                combined_data["licenses"] = data.get("licenses", combined_data["licenses"])
                combined_data["info"] = data.get("info", combined_data["info"])

                # Handle category merging for the first subfolder in each main folder
                categories = data.get("categories", [])
                for new_cat in categories:
                    new_id = None
                    for output_cat in combined_data["categories"]:
                        if new_cat["name"] == output_cat["name"]:
                            new_id = output_cat["id"]
                            break

                    if new_id is not None:
                        cat_id_map[new_cat["id"]] = new_id
                    else:
                        new_cat_id = max([c["id"] for c in combined_data["categories"]], default=0) + 1
                        cat_id_map[new_cat["id"]] = new_cat_id
                        new_cat["id"] = new_cat_id
                        combined_data["categories"].append(new_cat)
            else:
                print(f"Annotations not found in the first subfolder of: {main_folder}")

    # Process each subfolder in the provided main folders
    for main_folder in main_folders:
        subfolders = [os.path.join(main_folder, subfolder) for subfolder in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, subfolder))]

        for folder in subfolders:
            annotations_path = os.path.join(folder, "annotations", "instances_default.json")
            images_path = os.path.join(folder, "images")

            if not os.path.exists(annotations_path) or not os.path.exists(images_path):
                print(f"Annotations or images folder not found in: {folder}")
                continue

            data = load_json(annotations_path)
            images = data.get("images", [])
            annotations = data.get("annotations", [])
            categories = data.get("categories", [])

            # Handle category merging for the rest of the subfolders
            for new_cat in categories:
                if new_cat["id"] not in cat_id_map:
                    continue
                new_cat["id"] = cat_id_map[new_cat["id"]]

            image_files = {image_file for image_file in os.listdir(images_path)}

            for image in images:
                if "file_name" in image and image["file_name"] in image_files:
                    new_file_name = f"{counter}.PNG"
                    image_copy_path = os.path.join(output_folder, "images", new_file_name)
                    os.makedirs(os.path.dirname(image_copy_path), exist_ok=True)
                    shutil.copy(os.path.join(images_path, image["file_name"]), image_copy_path)

                    original_image_id = image["id"]
                    image["file_name"] = new_file_name
                    image["id"] = counter
                    combined_data["images"].append(image)

                    # Map original image ID to new image ID
                    image_id_map[original_image_id] = counter
                    counter += 1

            for annotation in annotations:
                original_image_id = annotation["image_id"]
                if original_image_id in image_id_map:
                    new_image_id = image_id_map[original_image_id]
                    annotation["image_id"] = new_image_id
                    annotation["id"] = new_image_id

                    # Update category IDs in annotations
                    if annotation["category_id"] in cat_id_map:
                        annotation["category_id"] = cat_id_map[annotation["category_id"]]

                    combined_data["annotations"].append(annotation)

    # Save the combined data to the output folder
    os.makedirs(os.path.join(output_folder, "annotations"), exist_ok=True)
    save_json(combined_data, os.path.join(output_folder, "annotations", "instances_default.json"))

def main():
    """
    Main function to execute the script.
    This script combines multiple COCO-style dataset annotations and images
    from different folders into a single dataset, ensuring that categories
    are properly merged with unique IDs.
    """
    # Get the number of main folders from the user
    num_main_folders = int(input("Enter the number of main folders containing subfolders: "))

    main_folders = []
    for i in range(num_main_folders):
        main_folder = input(f"Enter the name of main folder {i+1}: ")
        main_folders.append(main_folder)

    output_folder = input("Enter the name of the output folder: ")

    # Process and copy folders
    process_and_copy_folders(main_folders, output_folder)

if __name__ == "__main__":
    main()
