import json
import re
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_quiz(text, num_questions, num_options, difficulty):
 difficulty_rules = {
    "Easy": """
- Questions should be simple and direct
- Focus on basic facts and definitions
- Answers should be obvious from the text
""",
    "Medium": """
- Questions should require understanding
- Include explanations or relationships
- Avoid trivial questions
""",
    "Hard": """
- Questions should require reasoning or inference
- May combine multiple ideas from the text
- Include tricky or similar answer choices
"""
}

prompt = f"""
You are a teacher creating a quiz.

Create {num_questions} multiple-choice questions.

Each question must have EXACTLY {num_options} options.

Difficulty level: {difficulty}

Rules:
{difficulty_rules[difficulty]}

IMPORTANT:
- Each question must be UNIQUE
- Do NOT repeat ideas
- Cover different parts of the text
- The number of options MUST be exactly {num_options}

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