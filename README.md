
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
   python script.py
   ```

3. **Follow the Prompts:**
   - Enter the name of the main folder containing subfolders.
   - Provide the name of the output folder where the combined dataset will be saved.

## Script Explanation

### `process_and_copy_folders(folders, output_folder)`

This function processes multiple folders to update filenames and IDs, then combines JSON data and copies images to the specified output folder, ensuring unique filenames and IDs.

### `main()`

The main function orchestrates the processing by prompting the user for input, calling `process_and_copy_folders` to handle the merging of datasets.

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
   Enter the name of the main folder containing subfolders: main_folder
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
