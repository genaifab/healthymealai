import streamlit as st
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Healthy Meals AI",
    page_icon="🥗",
    layout="wide"
)

# Title in main area
st.title("🥗 Healthy Meals AI")

# Sidebar configuration
with st.sidebar:
    st.header("Your Preferences")
    
    # User Persona Selection
    st.subheader("Your Profile")
    user_profile = st.radio(
        "Which best describes you?",
        [
            "Standard Healthy Eating",
            "Low-Sugar/Pre-Diabetic Friendly",
            "Vegetarian",
            "Gluten-Free"
        ],
        help="Select the meal plan type that best fits your needs"
    )
    
    # Excluded Foods
    st.subheader("Foods to Exclude")
    excluded_foods = st.text_input(
        "List any specific foods to avoid:",
        placeholder="e.g., mushrooms, cilantro, seafood",
        help="Separate multiple items with commas"
    )
    
    # Meals per Day
    st.subheader("Meals per Day")
    meals_per_day = st.radio(
        "Select your meal plan:",
        ["Breakfast, Lunch, Dinner", "Lunch, Dinner"],
        help="Choose which meals to include in your plan"
    )
    
    # Divider before button
    st.divider()
    
    # Generate button
    generate_button = st.button(
        "🚀 Generate My Weekly Plan",
        type="primary",
        use_container_width=True
    )

# Main content area
# Welcome message when no plan is generated yet
st.markdown("## Welcome to Your Personal Meal Planning Assistant!")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ### 🎯 Get Started in 3 Simple Steps:
    
    1. **Set Your Preferences** - Use the sidebar to tell us about your dietary needs
    2. **Click Generate** - Our AI will create a personalized weekly meal plan
    3. **Get Your Grocery List** - Everything you need for the week, organized by category
    
    Your meal plan will feature:
    - ✨ Wholesome, non-processed ingredients
    - ⏱️ Recipes that respect your time constraints
    - 🥗 Meals tailored to your dietary preferences
    - 📝 Complete recipes with step-by-step instructions
    
    **👈 Start by setting your preferences in the sidebar!**
    """)

# Temporary API test section (will be removed in later phases)
st.divider()
with st.expander("🔧 API Connection Test (Development Only)"):
    st.markdown("### Testing LLM API Connection")
    
    provider = os.getenv("LLM_PROVIDER", "gemini")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini") if provider == "openai" else "gemini-pro"
    
    st.info(f"Current LLM provider: **{provider}**")
    if provider == "openai":
        st.info(f"Current OpenAI model: **{model}**")
    st.markdown("To change providers, edit `.env` file and set `LLM_PROVIDER` to 'gemini' or 'openai'")
    
    if st.button("Test API Connection"):
        with st.spinner("Connecting to LLM API..."):
            if provider == "gemini":
                response, error = test_gemini_api()
            elif provider == "openai":
                response, error = test_openai_api()
            else:
                response = None
                error = f"Invalid provider: {provider}. Please use 'gemini' or 'openai'"
            
            if response:
                st.success("✅ API Connection Successful!")
                st.markdown("**LLM Response:**")
                st.write(response)
            else:
                st.error("❌ API Connection Failed")
                st.error(error)

# API test functions (from Phase 1)
def test_gemini_api():
    """Test connection to Google Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        return None, "Please add your Gemini API key to .env file"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": "Say hello and confirm you're working. Response in one sentence."
            }]
        }]
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(url, json=data, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text, None
            else:
                return None, f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

def test_openai_api():
    """Test connection to OpenAI API"""
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
        return None, "Please add your OpenAI API key to .env file"
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Say hello and confirm you're working. Response in one sentence."
            }
        ],
        "max_tokens": 50
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(url, json=data, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                result = response.json()
                text = result['choices'][0]['message']['content']
                return text, None
            else:
                return None, f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"