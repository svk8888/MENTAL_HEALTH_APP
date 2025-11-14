# 🧠 Mindful Companion - AI Mental Health Chatbot

An intelligent mental health support companion powered by RAG (Retrieval-Augmented Generation) and LLM tool calling, providing empathetic, evidence-based mental health support.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-green.svg)

---

## 🌟 Features

### **Core Capabilities**
- 🤖 **AI-Powered Conversations** - Empathetic, supportive responses using GPT-3.5-turbo
- 📚 **RAG Architecture** - Retrieves relevant information from curated mental health knowledge base
- 🔍 **Intelligent Web Search** - LLM autonomously decides when to search for recent information
- ⚠️ **Crisis Detection** - Identifies high-risk situations and provides immediate resources
- 💭 **Context-Aware** - Maintains conversation history for coherent interactions

### **Technical Features**
- **Vector Database** - ChromaDB for semantic search and document retrieval
- **LLM Tool Calling** - OpenAI function calling for dynamic web search
- **Multi-Source Data** - Aggregates from Hugging Face, web scraping
- **Safety Guidelines** - Built-in safety rules to avoid medical advice
- **Real-Time Search** - Tavily API integration for latest mental health research

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Streamlit Chat UI)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Safety Monitor                            │
│              (Crisis Keyword Detection)                      │
└───────────┬─────────────────────────┬───────────────────────┘
            │                         │
    High/Medium Risk              Low Risk
            │                         │
            ▼                         ▼
    ┌──────────────┐        ┌─────────────────┐
    │   Crisis     │        │   RAG Engine    │
    │   Response   │        │   (ChromaDB)    │
    └──────────────┘        └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   MCP Handler   │
                            │  (LLM + Tools)  │
                            └────────┬────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                                 │
                    ▼                                 ▼
           ┌─────────────────┐            ┌──────────────────┐
           │  Direct Response│            │  Tool: Web Search│
           │  (No Tool Call) │            │  (Tavily API)    │
           └─────────────────┘            └──────────┬───────┘
                    │                                 │
                    └────────────────┬────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  Final Response │
                            │   to User       │
                            └─────────────────┘
```

---

## 📋 Prerequisites

- Python 3.13 or higher
- OpenAI API key
- Tavily API key
- 4GB RAM minimum
- Internet connection for API calls

---

## 🚀 Installation

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd mental_health_app
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux

```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
TAVILY_API_KEY=tvly-your-tavily-api-key-here
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com/ (Free tier: 1000 searches/month)

### **5. Initialize the Database (Optional)**

To load data into ChromaDB, when the application startup

```python


# To:
self.load_dynamic_knowledge()
```

---

## 🎮 Usage

### **Start the Application**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### **Interact with the Chatbot**

### **Example Interactions**

**Emotional Support:**
```
User: I'm feeling really anxious today
Bot: I hear you, and I'm here for you. Anxiety can feel overwhelming...
```

**Recent Information (Triggers Web Search):**
```
User: What's the latest research on anxiety treatments?
Bot: 🔍 Searching for latest information...
     Based on recent research, several new approaches...
```

**General Information (Uses RAG):**
```
User: What are some coping strategies for stress?
Bot: Here are some evidence-based coping strategies...
```

---

## 📁 Project Structure

```
mental_health_app/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                           # API keys (create this)
├── README.md                     
│
├── mental_health_db/              # ChromaDB vector database (auto-created)
│   └── chroma.sqlite3
│
├── utils/                         # Core modules
│   ├── __init__.py               # Package initializer
│   ├── rag_engine.py             # RAG system with ChromaDB
│   ├── mcp_handler.py            # LLM interactions & tool calling
│   ├── safety_monitor.py         # Crisis detection
│   ├── web_search_tavily.py      # Tavily web search integration
│   ├── huggingface_loader.py     # Loads PubMed QA dataset -https://huggingface.co/datasets/qiaojin/PubMedQA/
│──-├── web_loader.py             # Scrapes mental health websites

```

---

## 🔧 Configuration

### **LLM Settings** (`utils/mcp_handler.py`)

```python
model="gpt-3.5-turbo"      # OpenAI model
temperature=0.7            # Response creativity (0-1)
max_tokens=500             # Maximum response length
tool_choice="auto"         # Let LLM decide when to use tools
```

### **RAG Settings** (`utils/rag_engine.py`)

```python
n_results=3                # Number of similar documents to retrieve
collection_name="mental_health_knowledge"
db_path="./mental_health_db"
```

### **Web Search Settings** (`utils/web_search_tavily.py`)

```python
search_depth="advanced"    # Search comprehensiveness
include_answer=True        # Get AI-generated summary
max_results=3              # Number of search results
```

### **Safety Keywords** (`utils/safety_monitor.py`)

```python
high_risk_keywords = [
    "suicide", "kill myself", "end my life", 
    "want to die", "better off dead"
]

medium_risk_keywords = [
    "hopeless", "can't go on", "no point",
    "self-harm", "hurt myself"
]
```

---

## 🧪 Testing

### **Test Basic Functionality**

```bash
# Start the app
streamlit run app.py

# Test queries in the browser:
```

**1. Emotional Support (No Tool Call):**
- "I'm feeling depressed"
- "Can you help me with anxiety?"
- "I need someone to talk to"

**2. Recent Information (Tool Call Expected):**
- "What's the latest research on PTSD?"
- "Tell me about recent mental health news"
- "Any new anxiety treatments available?"

**3. Crisis Detection:**
- "I'm thinking about suicide" (should trigger crisis resources)
- "I feel hopeless" (medium risk)

### **Monitor Console Output**

```bash
# LLM decides to use tool:
🔧 LLM decided to use tool: search_mental_health_web
🔍 Executing web search: latest anxiety research...
✅ Tavily search returned 3 results
🤖 LLM processing search results and generating final response...

# LLM responds directly:
💭 LLM responding directly without tools

# Crisis detected:
⚠️ High risk detected: suicide, kill myself
```

---

## 📊 Data Sources

### **Current Sources**

1. **Hugging Face Datasets**
   - PubMed QA (medical Q&A) --> https://huggingface.co/datasets/qiaojin/PubMedQA/
   - 100 samples from training set

2. **Web Scraping**
   - WHO (World Health Organization)
   - NAMI (National Alliance on Mental Illness)
   - CDC (Centers for Disease Control)


---

## 🛡️ Safety Features

### **Built-in Protections**

✅ **No Medical Advice** - System never provides diagnoses or prescriptions  
✅ **Crisis Detection** - Identifies suicidal/self-harm language  
✅ **Resource Provision** - Provides 988 hotline and crisis resources  
✅ **Professional Referral** - Always encourages professional help  
✅ **Validation-Focused** - Empathetic listening, not medical treatment  

### **Crisis Resources Provided**

- **988 Suicide & Crisis Lifeline** (US)
- **Crisis Text Line**: Text HOME to 741741
- **International Hotlines** by country
- **Emergency Services**: 911 (US)

### **Disclaimer**

```
⚠️ IMPORTANT DISCLAIMER:
This chatbot is NOT a substitute for professional mental health care.
It does not provide medical advice, diagnoses, or treatment recommendations.
In case of emergency, call 988 (US) or your local emergency services.
Always consult with licensed mental health professionals for serious concerns.
```

---

## 🔍 How It Works

### **1. RAG (Retrieval-Augmented Generation)**

When you ask a question:
1. **Query embedding** - Converts your question to a vector
2. **Semantic search** - Finds similar documents in ChromaDB
3. **Context building** - Top 3 relevant documents retrieved
4. **LLM generation** - GPT-3.5 generates response with context

### **2. LLM Tool Calling**

The LLM autonomously decides when to search the web:

```python
# Tool definition given to LLM:
{
  "name": "search_mental_health_web",
  "description": "Search for recent mental health information, 
                  latest research, or current news",
  "parameters": {
    "query": "Search query",
    "max_results": 3
  }
}
```

**LLM Decision Process:**
- Analyzes user intent
- Determines if recent information needed
- Calls tool if appropriate
- Formats results into helpful response

### **3. Two-Step LLM Process**

**Without Tool:**
```
User Query → RAG Context → LLM → Response
```

**With Tool:**
```
User Query → RAG Context → LLM Call #1 → Tool Call → 
Web Search → LLM Call #2 (with results) → Response
```

---


## 🐛 Troubleshooting

### **Issue: "ModuleNotFoundError"**

```bash
# Solution: Install missing packages
pip install -r requirements.txt
```

### **Issue: "OPENAI_API_KEY not found"**

```bash
# Solution: Create .env file with your API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
echo "TAVILY_API_KEY=tvly-your-key-here" >> .env
```

### **Issue: "ChromaDB collection is empty"**

```python
# Solution: Uncomment in utils/rag_engine.py line 19:
self.load_dynamic_knowledge()
```

### **Issue: "LLM never calls tools"**

- Try more explicit queries: "What's the LATEST research..."
- Check console for tool call indicators (🔧)
- Consider upgrading to GPT-4 for better tool decisions

### **Issue: "Streamlit won't start"**

```bash
# Clear cache and restart
streamlit cache clear
streamlit run app.py
```

---


### **Planned Features**

- [ ] Voice input/output
- [ ] Mobile app version
- [ ] Appointment scheduling
- [ ] Mood tracking dashboard
- [ ] Therapist finder tool
- [ ] Personalized recommendations
- [ ] Progress tracking over time

---

## ⚠️ Disclaimer

**IMPORTANT:** This application is designed for:
- Emotional support and companionship
- General mental health education
- Coping strategy suggestions
- Resource provision

**This application is NOT:**
- A replacement for professional therapy
- A medical diagnostic tool
- A crisis intervention service
- A prescription or treatment provider

**If you are in crisis:**
- Call 988 (Suicide & Crisis Lifeline - US)
- Text HOME to 741741 (Crisis Text Line)
- Call 911 or go to your nearest emergency room
- Contact a licensed mental health professional


---

## 💡 Tips for Best Results

### **For Users:**
1. Be specific in your questions
2. Ask about "latest" or "recent" for web searches
3. Use mood buttons for quick check-ins
4. Don't hesitate to ask follow-up questions
5. Remember this is for support, not diagnosis

### **For Developers:**
1. Monitor console output for debugging
2. Test with various query types
3. Adjust temperature for creativity vs consistency
4. Keep API keys secure
5. Review safety guidelines regularly

---

## Tools Used

- **OpenAI** - GPT-3.5-turbo language model
- **Tavily** - Real-time web search API
- **ChromaDB** - Vector database
- **Streamlit** - Web app framework
- **Hugging Face** - Dataset hosting
- **Mental Health Organizations** - WHO, NAMI, CDC for educational content

---
