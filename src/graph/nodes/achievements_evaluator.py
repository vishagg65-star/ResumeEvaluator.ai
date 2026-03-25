from pydantic import BaseModel
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState


class AchievementEval(BaseModel):
    achievements: List[str]
    achievement_score: float  


def achievements_evaluator(state: ResumeState) -> ResumeState:
    print("Achievements Evaluator called")

    resume_text = state.get("resume_text", "")

    llm = get_llm().with_structured_output(AchievementEval)

    prompt = ChatPromptTemplate.from_template("""
You are an AI resume evaluator. Analyze the resume text and identify:

- Any **hackathons**, **coding competitions**, **open source contributions**, 
  **high-impact internships**, **awards**, **certifications**, **publications**, 
  or **achievement highlights**.

Return only a JSON object:
- achievements: string[]    → list of detected accomplishments
- achievement_score: number → between 0 and 0.1
     0.1 = multiple strong achievements
     0.05 = medium / some achievements
     0.0 = no significant achievements found

Resume:
{resume}
""")

    messages = prompt.format_messages(resume=resume_text)
    result: AchievementEval = llm.invoke(messages)

    return {
        "achievements": list(result.achievements or []),
        "achievement_score": float(result.achievement_score),
    }
