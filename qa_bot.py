"""
AI Q&A Bot - Command Line Interface
Powered by Groq API
"""

import os
from groq import Groq
from dotenv import load_dotenv
import sys

load_dotenv()

def print_header():
    print("\n" + "=" * 60)
    print("🤖  AI Q&A BOT - COMMAND LINE")
    print("=" * 60)
    print("⚡ Powered by Groq - Lightning Fast AI")
    print("💡 Type your questions and get instant answers")
    print("🚪 Type 'quit', 'exit', or 'q' to leave")
    print("=" * 60 + "\n")

def initialize_client():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\n❌ ERROR: GROQ_API_KEY not found!")
        print("\n📝 Please follow these steps:")
        print("1. Go to: https://console.groq.com/keys")
        print("2. Sign up (it's FREE!)")
        print("3. Create an API key")
        print("4. Add it to your .env file:")
        print("   GROQ_API_KEY=your_key_here")
        print()
        return None
    
    try:
        client = Groq(api_key=api_key)
        return client
    except Exception as e:
        print(f"\n❌ Error initializing Groq client: {e}\n")
        return None

def get_ai_response(client, question):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, friendly, and knowledgeable AI assistant."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=300,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    print_header()
    
    client = initialize_client()
    if not client:
        sys.exit(1)
    
    print("✅ Connected to Groq API successfully!\n")
    
    conversation_count = 0
    
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye! Thanks for using AI Q&A Bot!")
            break
        
        if question.lower() in ['quit', 'exit', 'q', 'bye']:
            print("\n👋 Goodbye! Thanks for using AI Q&A Bot!")
            break
        
        if not question:
            print("💭 Please ask me something!\n")
            continue
        
        print("\n🤔 Thinking...\n")
        answer = get_ai_response(client, question)
        
        print(f"🤖 Bot: {answer}\n")
        print("-" * 60 + "\n")
        
        conversation_count += 1
    
    print(f"\n📊 Session Stats: {conversation_count} questions answered")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()