import requests
import json

# Define your API key
# It's highly recommended to use environment variables for API keys in production
# For example: api_key = os.getenv("METOFFICE_API_KEY")
api_key = "eyJ4NXQjUzI1NiI6Ik5XVTVZakUxTkRjeVl6a3hZbUl4TkdSaFpqSmpOV1l6T1dGaE9XWXpNMk0yTWpRek5USm1OVEE0TXpOaU9EaG1NVFJqWVdNellXUm1ZalUyTTJJeVpBPT0iLCJraWQiOiJnYXRld2F5X2NlcnRpZmljYXRlX2FsaWFzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ==.eyJzdWIiOiJkb3VnaWVAZG91Z2llcmVpZC5jby51a0BjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6ImRvdWdpZUBkb3VnaWVyZWlkLmNvLnVrIiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJhdG1vc3BoZXJpYy05MjZkYzg4Yy04ZTkxLTQxYzEtOTA1NC0wYTE4ZmUwMTZlMGUiLCJpZCI6MTIxMzAsInV1aWQiOiI1NzFkYzBiMy1iNDE0LTRmODgtOGZjNi1mZWUwZjMwMTU5M2EifSwiaXNzIjoiaHR0cHM6XC9cL2FwaS1tYW5hZ2VyLmFwaS1tYW5hZ2VtZW50Lm1ldG9mZmljZS5jbG91ZDo0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyJ3ZGhfYXRtb3NwaGVyaWNfZnJlZSI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0Ijoic2VjIn19LCJrZXl0eXBlIjoiUFJPRFVDVElPTiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6ImF0bW9zcGhlcmljLW1vZGVscyIsImNvbnRleHQiOiJcL2F0bW9zcGhlcmljLW1vZGVsc1wvMS4wLjAiLCJwdWJsaXNoZXIiOiJXREhfQ0kiLCJ2ZXJzaW9uIjoiMS4wLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoid2RoX2F0bW9zcGhlcmljX2ZyZWUifV0sInRva2VuX3R5cGUiOiJhcGlLZXkiLCJpYXQiOjE3NDc0NjUyMDIsImp0aSI6ImE5OGRjOWM1LWMwZWYtNDk4ZS05ZjNmLTJiZWFmNTFlNGFjZiJ9.FHUgOdN9rimY0X4njSktGmee--14LniJpb6Chb0l6vO5wm1qQ08IN66dcTwL9gntluVpofux6zjfyaiW2l82abbw8cGm5lwQcO8GSrczFmobdwLUFxcvRcEMb1uZ4RRHn6wCmtyL2SwVSj1gFXd_91DhghR-OTUZBfsXxfNNnuQOPRDMG-JesSzn9xDygnLlrjF7UTKG7jjG_uz7x8UaXvL4yLA_2hDkyzsS4Us_HBwQZAzfq5IxEq6UCz34jrC6q60ojMWsQStd4FdPxQJ79xzTz0T9iNcOr4WWS4zgLpRpCDalOI16qEnGWKRt3DL-iPE1msx3LyZhx7Xob6WtnA==" # Replace with your actual API key

# Define the base URL for the API
base_api_url = "https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0"

# Define the headers
headers = {
    "accept": "application/json",
    "apikey": api_key
}

def get_order_ids(url, headers):
    """Fetches and returns a list of all order IDs."""
    order_ids = []
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        order_data = response.json()

        if isinstance(order_data, dict) and 'orders' in order_data and isinstance(order_data['orders'], list):
            for order in order_data['orders']:
                if isinstance(order, dict) and 'orderId' in order:
                    order_ids.append(order['orderId'])
        else:
            print("Could not find the 'orders' list in the expected format.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching order IDs: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON from order ID response.")
    return order_ids

def get_file_ids_for_order(order_id, base_url, headers):
    """Fetches and returns a list of file IDs for a given order ID."""
    file_ids = []
    order_detail_url = f"{base_url}/orders/{order_id}/latest"
    try:
        response = requests.get(order_detail_url, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        met_office_data = response.json()

        if "orderDetails" in met_office_data and "files" in met_office_data["orderDetails"]:
            for file_info in met_office_data["orderDetails"]["files"]:
                if "fileId" in file_info:
                    file_ids.append(file_info["fileId"])
        else:
            print(f"No file IDs found in the expected structure for order {order_id}.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file IDs for order {order_id}: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file ID response for order {order_id}.")
    return file_ids

def main():
    """Main function to orchestrate the fetching and URL creation."""
    all_generated_urls = {}

    print("Fetching all order IDs...")
    order_ids = get_order_ids(f"{base_api_url}/orders", headers)

    if not order_ids:
        print("No order IDs found to process.")
        return

    print(f"Found {len(order_ids)} order IDs. Now fetching file IDs and constructing URLs...")
    for order_id in order_ids:
        print(f"\nProcessing order ID: {order_id}")
        file_ids = get_file_ids_for_order(order_id, base_api_url, headers)
        
        if file_ids:
            urls_for_this_order = []
            for file_id in file_ids:
                # Construct the full URL
                full_url = f"{base_api_url}/orders/{order_id}/latest/{file_id}"
                urls_for_this_order.append(full_url)
            all_generated_urls[order_id] = urls_for_this_order
            print(f"Generated {len(urls_for_this_order)} URLs for order {order_id}.")
        else:
            print(f"No file IDs found for order {order_id}.")

    print("\n--- All Generated URLs ---")
    if all_generated_urls:
        for order_id, urls in all_generated_urls.items():
            print(f"Order ID: {order_id}")
            for url in urls:
                print(f"  {url}")
    else:
        print("No URLs were generated.")

if __name__ == "__main__":
    main()