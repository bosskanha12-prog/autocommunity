import requests
import os

STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/sdxl"


def generate_image(prompt, output_path):
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise RuntimeError("STABILITY_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/png"
    }

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "width": (None, "512"),
        "height": (None, "512"),
        "samples": (None, "1"),
        "cfg_scale": (None, "7"),
    }

    response = requests.post(
        STABILITY_URL,
        headers=headers,
        files=files,
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Stability API failed: {response.status_code} → {response.text}"
        )

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
