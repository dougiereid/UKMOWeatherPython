import requests
import json

# Define the API endpoint URL
api_url = "https://data.hub.api.metoffice.gov.uk/atmospheric-models/1.0.0/orders"

# Define the API key
# WARNING: Hardcoding API keys directly in scripts is generally NOT recommended for security reasons,
# especially if the script is shared or used in a production environment.
# Consider using environment variables or a configuration file to store your API key securely.
api_key = "eyJ4NXQjUzI1NiI6Ik5XVTVZakUxTkRjeVl6a3hZbUl4TkdSaFpqSmpOV1l6T1dGaE9XWXpNMk0yTWpRek5USm1OVEE0TXpOaU9EaG1NVFJqWVdNellXUm1ZalUyTTJJeVpBPT0iLCJraWQiOiJnYXRld2F5X2NlcnRpZmljYXRlX2FsaWFzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ==.eyJzdWIiOiJkb3VnaWVAZG91Z2llcmVpZC5jby51a0BjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6ImRvdWdpZUBkb3VnaWVyZWlkLmNvLnVrIiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJhdG1vc3BoZXJpYy05MjZkYzg4Yy04ZTkxLTQxYzEtOTA1NC0wYTE4ZmUwMTZlMGUiLCJpZCI6MTIxMzAsInV1aWQiOiI1NzFkYzBiMy1iNDE0LTRmODgtOGZjNi1mZWUwZjMwMTU5M2EifSwiaXNzIjoiaHR0cHM6XC9cL2FwaS1tYW5hZ2VyLmFwaS1tYW5hZ2VtZW50Lm1ldG9mZmljZS5jbG91ZDo0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyJ3ZGhfYXRtb3NwaGVyaWNfZnJlZSI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0Ijoic2VjIn19LCJrZXl0eXBlIjoiUFJPRFVDVElPTiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6ImF0bW9zcGhlcmljLW1vZGVscyIsImNvbnRleHQiOiJcL2F0bW9zcGhlcmljLW1vZGVsc1wvMS4wLjAiLCJwdWJsaXNoZXIiOiJXREhfQ0kiLCJ2ZXJzaW9uIjoiMS4wLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoid2RoX2F0bW9zcGhlcmljX2ZyZWUifV0sInRva2VuX3R5cGUiOiJhcGlLZXkiLCJpYXQiOjE3NDc0NjUyMDIsImp0aSI6ImE5OGRjOWM1LWMwZWYtNDk4ZS05ZjNmLTJiZWFmNTFlNGFjZiJ9.FHUgOdN9rimY0X4njSktGmee--14LniJpb6Chb0l6vO5wm1qQ08IN66dcTwL9gntluVpofux6zjfyaiW2l82abbw8cGm5lwQcO8GSrczFmobdwLUFxcvRcEMb1uZ4RRHn6wCmtyL2SwVSj1gFXd_91DhghR-OTUZBfsXxfNNnuQOPRDMG-JesSzn9xDygnLlrjF7UTKG7jjG_uz7x8UaXvL4yLA_2hDkyzsS4Us_HBwQZAzfq5IxEq6UCz34jrC6q60ojMWsQStd4FdPxQJ79xzTz0T9iNcOr4WWS4zgLpRpCDalOI16qEnGWKRt3DL-iPE1msx3LyZhx7Xob6WtnA=="

# Define the headers
headers = {
    "accept": "application/json",
    "apikey": api_key
}

try:
    # Make the GET request
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        order_data = response.json()

        # Extract and print only the orderIds
        print("--- Order IDs ---")
        if isinstance(order_data, dict) and 'orders' in order_data and isinstance(order_data['orders'], list):
            if order_data['orders']: # Check if the list is not empty
                for order in order_data['orders']:
                    if isinstance(order, dict) and 'orderId' in order:
                        print(order['orderId'])
                    else:
                        print("Warning: Found an item in 'orders' that is not a dictionary or is missing 'orderId'.")
            else:
                print("The 'orders' list is empty.")
        else:
            print("Could not find the 'orders' list in the expected format.")

    else:
        # Print an error message if the request was not successful
        print(f"Error: Failed to retrieve order information. Status code: {response.status_code}")
        print("Response body:")
        print(response.text)

except requests.exceptions.RequestException as e:
    # Handle any request errors (e.g., network issues)
    print(f"An error occurred during the request: {e}")
except Exception as e:
    # Catch any other potential errors during processing
    print(f"An unexpected error occurred: {e}")