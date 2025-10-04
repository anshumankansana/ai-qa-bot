"""
AI Q&A Bot - Web Interface
Powered by Groq API - Lightning Fast Responses
Built for Internship Assignment
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Q&A Bot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF6B6B;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def get_client():
    """Initialize Groq client"""
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return Groq(api_key=api_key)
    return None

def get_ai_response(client, question, conversation_history):
    """Get AI response with conversation context"""
    try:
        # Build messages with history for context
        messages = [
            {
                "role": "system",
                "content": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and concise answers. Be conversational and engaging."
            }
        ]
        
        # Add conversation history (last 5 exchanges for context)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current question
        messages.append({
            "role": "user",
            "content": question
        })
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main Streamlit app"""
    
    # Header
    st.title("🤖 AI Q&A Bot")
    st.markdown("### ⚡ Lightning-fast AI answers powered by Groq")
    
    # Check if client is initialized
    client = get_client()
    
    if not client:
        st.error("❌ GROQ_API_KEY not found!")
        st.info("📝 Please add your Groq API key to the .env file")
        st.markdown("""
        **How to get your FREE API key:**
        1. Visit: https://console.groq.com/keys
        2. Sign up (it's free!)
        3. Create an API key
        4. Add to `.env` file: `GROQ_API_KEY=your_key_here`
        """)
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **AI Q&A Bot**  
        Built for internship assignment
        
        **Features:**
        - ⚡ Lightning-fast responses
        - 💬 Conversation history
        - 🎨 Modern UI
        - 🆓 100% FREE
        - 🚀 Powered by Groq
        """)
        
        st.divider()
        
        st.header("📊 Statistics")
        if 'messages' in st.session_state:
            total_messages = len(st.session_state.messages)
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.metric("Total Messages", total_messages)
            st.metric("Your Questions", user_messages)
        else:
            st.metric("Total Messages", 0)
        
        st.divider()
        
        st.header("🎯 Model Info")
        st.info("""
        **Model:** Llama 3.1 8B Instant  
        **Provider:** Groq  
        **Speed:** ~500 tokens/sec  
        **Cost:** FREE
        """)
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <p style='font-size: 12px; color: #666;'>
                Made with ❤️ for Internship<br>
                © 2025
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "👋 Hi! I'm your AI assistant powered by Groq. Ask me anything!",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.caption(f"🕐 {message['timestamp']}")
    
    # Chat input
    if prompt := st.chat_input("💭 Ask me anything..."):
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"🕐 {timestamp}")
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = get_ai_response(client, prompt, st.session_state.messages)
                timestamp = datetime.now().strftime("%H:%M")
                st.markdown(response)
                st.caption(f"🕐 {timestamp}")
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": timestamp
        })
        
        # Rerun to update sidebar stats
        st.rerun()

if __name__ == "__main__":
    main()