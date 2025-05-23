import os
import requests

# Rescale API URL (for Rescale Japan platform)
BASE_URL = "https://platform.rescale.jp/api/v2/"

# グローバル設定オブジェクト
class RescaleConfig:
    def __init__(self, api_token=None, job_id=None):
        self.api_token = api_token or os.environ.get('RESCALE_API_KEY')
        self.job_id = job_id or os.environ.get('RESCALE_JOB_ID')
        if not self.api_token:
            raise ValueError("API token is required. Set RESCALE_API_KEY or provide it explicitly.")
        if not self.job_id:
            print("Warning: JOB ID is not set. Set RESCALE_JOB_ID or provide it if needed.")

# インスタンス（ライブラリ利用者が明示的に初期化）
rescale_config = None

def init_config(api_token=None, job_id=None):
    global rescale_config
    rescale_config = RescaleConfig(api_token, job_id)

def check_api_key():
    if not rescale_config:
        raise RuntimeError("Rescale config not initialized. Call init_config() first.")

    endpoint = BASE_URL + "users/me/"
    headers = {
        "Authorization": "Token " + rescale_config.api_token,
        "Content-Type": "application/json"
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        print("API key is valid!")
        user_details = response.json()
        print("User:", user_details.get("username"))
        print("Email:", user_details.get("email"))
    elif response.status_code == 401:
        print("Invalid API key! Please check your API key and try again.")
    else:
        print("Failed to check API key. Status code:", response.status_code)
        print("Response:", response.text)

