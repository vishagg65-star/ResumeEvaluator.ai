
import json
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState


def experience_evaluator(state: ResumeState) -> ResumeState:
    print("Experience Evaluator called")

    resume_text = state.get("resume_text", "")
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template("""
You are an expert technical recruiter and data analyst. Your task is to extract and precisely calculate professional experience from a resume.

### Calculation Rules:
1. **Total Experience (Years)**: 
   - Identify every unique professional job entry (EXCLUDE internships, volunteer work, and education).
   - For each entry, find the Start Date and End Date. 
   - If the End Date is "Present", use the current date (March 2026).
   - Calculate the duration for each role in months.
   - **IMPORTANT**: If roles overlap in time, do NOT double-count the overlapping months.
   - Sum the non-overlapping months and divide by 12 to get the total years.
   - Round to 1 decimal place.
2. **Experience Score (0.0 - 1.0)**: 
   - 0.0-0.3: Junior (0-2 years)
   - 0.4-0.7: Mid-level (2-6 years)
   - 0.8-1.0: Senior/Expert (6+ years)
   - Adjust slightly based on company prestige and role complexity.
3. **Job Switch Pattern**: 
   - "Frequent" if the average tenure is less than 1.5 years across multiple roles.
   - "Stable" otherwise.
4. **Ranking Companies**: 
   - List professional companies worked at.
   - Rank globally recognized/prestigious firms (e.g., FAANG, Fortune 500) at the top.
   - Exclude schools/colleges from this specific list.

Return ONLY a valid JSON object with these keys:
- "total_experience": number (e.g., 1.2)
- "experience_score": number (0.0 to 1.0)
- "job_switch_pattern": string ("Stable" or "Frequent")
- "best_fit_role": string (suggested professional title)
- "companies": array of strings (ranked list)

Resume Text:
{resume}

Return ONLY the JSON. No preamble or explanation.
""")

    messages = prompt.format_messages(resume=resume_text)
    response = llm.invoke(messages)

    try:
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0]
        data = json.loads(raw)
    except (json.JSONDecodeError, IndexError):
        data = {}

    return {
        "companies": list(data.get("companies") or []),
        "total_experience": float(data.get("total_experience") or 0.0),
        "experience_score": float(data.get("experience_score") or 0.0),
        "job_switch_pattern": str(data.get("job_switch_pattern") or "Stable"),
        "best_fit_role": str(data.get("best_fit_role") or "Software Engineer")
    }
