import os
import zipfile
import requests
import shutil
import click

def download_and_extract_zip(zip_url, destination_folder):
    """
    The function `download_and_extract_zip` downloads a zip file from a given URL and extracts its
    contents to a specified destination folder.
    
    :param zip_url: The URL of the zip file that you want to download and extract
    :param destination_folder: The destination_folder parameter is the path where you want to save the
    downloaded zip file and extract its contents. It can be an absolute path or a relative path to the
    current working directory
    """
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Download the zip file
    response = requests.get(zip_url)
    if response.status_code == 200:
        zip_file_path = os.path.join(destination_folder, "temp.zip")
        with open(zip_file_path, 'wb') as f:
            f.write(response.content)

        # Extract the contents of the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

        # Remove the zip file after extraction
        os.remove(zip_file_path)

        # Remove the existing "dist" folder if it exists
        dist_folder = os.path.join(destination_folder, "dist")
        if os.path.exists(dist_folder):
            shutil.rmtree(dist_folder)

        # Rename the extracted folder to "dist"
        extracted_folder = os.path.join(destination_folder, os.path.basename(zip_url).replace('.zip', ''))
        shutil.move(extracted_folder, dist_folder)

        click.secho("Zip file downloaded and extracted successfully.", fg="yellow")
    else:
        click.secho("Failed to download the zip file.", fg="red")