import streamlit as st
import json
from datetime import datetime
from agent import run_research_agent

# Use wide mode for a more 'dashboard' feel
st.set_page_config(page_title="AutoResearch Agent", layout="wide", initial_sidebar_state="expanded")

# Initialize session state so the report and logs stay visible
if "final_report_text" not in st.session_state:
    st.session_state.final_report_text = None
if "agent_logs_data" not in st.session_state:
    st.session_state.agent_logs_data = None

# --- UI Header ---
st.title("🔬 AutoResearch Agent")
st.info("Autonomous AI agent that searches, evaluates, and synthesizes real-time web data.")

# --- Sidebar for Thinking Log & Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    research_depth = st.select_slider(
        "Select Research Depth",
        options=["Quick", "Standard", "Detailed"],
        value="Standard"
    )
    
    st.divider()
    st.header("🧠 Thinking Log")
    st.write("Agent's internal decision-making process:")
    log_placeholder = st.empty() # Create a place to update logs

# --- Main Input Area ---
topic = st.text_input("Enter a topic to research:", placeholder="e.g. Impact of AI on healthcare in 2026")

if st.button("Generate Research", use_container_width=True):
    if topic:
        with st.sidebar:
            with st.status("Agent is working...", expanded=True) as status:
                # 1. Run the Agent logic
                logs, final_result = run_research_agent(topic)
                
                # 2. Show the thoughts live
                for step in logs:
                    st.write(f"✔️ {step}")
                
                # 3. Store EVERYTHING for the JSON log
                st.session_state.agent_logs_data = {
                    "metadata": {
                        "topic": topic,
                        "timestamp": datetime.now().isoformat(),
                        "depth": research_depth
                    },
                    "trace_steps": logs,
                    "final_report": final_result.get("report", ""),
                    "raw_state_summary": str(final_result) # Captures internal variables
                }
                
                st.session_state.final_report_text = final_result["report"]
                status.update(label="✅ Analysis Complete!", state="complete")
    else:
        st.error("Please enter a topic first")

# --- 3. Display the Final Report & Submission Tools ---
if st.session_state.final_report_text:
    st.divider()
    
    # Create two columns for download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Download Report (TXT)", 
            data=st.session_state.final_report_text, 
            file_name=f"research_{topic.replace(' ', '_')}.txt",
            use_container_width=True
        )
    
    with col2:
        # This is the JSON Log for your Hackathon Submission!
        json_log = json.dumps(st.session_state.agent_logs_data, indent=4)
        st.download_button(
            label="📥 Download Agent Logs (JSON for Submission)",
            data=json_log,
            file_name="agent_logs.json",
            mime="application/json",
            use_container_width=True,
            help="Upload this file to your GitHub to show your agent traces."
        )

    st.markdown("### 📝 Final Research Report")
    st.markdown(st.session_state.final_report_text)