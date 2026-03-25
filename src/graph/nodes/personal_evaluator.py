# src/graph/nodes/personal_evaluator.py
import json
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState


def personal_info_extractor(state: ResumeState) -> ResumeState:
    print("Personal Info Extractor called")

    resume_text = state.get("resume_text", "")
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template("""
Extract personal contact information from the resume below.
Return ONLY a valid JSON object with these keys:
- "name": string (full name)
- "email": string (email address) 
- "phone": string (phone number)
- "languages": array of strings (languages spoken)

If any field is not found, use "" for strings and [] for arrays.
Return ONLY the JSON, no other text.

Resume Text:
{resume}
""")

    messages = prompt.format_messages(resume=resume_text)
    response = llm.invoke(messages)

    # Parse the JSON response ourselves — no Groq tool validation
    try:
        raw = response.content.strip()
        # Handle potential markdown code fences
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0]
        data = json.loads(raw)
    except (json.JSONDecodeError, IndexError):
        data = {}

    return {
        "name": data.get("name") or "",
        "email": data.get("email") or "",
        "phone_number": data.get("phone") or "",
        "languages": data.get("languages") or [],
    }