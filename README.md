# AutoCommunity

Automation for generating a daily YouTube Community-style poll post with an AI image.

## Project structure

- `src/main.py` – orchestrates the daily flow.
- `src/rotation.py` – deterministic daily rotation across configured lists.
- `src/image_ai.py` – image generation (Pollinations primary, Hugging Face fallback).
- `src/poll_builder.py` – formats poll text.
- `src/youtube.py` – publishes post via YouTube Data API.
- `config/rotation.yaml` – rotating topics/styles.
- `config/image_polls.yaml` – poll questions/options.
- `config/prompts.yaml` – prompt templates.
- `assets/generated/` – generated images.

## Workflow

1. Load YAML configs.
2. Pick the day’s topic/style/poll using `rotate()`.
3. Build image prompt and generate image to `assets/generated/today.png`.
4. Build poll text from selected question/options.
5. Publish a bulletin/community activity to YouTube.

## What was broken and what was fixed

### 1) Runtime crash in post upload call
- **Problem:** `main.py` called `upload_community_post(text=..., image_path=...)`, but `upload_community_post` only accepted `text`.
- **Impact:** Immediate `TypeError` before publish step.
- **Fix:** Updated `upload_community_post` signature to accept `image_path=None` for compatibility.

### 2) Hidden failure mode in rotation
- **Problem:** `rotate()` used modulo on `len(items)` with no guard.
- **Impact:** Empty config lists would raise a less-clear `ZeroDivisionError`.
- **Fix:** Added explicit non-empty validation and a clear `ValueError`.

### 3) Unused/fragile OpenAI dependency in text helper
- **Problem:** `text_ai.py` imported and configured `openai` but didn’t use it.
- **Impact:** Extra dependency burden and potential import failure in minimal environments.
- **Fix:** Removed unused import and env wiring.

## Suggested improvements

- Add a `--dry-run` mode in `main.py` to test generation without posting.
- Add retry/backoff around external API calls.
- Add unit tests for rotation, poll formatting, and YouTube payload assembly.
- Consider provider abstraction so image and post providers can be swapped cleanly.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables:

- `YOUTUBE_REFRESH_TOKEN`
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `HF_API_TOKEN` (only needed if Pollinations fails)

Run:

```bash
python src/main.py
```
