import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def evaluate_writing(text):

    prompt = f"""
You are an English evaluator.

Evaluate the following English writing.

Return ONLY valid JSON.

The JSON format must be exactly:

{{
    "overall_score": 85,
    "grammar": "...",
    "vocabulary": "...",
    "suggestion": "..."
}}

Writing:

{text}
"""

    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    # Menghapus markdown ```json jika ada
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    return json.loads(content)