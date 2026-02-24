🧠 AutoResearch Agent
📌 Introduction

AutoResearch Agent is an autonomous AI-powered research system that intelligently investigates user-provided topics by planning research steps, automatically searching the web, evaluating information quality, and synthesizing structured insights.

Unlike a basic chatbot, this agent performs multi-step reasoning, autonomous tool usage, and self-correction loops to produce reliable research summaries along with sources and confidence scores.

The system also visualizes its internal reasoning through a Thinking Log, enabling transparency into how decisions are made in real time.

This project was built for Track-1: AI/ML — AutoResearch Agent.

🛠️ Technologies & Tools Used
🔹 AI & Orchestration

LangChain — Used as the orchestration framework to manage LLM calls and agent workflow

Google Gemini 2.5-Flash — Core reasoning and synthesis LLM

🔹 Tool Integration

Tavily Search API — Real-time web search tool used autonomously by the agent

🔹 Frontend

Streamlit — Lightweight web UI for user interaction and live reasoning visualization

🔹 Backend & Utilities

Python

python-dotenv — Secure environment variable management

🏗️ Architecture Flow

User Input (Streamlit UI)
        ↓
LangChain Orchestration Layer
        ↓
Gemini 2.5 LLM (Reasoning & Synthesis)
        ↓
Tavily Search Tool (External Knowledge)
        ↓
Evaluation + Retry Loop
        ↓
Final Structured Research Report

https://drive.google.com/file/d/1MsG8imnn74WoGdAzJoWPszEHoFChjiu9/view?usp=sharing

Key Features
✔ Multi-Step Reasoning
Agent generates a research plan before executing.

✔ Autonomous Tool Usage
Agent decides when and what to search.

✔ Self-Evaluation & Iteration
Agent checks sufficiency of results and retries if needed.

✔ Information Synthesis
Combines sources and outputs summary, insights, citations, and confidence score.

✔ Thinking Log Visualization
Real-time logs show internal reasoning during execution.

🔬 Analysis & Stress Test Document
3. Hallucination Risks & Prevention
The Risk: Since the agent uses a Large Language Model (Gemini), it might "hallucinate" (invent facts) if the search results are messy or if it tries to fill gaps in its knowledge with guesswork.

Our Prevention Strategies:

Grounding in Search (RAG): The agent is strictly instructed to only use information provided by the Tavily Search API. It acts as a "Retrieval-Augmented Generation" (RAG) system, meaning it doesn't rely on its internal training data for facts.

Mandatory Source Citations: We've programmed the Synthesizer Node to include URLs for every major claim. If it can't find a source in the "State," it is told to say "Information not found" rather than making it up.

The Evaluator "Gatekeeper": The Evaluator Node acts as a fact-checker. If the retrieved data is conflicting or vague, the Evaluator rejects the draft and forces a new search with more specific queries to clear up the confusion.

2. Preventing Infinite Loops
The Risk: In a cyclic architecture (like LangGraph), the agent could theoretically loop between the Researcher and Evaluator forever if it keeps failing to find "perfect" information.

Our Prevention Strategies:

Recursion Limits: We utilize LangGraph’s built-in recursion_limit. By setting this to a fixed number (e.g., 25 steps), the framework automatically kills the process if it loops too many times, acting as a "Circuit Breaker."

Iteration Counter: We added an iterations variable to our AgentState. Every time the Researcher runs, we do iterations += 1.

Deterministic Exit Logic: In the Evaluator's conditional edge, we have a hard-coded rule: "If iterations > 3, proceed to Synthesis immediately." This ensures that even if the research isn't "perfect," the agent will eventually stop and give the "Best Effort" report rather than looping indefinitely.

▶️ How to Run
1. Clone repo
2. Create virtual environment
3. Install dependencies:
   pip install -r requirements.txt

4. Add API keys in .env:
   GOOGLE_API_KEY=...
   TAVILY_API_KEY=...

5. Run:
   streamlit run app.py

🧠 Why LangChain 
LangChain was chosen as the orchestration framework to manage:
- Gemini model interaction
- search tool integration
- reasoning workflow (plan → search → evaluate → retry → synthesize)

This enables a transparent autonomous research pipeline.

Demo Video
https://drive.google.com/file/d/1HCfA27UqSg89zM7HReT2qfUJG6-GXJun/view?usp=sharing
 
