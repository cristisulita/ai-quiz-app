import json
import re
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_quiz(text, num_questions, num_options):
    prompt = f"""
Create {num_questions} multiple-choice questions.

Return ONLY JSON array:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ..."],
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

        # DEBUG
        st.text_area("DEBUG AI OUTPUT", output, height=300)

        # Clean markdown
        clean_output = re.sub(r"```json|```", "", output).strip()

        quiz = json.loads(clean_output)
        return quiz

    except Exception as e:
        import traceback
        traceback.print_exc()
        st.error(f"Error: {e}")
        return []