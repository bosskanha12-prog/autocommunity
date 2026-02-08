import requests
import os
import base64

STABILITY_URL = "https://api.stability.ai/v1/generation/sdxl-1-0/text-to-image"


def generate_image(prompt, output_path):
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise RuntimeError("STABILITY_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 512,
        "width": 512,
        "steps": 30,
        "samples": 1
    }

    r = requests.post(STABILITY_URL, headers=headers, json=payload)

    # 🔴 HARD CHECK
    if r.status_code != 200:
        raise RuntimeError(
            f"Stability API failed: {r.status_code} → {r.text}"
        )

    data = r.json()

    # 🔴 HARD CHECK
    if "artifacts" not in data:
        raise RuntimeError(
            f"Unexpected Stability response: {data}"
        )

    image_base64 = data["artifacts"][0]["base64"]
    image_bytes = base64.b64decode(image_base64)

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path
