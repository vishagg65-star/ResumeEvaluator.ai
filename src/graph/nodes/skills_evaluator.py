from typing import List
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState

class SkillsEval(BaseModel):
    role_inferred: str
    matched_skills: List[str]
    missing_skills: List[str]
    skills_score: float

def skills_evaluator(state: ResumeState) -> ResumeState:
    print("Skills Evaluator called")

    resume_text = state["resume_text"]
    llm = get_llm().with_structured_output(SkillsEval)

    prompt = ChatPromptTemplate.from_template("""
You are an AI recruitment assistant analyzing a candidate's skills.
Based only on the given resume, do the following:
1) Infer the most likely professional role or domain (e.g., AI Engineer, Frontend Developer, DevOps Engineer, Data Scientist).
2) Identify which critical skills are present and which key skills are missing for that role.
3) Give an overall skills completeness score between 0 and 1.

Return ONLY the JSON object with keys:
- role_inferred: string
- matched_skills: string[]
- missing_skills: string[]
- skills_score: number

Candidate Resume:
{resume}
""")

    messages = prompt.format_messages(resume=resume_text)
    result: SkillsEval = llm.invoke(messages)

    # Return only updated fields
    return {
        "role_inferred": result.role_inferred,
        "skills_score": float(result.skills_score),
        "matched_skills": list(result.matched_skills or []),
        "missing_skills": list(result.missing_skills or []),
    }