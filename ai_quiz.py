import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quiz(text, num_questions, num_options):
    prompt = f"""
Create {num_questions} multiple-choice questions from the text below.

Each question must have exactly {num_options} options.

Return ONLY valid JSON in this format:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "..."
  }}
]

Text:
{text[:3000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # cheap + reliable
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output = response.choices[0].message.content

        # Parse JSON safely
        quiz = json.loads(output)
        return quiz

    except Exception as e:
        print("Error:", e)
        return []