import json
import re
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_quiz(text, num_questions, num_options):
    prompt = f"""
You are a teacher.
Create {num_questions} multiple-choice questions.

Each question must have EXACTLY {num_options} options.

Return ONLY JSON array:
[
  {{
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ..."],
    "answer": "..."
  }}
]

IMPORTANT:
- The number of options MUST be exactly {num_options}
- Do NOT add extra options
- Each question must be UNIQUE
- Do NOT repeat questions
- Cover different parts of the text
- Avoid repeating ideas or wording between questions.
If you do not follow the exact number of options, the answer is invalid.

Text:
{text[:3000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
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