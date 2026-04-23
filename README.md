# Skin Analyser

An AI-powered facial skin analysis tool built with FastAPI and Claude Vision.

Upload a photo of your face and get a detailed analysis including skin type, detected concerns, positive attributes, and personalised recommendations.

## Features

- Drag-and-drop or click-to-upload image interface
- Supports JPEG, PNG, WebP, GIF (max 10 MB)
- Returns:
  - Skin type (oily, dry, combination, normal, sensitive)
  - Overall health score (1–10)
  - Detected concerns with severity levels
  - Positive skin attributes
  - Actionable recommendations by category

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/kanekargauri/skin-analyser.git
cd skin-analyser
```

**2. Install dependencies**
```bash
pip3 install -r requirements.txt
```

**3. Set your Anthropic API key**
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Get a key at [console.anthropic.com](https://console.anthropic.com).

**4. Run the server**
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**5. Open in browser**
```
http://localhost:8000
```

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — API server
- [Claude claude-opus-4-7](https://anthropic.com) — Vision model for skin analysis
- Vanilla HTML/CSS/JS — frontend
