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

The system operates through the following workflow:

User enters a research topic in the Streamlit interface

Agent generates a research plan using Gemini

Agent autonomously decides and triggers Tavily search

Search results are evaluated for sufficiency

If insufficient, the agent refines the query and retries

Gemini synthesizes information from multiple sources

Thinking logs are streamed to the UI in real time

Final structured research report is displayed