"""
AI Q&A Bot Pro - Enhanced Web Interface
Features: Multiple Chats, Incognito Mode, Beautiful UI
Powered by Groq API
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

st.set_page_config(
    page_title="AI Q&A Bot Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0e1117 0%, #1a1d29 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d29 0%, #0e1117 100%);
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        border: 2px solid #FF4B4B;
        border-radius: 10px;
        padding: 12px;
        color: white;
    }
    .stButton > button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8B8B 100%);
        box-shadow: 0 6px 12px rgba(255, 75, 75, 0.5);
        transform: translateY(-2px);
    }
    .stChatMessage {
        background-color: rgba(38, 39, 48, 0.5);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #FF4B4B;
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #FF4B4B;
    }
    h1 {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8B8B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    h2, h3 {
        color: #FF6B6B;
    }
    .incognito-badge {
        background: linear-gradient(135deg, #6B46C1 0%, #805AD5 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return Groq(api_key=api_key)
    return None

def initialize_session_state():
    if 'chats' not in st.session_state:
        st.session_state.chats = {}
        chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.chats[chat_id] = {
            'name': 'Chat 1',
            'messages': [],
            'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'incognito': False
        }
        st.session_state.current_chat = chat_id
    
    if 'current_chat' not in st.session_state:
        st.session_state.current_chat = list(st.session_state.chats.keys())[0]
    
    if 'incognito_mode' not in st.session_state:
        st.session_state.incognito_mode = False

def create_new_chat():
    chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    chat_number = len(st.session_state.chats) + 1
    st.session_state.chats[chat_id] = {
        'name': f'Chat {chat_number}',
        'messages': [],
        'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'incognito': st.session_state.incognito_mode
    }
    st.session_state.current_chat = chat_id
    st.rerun()

def delete_chat(chat_id):
    if len(st.session_state.chats) > 1:
        del st.session_state.chats[chat_id]
        st.session_state.current_chat = list(st.session_state.chats.keys())[0]
        st.rerun()

def rename_chat(chat_id, new_name):
    st.session_state.chats[chat_id]['name'] = new_name

def get_ai_response(client, question, conversation_history):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and engaging answers."
            }
        ]
        
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
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
    initialize_session_state()
    
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
    
    with st.sidebar:
        st.markdown("# 🤖 AI Q&A Bot Pro")
        st.markdown("### ⚡ Lightning Fast AI")
        
        st.divider()
        
        st.markdown("### 🕵️ Privacy Mode")
        incognito = st.toggle(
            "🔒 Incognito Mode", 
            value=st.session_state.incognito_mode,
            help="Messages won't be saved in history"
        )
        
        if incognito != st.session_state.incognito_mode:
            st.session_state.incognito_mode = incognito
            st.session_state.chats[st.session_state.current_chat]['incognito'] = incognito
        
        if st.session_state.incognito_mode:
            st.markdown("""
                <div class="incognito-badge">
                    🕵️ INCOGNITO MODE ACTIVE
                </div>
            """, unsafe_allow_html=True)
            st.caption("💡 Messages won't be permanently saved")
        
        st.divider()
        
        st.markdown("### 💬 Your Chats")
        
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            create_new_chat()
        
        st.divider()
        
        for chat_id, chat_data in st.session_state.chats.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                is_active = chat_id == st.session_state.current_chat
                button_type = "primary" if is_active else "secondary"
                
                chat_label = chat_data['name']
                if chat_data['incognito']:
                    chat_label = f"🕵️ {chat_label}"
                
                if st.button(chat_label, key=f"chat_{chat_id}", use_container_width=True, type=button_type):
                    st.session_state.current_chat = chat_id
                    st.rerun()
            
            with col2:
                if st.button("✏️", key=f"rename_{chat_id}", help="Rename"):
                    st.session_state[f"rename_mode_{chat_id}"] = True
            
            with col3:
                if len(st.session_state.chats) > 1:
                    if st.button("🗑️", key=f"delete_{chat_id}", help="Delete"):
                        delete_chat(chat_id)
            
            if st.session_state.get(f"rename_mode_{chat_id}", False):
                new_name = st.text_input(
                    "New name:", 
                    value=chat_data['name'],
                    key=f"rename_input_{chat_id}"
                )
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅", key=f"confirm_{chat_id}"):
                        rename_chat(chat_id, new_name)
                        st.session_state[f"rename_mode_{chat_id}"] = False
                        st.rerun()
                with col_b:
                    if st.button("❌", key=f"cancel_{chat_id}"):
                        st.session_state[f"rename_mode_{chat_id}"] = False
                        st.rerun()
            
            msg_count = len([m for m in chat_data['messages'] if m['role'] == 'user'])
            st.caption(f"💬 {msg_count} messages • {chat_data['created']}")
        
        st.divider()
        
        st.markdown("### 📊 Statistics")
        total_chats = len(st.session_state.chats)
        current_chat = st.session_state.chats[st.session_state.current_chat]
        current_messages = len([m for m in current_chat['messages'] if m['role'] == 'user'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Chats", total_chats)
        with col2:
            st.metric("Messages", current_messages)
        
        st.divider()
        
        st.markdown("### 🎯 Model Info")
        st.info("""
        **Model:** Llama 3.1 8B  
        **Provider:** Groq  
        **Speed:** ~500 tok/sec  
        **Cost:** FREE ✨
        """)
        
        st.divider()
        
        if st.button("🗑️ Clear Current Chat", use_container_width=True):
            st.session_state.chats[st.session_state.current_chat]['messages'] = []
            st.rerun()
        
        st.divider()
        
        st.markdown("### 💾 Export")
        if st.button("📥 Export Chat as JSON", use_container_width=True):
            current_chat = st.session_state.chats[st.session_state.current_chat]
            chat_json = json.dumps(current_chat, indent=2)
            st.download_button(
                label="Download JSON",
                data=chat_json,
                file_name=f"{current_chat['name'].replace(' ', '_')}.json",
                mime="application/json"
            )
        
        st.divider()
        
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <p style='font-size: 12px; color: #666;'>
                Made with ❤️ for Internship<br>
                Enhanced Version 2.0<br>
                © 2025
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    current_chat_data = st.session_state.chats[st.session_state.current_chat]
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title(f"💬 {current_chat_data['name']}")
    with col2:
        if current_chat_data['incognito']:
            st.markdown("""
                <div class="incognito-badge">
                    🕵️ INCOGNITO
                </div>
            """, unsafe_allow_html=True)
    with col3:
        st.caption(f"Created: {current_chat_data['created']}")
    
    st.markdown("### ⚡ Ask me anything!")
    
    if len(current_chat_data['messages']) == 0:
        current_chat_data['messages'].append({
            "role": "assistant",
            "content": "👋 Hi! I'm your AI assistant. What would you like to know?",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    for message in current_chat_data['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.caption(f"🕐 {message['timestamp']}")
    
    if prompt := st.chat_input("💭 Type your message here..."):
        
        timestamp = datetime.now().strftime("%H:%M")
        
        current_chat_data['messages'].append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"🕐 {timestamp}")
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = get_ai_response(client, prompt, current_chat_data['messages'])
                timestamp = datetime.now().strftime("%H:%M")
                st.markdown(response)
                st.caption(f"🕐 {timestamp}")
        
        current_chat_data['messages'].append({
            "role": "assistant",
            "content": response,
            "timestamp": timestamp
        })
        
        st.rerun()

if __name__ == "__main__":
    main()