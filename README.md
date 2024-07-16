
# COCO Dataset Merger

## Description

This project provides a Python script to process and merge multiple folders containing COCO annotations and image files into a single unified dataset. The script ensures that all image filenames and IDs within the annotations are unique, preventing conflicts and making it easier to work with combined datasets. This is particularly useful for researchers and developers working with COCO-format datasets, enabling streamlined data preparation for machine learning and computer vision tasks.

## Key Features

- **Update File Names and IDs:** Automatically renames image files and updates corresponding entries in the JSON annotation files to ensure uniqueness across the combined dataset.
- **Merge Multiple Folders:** Combines images and annotations from multiple source folders into a single output folder.
- **Data Integrity:** Copies original images to the output folder, ensuring no loss of data from the source folders.
- **Compatibility:** Designed to work with COCO-format datasets, maintaining consistency and compatibility for further processing and model training.

## Prerequisites

- Python 3.x
- Libraries:
  - `os`
  - `json`
  - `shutil`

## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Run the Script:**
   ```bash
   ./script.py
   ```

3. **Follow the Prompts:**
   - Enter the number of folders you want to process.
   - Provide the names of the folders to be processed.
   - Provide the name of the output folder where the combined dataset will be saved.

## Script Explanation

### `update_file_names(folder, counter, image_id_map)`

This function updates the filenames and IDs in the JSON annotation file for a given folder, ensuring unique filenames and IDs. It returns the updated counter for use with subsequent folders.

### `create_new_json(folder, output_folder)`

This function creates a new JSON file in the output folder, containing only the `licenses`, `info`, and `categories` keys from the original JSON file.

### `combine_json_and_images(folders, output_folder, image_id_map)`

This function combines the JSON data and images from multiple folders into the specified output folder. It updates the combined JSON file and copies the images to the output folder.

### `main(folders, output_folder)`

The main function orchestrates the processing of multiple folders, calling `update_file_names` for each folder and then combining the JSON and image files.

## Example

1. **Prepare your folders:**
   - Ensure each folder has the following structure:
     ```
     folder_name/
     ├── annotations/
     │   └── instances_default.json
     └── images/
         ├── image1.png
         └── image2.png
     ```

2. **Run the script and follow the prompts:**
   ```bash
   How many folders do you want to process? 2
   Enter the name of folder 1: folder1
   Enter the name of folder 2: folder2
   Enter the name of the output folder: output_folder
   ```

3. **Check the output:**
   - The output folder will contain:
     ```
     output_folder/
     ├── annotations/
     │   └── instances_default.json
     └── images/
         ├── 1.PNG
         ├── 2.PNG
         ├── ...
     ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
