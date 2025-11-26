import os
import requests


def download(url, folder, name=None):
    try:
        with requests.get(url, stream=True) as response:
            file = name or url.split("/")[-1]
            response.raise_for_status()
            if not os.path.exists(folder):
                os.mkdir(folder)
            out = os.path.join(folder, file)
            with open(out, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return out
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None
