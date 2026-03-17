import json
import os
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI

def gen_mcqs(text: str, llm, num_questions: int = 5) -> List[Dict]:
    \"\"\"Generate MCQs from text using LLM.\"\"\"
    prompt = f\"\"\"Generate {num_questions} multiple choice questions from the following text.
Each question should have 4 options (A,B,C,D), one correct.
Return ONLY valid JSON list of objects, each: {{\"question\": \"...\", \"options\": {{\"A\": \"...\", \"B\": \"...\", \"C\": \"...\", \"D\": \"...\"}}, \"correct\": \"A\"}}
Text: {text[:4000]}
\"\"\"

    try:
        msg = llm.invoke(prompt)
        response = msg.content.strip()
        mcqs = json.loads(response)
        return mcqs
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

