import requests
import urllib.parse

def get_token(init_data, verify_ssl=True):
    # URL encode the init_data
    encoded_init_data = urllib.parse.quote(init_data, safe='')

    url = f"https://api.pixelfarm.app/user/login?auth_data={encoded_init_data}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "Referer": "https://pixelfarm.app/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    try:
        # Attempt to request with the current SSL verification setting
        response = requests.get(url, headers=headers, verify=verify_ssl)

        if response.status_code == 200:
            return response.json().get('data')
        else:
            print(f"Failed to fetch token. Status code: {response.status_code}")
            return None

    except requests.exceptions.SSLError as ssl_error:
        # If there is an SSL error and verify_ssl is True, retry without SSL verification
        if verify_ssl:
            print(f"SSL error encountered: {ssl_error}. Retrying with SSL verification disabled.")
            return get_token(init_data, verify_ssl=False)
        else:
            print(f"Request failed with SSL disabled: {ssl_error}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
def fetch_user_data(token):
    url = "https://api.pixelfarm.app/user"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch user data: {response.status_code}")

def claim_rewards(token):
    url = "https://api.pixelfarm.app/user/claim"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        return response.json().get('messages')
    else:
        raise Exception(f"Failed to claim rewards. Status code: {response.status_code}, Response: {response.text}")