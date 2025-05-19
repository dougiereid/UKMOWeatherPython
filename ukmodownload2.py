import requests
import os
from urllib.parse import urlencode, quote_plus
import json  # Import the json module

def download_metoffice_data(api_key, order_id, download_path="."):
    """
    Downloads data files for a given order from the Met Office DataHub.

    Args:
        api_key (str): Your Met Office DataHub API key.
        order_id (str): The ID of the order you want to download.
        download_path (str, optional): The directory where files will be saved. Defaults to the current directory.
    """
    # Base URL for the Met Office DataHub API
    base_url = "https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0"

    # Construct the URL to get the latest files for the order
    order_url = f"{base_url}/orders/{order_id}/latest"
    print(f"Fetching file list from: {order_url}")  # Helpful for debugging

    try:
        # Make the request to get the file list
        response = requests.get(order_url, headers={"apikey": api_key})
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        text_response = response.text #get the text
        files_data = json.loads(text_response) #convert the text to json

        if not files_data:
            print(f"No files found for order ID: {order_id}")
            return

        print(f"Found {len(files_data)} files.")  # Inform the user

        # Iterate through each file and download it
        for file_info in files_data:
            file_id = file_info["fileId"]
            file_name = file_info["name"]  # Get filename
            # Construct the URL to download the file's data.  Crucially use quote_plus
            download_url = f"{base_url}/orders/{order_id}/latest/{quote_plus(file_id)}/data"

            print(f"Downloading: {file_name} from {download_url}")  # Show download URL
            try:
                # Make the request to download the file
                file_response = requests.get(download_url, headers={"apikey": api_key}, stream=True)  # stream = True is important for large files
                file_response.raise_for_status()

                # Create the full file path
                file_path = os.path.join(download_path, file_name)

                # Write the file data to disk in chunks
                with open(file_path, "wb") as f:
                    for chunk in file_response.iter_content(chunk_size=8192):  # 8KB chunks
                        f.write(chunk)
                print(f"Downloaded successfully to: {file_path}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading file {file_name}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching file list: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Unable to decode JSON response.  Check the API key and order ID.  Error Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    #  Replace with your actual API key and order ID.
    #  IMPORTANT: Storing API keys directly in the script is NOT recommended for security.
    #  Use environment variables or config files instead.
    api_key = "eyJ4NXQjUzI1NiI6Ik5XVTVZakUxTkRjeVl6a3hZbUl4TkdSaFpqSmpOV1l6T1dGaE9XWXpNMk0yTWpRek5USm1OVEE0TXpOaU9EaG1NVFJqWVdNellXUm1ZalUyTTJJeVpBPT0iLCJraWQiOiJnYXRld2F5X2NlcnRpZmljYXRlX2FsaWFzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ==.eyJzdWIiOiJkb3VnaWVAZG91Z2llcmVpZC5jby51a0BjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6ImRvdWdpZUBkb3VnaWVyZWlkLmNvLnVrIiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJhdG1vc3BoZXJpYy05MjZkYzg4Yy04ZTkxLTQxYzEtOTA1NC0wYTE4ZmUwMTZlMGUiLCJpZCI6MTE4MTUsInV1aWQiOiIyN2FiMjJhZi0xNDU0LTQ2MWQtYWYyMy04MjRiMzM2MjkyZjgifSwiaXNzIjoiaHR0cHM6XC9cL2FwaS1tYW5hZ2VyLmFwaS1tYW5hZ2VtZW50Lm1ldG9mZmljZS5jbG91ZDo0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyJ3ZGhfYXRtb3NwaGVyaWNfZnJlZSI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0Ijoic2VjIn19LCJrZXl0eXBlIjoiUFJPRFVDVElPTiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6ImF0bW9zcGhlcmljLW1vZGVscyIsImNvbnRleHQiOiJcL2F0bW9zcGhlcmljLW1vZGVsc1wvMS4wLjAiLCJwdWJsaXNoZXIiOiJXREhfQ0kiLCJ2ZXJzaW9uIjoiMS4wLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoid2RoX2F0bW9zcGhlcmljX2ZyZWUifV0sInRva2VuX3R5cGUiOiJhcGlLZXkiLCJpYXQiOjE3NDY2MzI4NDIsImp0aSI6ImJiNTVmOGZjLTRkMWQtNDBmYy1hMzFjLTY2MWYzZWE2YjlmYyJ9.QUsfZkvi3Vmxpi8sUh65UUj3F7Qs_0zMIXd_FeaeX4HWZwgjH76pFkPA8Y9m9FdFge8KFRsSfgMU46jA3E0Q2Tzb534oNTPc_oteTQ2QwLXAKMKqIpW_su6I3AIXs3CVVMSz_TgIVBQ1wZ7qaP8yY9QU03Jgky4bB2jFrnoeNzA79aUDMDnIMHs-nwJa5HK8WbFG-ksA24ywj2p0rv6Jtw8jkwzHdzDzDce-RLgctrrzNnfYQs_RNhQSByIjGkCVK84m3wB6Mr5qn0piiwK4IVfHv7hG5qM9fWZ8ZTmM2caYnG8v8_84f5QwqGGeG5iMWJOi-CXkyUbBQVQDmq38OQ=="  # Replace with your actual API key
    order_id = "061311791874"  # Replace with your actual order ID

    # Specify the directory where you want to save the downloaded files
    download_path = "metoffice_data"  # Create a folder
    os.makedirs(download_path, exist_ok=True)  # Ensure the directory exists

    download_metoffice_data(api_key, order_id, download_path)
    print("Download process complete.")


