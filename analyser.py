import base64
import json
import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are an expert dermatology AI assistant. Analyse the facial skin in the image provided and return a JSON object with the following structure:

{
  "skin_type": "oily|dry|combination|normal|sensitive",
  "overall_health_score": <integer 1-10>,
  "detected_concerns": [
    {
      "name": "<concern name>",
      "severity": "mild|moderate|severe",
      "description": "<1-2 sentence description>"
    }
  ],
  "positive_attributes": ["<attribute>", ...],
  "recommendations": [
    {
      "category": "cleanser|moisturizer|sunscreen|treatment|lifestyle|diet",
      "advice": "<specific actionable advice>"
    }
  ],
  "summary": "<2-3 sentence overall assessment>"
}

Rules:
- Return ONLY the JSON object, no markdown fences, no extra text.
- If no face is visible, return {"error": "No face detected in the image"}.
- If image quality is too low, return {"error": "Image quality too low for analysis"}.
- detected_concerns may be an empty list if skin looks healthy.
- Be specific and clinically accurate but avoid alarmist language."""


def analyse_skin(image_bytes: bytes, media_type: str) -> dict:
    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    },
                },
                {"type": "text", "text": "Analyse this facial skin image."},
            ],
        }],
    )

    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)
