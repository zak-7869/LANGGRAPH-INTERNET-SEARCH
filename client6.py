import os
from typing import TypedDict, List
import streamlit as st
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="Agentic AI Researcher", page_icon="🤖", layout="wide")
st.title("🤖 Multi-Agent Research & Reporting System")
st.caption("Powered by LangGraph, Groq (Llama 3.3), and Tavily Search")

load_dotenv()
# --- SIDEBAR: API KEYS ---
with st.sidebar:
    st.header("🔑 API Configuration")
    groq_key = st.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
    tavily_key = st.text_input("Tavily API Key", type="password", value=os.environ.get("TAVILY_API_KEY", ""))
    st.info("Provide your keys here or set them as environment variables before running.")

# --- LANGGRAPH SETUP ---
class AgentState(TypedDict):
    query: str
    research_results: List[str]
    summary: str
    report: str

def get_workflow(groq_api, tavily_api):
    # FIX: Corrected API key parameters for LangChain components
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api) 
    search_tool = TavilySearchResults(max_results=3, api_key=tavily_api)

    # Node 1: Research Agent
    def research_node(state: AgentState):
        query = state["query"]
        results = search_tool.invoke({"query": query})
        content = [res['content'] for res in results]
        return {"research_results": content}

    # Node 2: Summarizer Agent
    def summarizer_node(state: AgentState):
        data = "\n".join(state["research_results"])
        prompt = f"Summarize the following research data into bullet points:\n\n{data}"
        response = llm.invoke(prompt)
        return {"summary": response.content}

    # Node 3: Report Agent
    def reporter_node(state: AgentState):
        summary = state["summary"]
        prompt = f"Write a professional markdown report based on this summary:\n\n{summary}"
        response = llm.invoke(prompt)
        return {"report": response.content}

    # Build Graph
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", research_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("reporter", reporter_node)

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "summarizer")
    workflow.add_edge("summarizer", "reporter")
    workflow.add_edge("reporter", END)

    return workflow.compile()

# --- MAIN INTERFACE ---
user_query = st.text_input(
    "Enter your research topic:", 
    placeholder="e.g., Latest news on agentic AI?"
)

if st.button("Run Research Pipeline", type="primary"):
    # Validation checks
    if not groq_key or not tavily_key:
        st.error("Please enter both Groq and Tavily API keys in the sidebar.")
    elif not user_query.strip():
        st.warning("Please enter a valid research topic.")
    else:
        # Create container for live execution status updates
        status_container = st.container()
        
        # Setup inputs and application graph
        inputs = {"query": user_query}
        config = {"recursion_limit": 50}
        app = get_workflow(groq_key, tavily_key)
        
        # Dictionary to systematically compile the cumulative global state
        full_state = {}

        with status_container:
            st.subheader("⚙️ Pipeline Execution Log")
            
            # Streaming results through the graph UI
            for output in app.stream(inputs, config):
                for node_name, node_output in output.items():
                    # Safely merge node changes into the full accumulated state
                    full_state.update(node_output)
                    
                    if node_name == "researcher":
                        st.success("✅ Research Agent: Successfully fetched web data.")
                    elif node_name == "summarizer":
                        st.success("✅ Summarizer Agent: Bullet points generated.")
                    elif node_name == "reporter":
                        st.success("✅ Report Agent: Markdown report completed.")

        # --- DISPLAY RESULTS ---
        st.divider()
        st.subheader("📑 Generated Report")
        
        # FIX: Access the clean, accumulated global state dictionary directly
        if "report" in full_state and full_state["report"]:
            st.markdown(full_state["report"])
        else:
            st.error("Pipeline finished but report rendering failed.")
