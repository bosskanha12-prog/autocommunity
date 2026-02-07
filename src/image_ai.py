import requests, os, base64

def generate_image(prompt, output="assets/generated/today.png"):
    headers = {
        "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
        "Accept": "application/json"
    }

    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 512,
        "width": 512,
        "steps": 30
    }

    r = requests.post(
        "https://api.stability.ai/v1/generation/sdxl-1-0/text-to-image",
        headers=headers,
        json=payload
    )

    image_data = r.json()["artifacts"][0]["base64"]
    with open(output, "wb") as f:
        f.write(base64.b64decode(image_data))
