import json
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_quiz(text, num_questions, num_options):
    prompt = f"""
Create {num_questions} multiple-choice questions from the text below.

Each question must have exactly {num_options} options.

Return ONLY valid JSON:
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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content
        return json.loads(output)

    except Exception as e:
        print("Error:", e)
        return []