import os
import requests
import urllib.parse

# ======================
# Primary: Pollinations
# ======================
POLLINATIONS_BASE = "https://image.pollinations.ai/prompt"

# ======================
# Fallback: Hugging Face
# ======================
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


def generate_image(prompt, output_path):
    """
    Try Pollinations first (no auth, free).
    If it fails, fallback to Hugging Face Inference API (free tier).
    """

    try:
        print("🖼️ Trying Pollinations AI...")
        return generate_with_pollinations(prompt, output_path)
    except Exception as e:
        print(f"⚠️ Pollinations failed: {e}")
        print("🔁 Falling back to Hugging Face...")
        return generate_with_huggingface(prompt, output_path)


def generate_with_pollinations(prompt, output_path):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"{POLLINATIONS_BASE}/{encoded_prompt}?width=512&height=512&seed=42"

    response = requests.get(url, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"Pollinations HTTP {response.status_code}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def generate_with_huggingface(prompt, output_path):
    hf_token = os.getenv("HF_API_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_API_TOKEN not set (required for fallback)")

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Accept": "image/png",
    }

    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Hugging Face failed: {response.status_code} → {response.text}"
        )

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
