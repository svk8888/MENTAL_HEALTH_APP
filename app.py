import streamlit as st
import os
from dotenv import load_dotenv
from utils.rag_engine import MentalHealthRAG
from utils.safety_monitor import SafetyMonitor
from utils.mcp_handler import MCPHandler
from utils.web_search_tavily import TavilyWebSearch

# Load environment variables
load_dotenv()

# Initialize components
@st.cache_resource
def initialize_components():
    rag_engine = MentalHealthRAG()
    safety_monitor = SafetyMonitor()
    web_search = TavilyWebSearch(api_key=os.getenv("TAVILY_API_KEY"))
    
    # Pass web search tool to MCP handler so LLM can use it
    mcp_handler = MCPHandler(
        api_key=os.getenv("OPENAI_API_KEY"),
        web_search_tool=web_search.search  # Pass the search method as a tool
    )
    return rag_engine, safety_monitor, mcp_handler, web_search

def main():
    st.set_page_config(
        page_title="Mindful Companion",
        page_icon="🧠",
        layout="wide"
    )
    
    # Initialize components
    try:
        rag_engine, safety_monitor, mcp_handler, web_search = initialize_components()
    except Exception as e:
        st.error(f"Failed to initialize: {str(e)}")
        return
    
    # Sidebar
    st.sidebar.title("🧠 MindSukoon")
    st.sidebar.markdown("Your AI mental health support companion")
    
    st.sidebar.markdown("### 💡 Support Features")
    st.sidebar.markdown("""
    - Emotional support & validation
    - CBT-inspired reflections
    - Crisis resources
    """)
    
    st.sidebar.markdown("### ⚠️ Important")
    st.sidebar.markdown("""
    - Not a substitute for therapy
    - No medical advice
    - Emergency: Call 988
    - Always consult professionals
    """)
    
    # Main interface
    st.title("🧠 MindSukoon")
    st.markdown("### Your compassionate AI mental health support partner")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hi there! I'm here to listen and offer support. How are you feeling today? 💭"
        })
    
      
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Share what's on your mind..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Safety check first
        risk_level = safety_monitor.assess_risk_level(prompt)
        
        if risk_level != "low_risk":
            # Crisis situation - use safety response
            crisis_response = safety_monitor.get_crisis_response(risk_level)
            with st.chat_message("assistant"):
                st.markdown(crisis_response)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": crisis_response
            })
        else:
            # Normal conversation flow
            with st.spinner("🧠 Thinking compassionately..."):
                # RAG: Retrieve relevant mental health content
                rag_context = rag_engine.retrieve_relevant_content(prompt)
                
                # MCP: Generate response with tool calling (LLM decides if web search is needed)
                ai_response = mcp_handler.generate_response_with_tools(
                    prompt, rag_context, risk_level
                )
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response
            })
    
  

if __name__ == "__main__":
    main()