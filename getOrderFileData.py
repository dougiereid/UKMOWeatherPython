import requests
import json
import os
import datetime
import shutil
from urllib.parse import quote # Import the quote function

# --- Configuration ---
api_key = "eyJ4NXQjUzI1NiI6Ik5XVTVZakUxTkRjeVl6a3hZbUl4TkdSaFpqSmpOV1l6T1dGaE9XWXpNMk0yTWpRek5USm1OVEE0TXpOaU9EaG1NVFJqWVdNellXUm1ZalUyTTJJeVpBPT0iLCJraWQiOiJnYXRld2F5X2NlcnRpZmljYXRlX2FsaWFzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ==.eyJzdWIiOiJkb3VnaWVAZG91Z2llcmVpZC5jby51a0BjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6ImRvdWdpZUBkb3VnaWVyZWlkLmNvLnVrIiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJhdG1vc3BoZXJpYy05MjZkYzg4Yy04ZTkxLTQxYzEtOTA1NC0wYTE4ZmUwMTZlMGUiLCJpZCI6MTIxMzAsInV1aWQiOiI1NzFkYzBiMy1iNDE0LTRmODgtOGZjNi1mZWUwZjMwMTU5M2EifSwiaXNzIjoiaHR0cHM6XC9cL2FwaS1tYW5hZ2VyLmFwaS1tYW5hZ2VtZW50Lm1ldG9mZmljZS5jbG91ZDo0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyJ3ZGhfYXRtb3NwaGVyaWNfZnJlZSI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0Ijoic2VjIn19LCJrZXl0eXBlIjoiUFJPRFVDVElPTiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6ImF0bW9zcGhlcmljLW1vZGVscyIsImNvbnRleHQiOiJcL2F0bW9zcGhlcmljLW1vZGVsc1wvMS4wLjAiLCJwdWJsaXNoZXIiOiJXREhfQ0kiLCJ2ZXJzaW9uIjoiMS4wLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoid2RoX2F0bW9zcGhlcmljX2ZyZWUifV0sInRva2VuX3R5cGUiOiJhcGlLZXkiLCJpYXQiOjE3NDc0NjUyMDIsImp0aSI6ImE5OGRjOWM1LWMwZWYtNDk4ZS05ZjNmLTJiZWFmNTFlNGFjZiJ9.FHUgOdN9rimY0X4njSktGmee--14LniJpb6Chb0l6vO5wm1qQ08IN66dcTwL9gntluVpofux6zjfyaiW2l82abbw8cGm5lwQcO8GSrczFmobdwLUFxcvRcEMb1uZ4RRHn6wCmtyL2SwVSj1gFXd_91DhghR-OTUZBfsXxfNNnuQOPRDMG-JesSzn9xDygnLlrjF7UTKG7jjG_uz7x8UaXvL4yLA_2hDkyzsS4Us_HBwQZAzfq5IxEq6UCz34jrC6q60ojMWsQStd4FdPxQJ79xzTz0T9iNcOr4WWS4zgLpRpCDalOI16qEnGWKRt3DL-iPE1msx3LyZhx7Xob6WtnA==" # Replace with your actual API key
base_api_url = "https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0"
output_base_dir = "metoffice_downloads" # Base folder for all downloads
# --- End Configuration ---

# Headers for JSON API calls (listing orders, getting file IDs)
json_headers = {
    "accept": "application/json",
    "apikey": api_key
}

# Headers for binary data API calls (downloading GRIB files)
binary_headers = {
    "accept": "*/*", # Or 'application/octet-stream', 'application/x-grib'
    "apikey": api_key
}

def get_order_ids(url, headers_json):
    """Fetches and returns a dictionary of order IDs with their indices."""
    order_map = {}
    print("Attempting to fetch order IDs from:", url)
    try:
        response = requests.get(url, headers=headers_json)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        order_data = response.json()

        if isinstance(order_data, dict) and 'orders' in order_data and isinstance(order_data['orders'], list):
            for i, order in enumerate(order_data['orders']):
                if isinstance(order, dict) and 'orderId' in order:
                    order_map[i + 1] = order['orderId'] # Store with 1-based index
        else:
            print("Could not find the 'orders' list in the expected format.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching order IDs: {e}")
        if response is not None:
            print(f"Response status: {response.status_code}, body: {response.text}")
    except json.JSONDecodeError:
        print("Error decoding JSON from order ID response.")
    return order_map

def download_and_concatenate_files(order_id, base_url, headers_json, headers_binary, output_dir):
    """
    Downloads binary files for a given order ID, saves them individually,
    and then concatenates them into a single file.
    """
    order_detail_url = f"{base_url}/orders/{order_id}/latest"
    print(f"\nFetching file IDs for order {order_id} from: {order_detail_url}")

    temp_files = [] # To store paths of downloaded individual files
    
    try:
        response = requests.get(order_detail_url, headers=headers_json)
        response.raise_for_status()
        met_office_data = response.json()

        if "orderDetails" in met_office_data and "files" in met_office_data["orderDetails"]:
            file_infos = met_office_data["orderDetails"]["files"]
            print(f"Found {len(file_infos)} files for order {order_id}. Starting download...")

            for i, file_info in enumerate(file_infos):
                if "fileId" in file_info:
                    raw_file_id = file_info["fileId"]
                    # URL-encode the fileId before including it in the URL
                    encoded_file_id = quote(raw_file_id, safe='') # safe='' means encode all special chars
                    
                    download_url = f"{base_url}/orders/{order_id}/latest/{encoded_file_id}/data"
                    file_path = os.path.join(output_dir, f"{raw_file_id}.grib") # Use raw_file_id for filename

                    print(f"  Downloading file {i+1}/{len(file_infos)}: {raw_file_id}")
                    print(f"    (URL: {download_url})") # Print the actual URL being used

                    try:
                        file_response = requests.get(download_url, headers=headers_binary, stream=True)
                        file_response.raise_for_status()
                        
                        with open(file_path, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        temp_files.append(file_path)
                        print(f"  Successfully downloaded {raw_file_id}")

                    except requests.exceptions.RequestException as e:
                        print(f"  Error downloading {raw_file_id}: {e}")
                        if file_response is not None:
                            print(f"  Response status: {file_response.status_code}, body: {file_response.text}")
                    except IOError as e:
                        print(f"  Error writing file {raw_file_id} to disk: {e}")
                else:
                    print(f"  Warning: Found a file entry without 'fileId' for order {order_id}.")
        else:
            print(f"No file IDs found in the expected structure for order {order_id}.")
            return False # Indicate no files were processed

    except requests.exceptions.RequestException as e:
        print(f"Error fetching file list for order {order_id}: {e}")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON for file list of order {order_id}.")
        return False

    # --- Concatenate downloaded files ---
    if temp_files:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        concatenated_filename = f"{order_id}_{timestamp}.grib"
        concatenated_filepath = os.path.join(output_dir, concatenated_filename)

        print(f"\nConcatenating {len(temp_files)} files into: {concatenated_filepath}")
        try:
            with open(concatenated_filepath, 'wb') as outfile:
                for fname in temp_files:
                    with open(fname, 'rb') as infile:
                        shutil.copyfileobj(infile, outfile) # Efficiently copy binary data
                    os.remove(fname) # Clean up individual files after concatenation
            print(f"Successfully concatenated files for order {order_id}.")
            return True
        except IOError as e:
            print(f"Error during concatenation for order {order_id}: {e}")
            return False
    else:
        print("No files were successfully downloaded to concatenate.")
        return False


def main():
    """Main function to list orders, prompt for selection, and download/concatenate files."""
    print("--- Listing Available Orders ---")
    order_map = get_order_ids(f"{base_api_url}/orders", json_headers)

    if not order_map:
        print("No orders found or unable to retrieve orders. Exiting.")
        return

    for index, order_id in order_map.items():
        print(f"{index}. {order_id}")

    while True:
        try:
            choice = input("\nEnter the number of the order you want to download (or 'q' to quit): ")
            if choice.lower() == 'q':
                print("Exiting.")
                break

            selected_index = int(choice)
            if selected_index in order_map:
                selected_order_id = order_map[selected_index]
                print(f"\nPreparing to download files for Order: {selected_order_id}")

                # Create timestamped sub-folder
                current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                # Removed "metoffice/" from the folder name string to rely solely on os.path.join
                # The root folder is output_base_dir, which is 'metoffice_downloads'
                sub_folder_name = f"{selected_order_id}_{current_timestamp}"
                full_output_path = os.path.join(output_base_dir, sub_folder_name)
                
                os.makedirs(full_output_path, exist_ok=True) # Create if it doesn't exist
                print(f"Created/Ensured directory: {full_output_path}")

                download_and_concatenate_files(selected_order_id, base_api_url, json_headers, binary_headers, full_output_path)
                
                print(f"\nProcess complete for order {selected_order_id}.")
                break # Exit after processing the selected order
            else:
                print("Invalid order number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()