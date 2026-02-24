import os
import time
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

load_dotenv()

# --- Quota Safe LLM Setup ---
def get_llm(model_name="gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )

llm = get_llm()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class AgentState(TypedDict):
    topic: str
    plan: str
    content: Annotated[list, operator.add] 
    steps: Annotated[list, operator.add]   
    iterations: int
    is_sufficient: bool
    final_report: dict

# --- Nodes ---

def planner_node(state: AgentState):
    prompt = f"Create a simple 3-step research plan for: {state['topic']}. Return only the steps."
    try:
        plan = llm.invoke(prompt).content
    except Exception:
        plan = "1. Search web 2. Gather data 3. Summarize"
    return {"plan": plan, "steps": ["📋 Created research plan"]}

def researcher_node(state: AgentState):
    query = state['topic']
    # Getting 5 results to ensure plenty of links for the report
    results = tavily.search(query=query, search_depth="advanced", max_results=5)
    new_data = [f"SOURCE ({r['url']}): {r['content']}" for r in results['results']]
    
    return {
        "content": new_data, 
        "iterations": state['iterations'] + 1,
        "steps": [f"🔍 Research search completed (Found {len(new_data)} sources)"]
    }

def evaluator_node(state: AgentState):
    if state['iterations'] >= 2:
        return {"is_sufficient": True, "steps": ["⚖️ Evaluation: Finished"]}
    
    combined = " ".join(state['content'][:2])
    prompt = f"Is this enough info for '{state['topic']}'? Reply YES or NO.\n\n{combined}"
    try:
        answer = llm.invoke(prompt).content.strip().upper()
        is_suff = "YES" in answer
    except Exception:
        is_suff = True 
    return {"is_sufficient": is_suff, "steps": ["⚖️ Evaluation completed"]}

def synthesizer_node(state: AgentState):
    full_context = "\n\n".join(state['content'])
    
    # Restored your specific 4-5 sections + Inline Link instructions
    prompt = f"""
    Synthesize a professional research report on: {state['topic']}
    Using this gathered data: {full_context}
    
    IMPORTANT: You MUST place clickable links [Source Name](URL) directly next to the facts you cite.
    
    The report MUST include:
    1. 📝 Executive Summary: Overview with [Links].
    2. 💡 Key Insights: 3 detailed points with [Links].
    3. ⚖️ Contradiction Check: Where sources disagree, with [Links].
    4. 🎯 Confidence Score: (0-100%) based on the quality of sources.
    5. 🚀 Key Takeaways: Final summary and next steps.
    6. 🔗 Reference List: List all clickable links at the end.
    """
    
    try:
        report = llm.invoke(prompt).content
    except Exception as e:
        report = f"Error generating report: {str(e)}"

    return {"final_report": {"report": report}, "steps": ["✍️ Professional report synthesized"]}

# --- Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("evaluator", evaluator_node)
workflow.add_node("synthesizer", synthesizer_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "evaluator")
workflow.add_conditional_edges("evaluator", lambda x: "synthesizer" if x["is_sufficient"] else "researcher")
workflow.add_edge("synthesizer", END)

app_graph = workflow.compile()

def run_research_agent(topic: str):
    initial_state = {
        "topic": topic, 
        "content": [], 
        "steps": [], 
        "iterations": 0, 
        "is_sufficient": False
    }
    final_state = app_graph.invoke(initial_state)
    return final_state["steps"], final_state["final_report"]