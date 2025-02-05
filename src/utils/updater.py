import requests
from version.version import CURRENT_VERSION, GITHUB_USER, GITHUB_REPO

def check_latest_version():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    try:
        print(f"Checking for updates at {url}")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            latest_version = data["tag_name"]
            # Optionally, you can also get asset download URL if needed:
            assets = data.get("assets", [])
            download_url = assets[0]["browser_download_url"] if assets else None
            return latest_version, download_url
        else:
            # log response body andstatus code
            print(f"Failed to check for updates. Response body: {response.text}, Status code: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error while checking for updates: {e}")
        return None, None

def install_update(download_url):
    if not download_url:
        print("No update available.")
        return

    try:
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            # Save the file to a temporary path (here we save it as update.zip)
            update_file = "update.zip"
            with open(update_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Update downloaded to {update_file}")
        else:
            print("Failed to download update.")
    except Exception as e:
        print(f"Error while downloading update: {e}")

