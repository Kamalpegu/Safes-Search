import os
import requests
import base64
import json

def get_safe_links(url):
    api_key = os.environ.get("VIRUSTOTAL_API_KEY")
    if api_key is None:
        return {"error": "Environment variable VIRUSTOTAL_API_KEY not set"}

    url_check_endpoint = "https://www.virustotal.com/api/v3/urls/"
    encoded_url = base64.urlsafe_b64encode(url.encode()).decode().replace("=", "")

    headers = {"x-apikey": api_key}

    try:
        response = requests.get(url_check_endpoint + encoded_url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors

        try:
            data = response.json()
            if 'data' not in data:
                return {'error': 'Invalid VirusTotal response: "data" key missing'}
            if 'attributes' not in data['data']:
                return {'error': 'Invalid VirusTotal response: "attributes" key missing'}
            if 'last_analysis_stats' not in data['data']['attributes']:
              return {'error': 'Invalid VirusTotal response: "last_analysis_stats" key missing'}


            return data['data']['attributes']['last_analysis_stats']

        except json.JSONDecodeError as e:
            return {"error": f"Error decoding JSON response: {e}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error communicating with VirusTotal: {e}"}
        
