# final_score = (
#     0.4 * skills_score +
#     0.3 * experience_score +
#     0.2 * project_score +
#     0.1 * education_score
# )
from src.graph.state.graph_state import ResumeState

class ScoreAggregationLogic:
    def final_score_of_resume(self, state: ResumeState) -> float:
        final_score = (
                0.4 * state["skills_score"] +
                0.3 * state["experience_score"] +
                0.2 * state["project_score"] +
                0.1 * state["education_score"]
        )
        return final_score