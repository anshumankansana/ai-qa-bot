import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

def test_models():
    """Test which models are working"""
    
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ No API key found!")
        return
    
    client = InferenceClient(token=api_key)
    
    models = [
        "microsoft/Phi-3-mini-4k-instruct",
        "mistralai/Mistral-7B-Instruct-v0.2",
        "google/flan-t5-large",
        "google/flan-t5-base",
        "HuggingFaceH4/zephyr-7b-beta",
        "tiiuae/falcon-7b-instruct",
        "facebook/opt-1.3b",
        "EleutherAI/gpt-neo-1.3B",
    ]
    
    test_question = "What is Python?"
    
    print("🧪 Testing Hugging Face Models...")
    print("=" * 60)
    
    working_models = []
    
    for model in models:
        print(f"\n📝 Testing: {model}")
        try:
            response = client.text_generation(
                test_question,
                model=model,
                max_new_tokens=50,
                temperature=0.7
            )
            
            print(f"✅ SUCCESS!")
            print(f"Response: {response[:80]}...")
            working_models.append(model)
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)[:60]}")
    
    print("\n" + "=" * 60)
    print(f"\n✅ Working Models ({len(working_models)}):")
    for model in working_models:
        print(f"   - {model}")

if __name__ == "__main__":
    test_models()