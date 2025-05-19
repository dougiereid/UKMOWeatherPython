import requests
import os
from urllib.parse import urlparse, quote
import time
import json
import argparse

# Configuration
# API_KEY = "YOUR_API_KEY"  # Replace with your actual API key - Removed hardcoding
# BASE_URL = "https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0" # Removed hardcoding.
# ORDER_ID = "YOUR_ORDER_ID"  # Replace with your Order ID - Removed hardcoding
DOWNLOAD_PATH = "weather_data"  # Directory to save downloaded files


def list_files_in_order(base_url, order_id, api_key):
    """
    Lists the files available in a specific order.

    Args:
        base_url (str): The base URL of the API.
        order_id (str): The ID of the order.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of file IDs, or None on error.
    """
    url = f"{base_url}/orders/{order_id}/latest"
    headers = {"Accept": "application/json", "x-api-key": api_key}  # Include API key in headers

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if not response.content:
            print("Warning: Empty response from the server.")
            return []

        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Error decoding JSON response.  Response text was:")
            print(response.text)
            return None

        if not isinstance(data, list):
            print("Error: Expected a list of files, but got a different data structure:")
            print(data)
            return None

        files = [item["fileId"] for item in data]
        return files
    except requests.exceptions.RequestException as e:
        print(f"Error listing files: {e}")
        return None



def download_file(base_url, order_id, file_id, download_path, api_key):
    """
    Downloads a specific file from an order. Handles file naming
    and ensures the download directory exists.

    Args:
        base_url (str): The base URL of the API.
        order_id (str): The ID of the order.
        file_id (str): The ID of the file to download.
        download_path (str): The directory to save the file to.
        api_key (str): The API key for authentication.
    """
    encoded_file_id = quote(file_id)
    url = f"{base_url}/orders/{order_id}/latest/{encoded_file_id}/data"
    headers = {"Accept": "application/x-grib", "x-api-key": api_key}  # Include API key

    os.makedirs(download_path, exist_ok=True)
    file_extension = os.path.splitext(file_id)[1] or ".dat"
    safe_filename = f"{file_id.replace('/', '_')}{file_extension}"
    filepath = os.path.join(download_path, safe_filename)

    try:
        print(f"Downloading {file_id} to {filepath}")
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {file_id} successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {file_id}: {e}")
    except OSError as e:
        print(f"OS Error writing file: {e}")



def main():
    """
    Main function to list files and download them.
    """
    parser = argparse.ArgumentParser(description="Download data from the Met Office Data Hub.")
    parser.add_argument("--apikey", required=True, help="Your Met Office Data Hub API key.")
    parser.add_argument("--orderid", required=True, help="The ID of the order to download.")
    parser.add_argument("--baseurl",
                        default="https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0",
                        help="The base URL of the Met Office API.  Defaults to "
                             "https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0")
    parser.add_argument("--downloadpath", default="weather_data",
                        help="The directory to download files to. Defaults to 'weather_data'.")

    args = parser.parse_args()

    api_key = args.apikey
    order_id = args.orderid
    base_url = args.baseurl
    download_path = args.downloadpath
    if not api_key:
        print("Error: API_KEY is not set.  Please provide it using the --apikey argument.")
        return

    if not order_id:
        print("Error: ORDER_ID is not set. Please provide it using the --orderid argument.")
        return

    files = list_files_in_order(base_url, order_id, api_key)  # Pass api_key
    if files:
        print(f"Found {len(files)} files in order {order_id}.")
        for file_id in files:
            download_file(base_url, order_id, file_id, download_path, api_key)  # Pass api_key
            time.sleep(1)
    else:
        print(f"No files found or error listing files for order {order_id}.")



if __name__ == "__main__":
    main()
