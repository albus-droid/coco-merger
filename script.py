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

def process_and_copy_folders(folders, output_folder):
    """
    Process multiple folders to update filenames and IDs, then combine JSON data and copy images 
    to the specified output folder. Ensures unique filenames and IDs.
    
    Parameters:
    - folders: List of paths to the input folders.
    - output_folder: Path to the output folder.
    """
    # Initialize the combined data dictionary
    combined_data = {
        "licenses": [], 
        "info": [], 
        "categories": [], 
        "images": [], 
        "annotations": []
    }
    counter = 1
    image_id_map = {}

    for folder in folders:
        annotations_path = os.path.join(folder, "annotations", "instances_default.json")
        images_path = os.path.join(folder, "images")

        # Check if annotations and images directories exist
        if not os.path.exists(annotations_path) or not os.path.exists(images_path):
            print(f"Annotations or images folder not found in: {folder}")
            continue

        # Load JSON data from the annotations file
        data = load_json(annotations_path)
        images = data.get("images", [])
        annotations = data.get("annotations", [])
        image_files = set(os.listdir(images_path))

        # Initialize the licenses, info, and categories keys from the first folder
        if not combined_data["licenses"]:
            combined_data["licenses"] = data.get("licenses", [])
        if not combined_data["info"]:
            combined_data["info"] = data.get("info", [])
        if not combined_data["categories"]:
            combined_data["categories"] = data.get("categories", [])

        for image in images:
            if "file_name" in image and image["file_name"] in image_files:
                # Create new filename and copy the image
                new_file_name = f"{counter}.PNG"
                image_copy_path = os.path.join(output_folder, "images", new_file_name)
                os.makedirs(os.path.dirname(image_copy_path), exist_ok=True)
                shutil.copy(os.path.join(images_path, image["file_name"]), image_copy_path)

                # Update image information
                image_id_map[image["id"]] = counter
                image["file_name"] = new_file_name
                image["id"] = counter

                # Append updated image to combined data
                combined_data["images"].append(image)
                counter += 1

        for annotation in annotations:
            # Update annotation with new image ID
            old_id = annotation["image_id"]
            if old_id in image_id_map:
                annotation["image_id"] = image_id_map[old_id]
                combined_data["annotations"].append(annotation)

    # Ensure the output directory exists and save combined JSON data
    os.makedirs(os.path.join(output_folder, "annotations"), exist_ok=True)
    save_json(combined_data, os.path.join(output_folder, "annotations", "instances_default.json"))

def main():
    """Main function to handle user input and initiate the processing."""
    main_folder = input("Enter the name of the main folder containing subfolders: ")
    output_folder = input("Enter the name of the output folder: ")

    # Collect all subfolders in the main folder
    subfolders = [
        os.path.join(main_folder, subfolder) 
        for subfolder in os.listdir(main_folder) 
        if os.path.isdir(os.path.join(main_folder, subfolder))
    ]

    # Process the subfolders and copy data to the output folder
    process_and_copy_folders(subfolders, output_folder)

if __name__ == "__main__":
    main()
