from langgraph.graph import StateGraph
from app.agents.extract_agent import extract_clauses
from app.agents.risk_agent import analyze_risk
from app.agents.proscons_agent import generate_pros_cons
from app.agents.summary_agent import generate_summary
from app.agents.tts_agent import generate_audio


def build_graph():
    graph = StateGraph(dict)

    graph.add_node("extract", extract_clauses)
    graph.add_node("risk", analyze_risk)
    graph.add_node("proscons", generate_pros_cons)
    graph.add_node("summary", generate_summary)
    graph.add_node("tts", generate_audio)

    graph.set_entry_point("extract")

    graph.add_edge("extract", "risk")
    graph.add_edge("risk", "proscons")
    graph.add_edge("proscons", "summary")
    graph.add_edge("summary", "tts")

    return graph.compile()
