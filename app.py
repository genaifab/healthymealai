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

st.title("🥗 Healthy Meals AI - Phase 1: API Connection Test")

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
    
    if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
        return None, "Please add your OpenAI API key to .env file"
    
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
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

st.markdown("### Testing LLM API Connection")

provider = os.getenv("LLM_PROVIDER", "gemini")

st.info(f"Current LLM provider: **{provider}**")
st.markdown("To change providers, edit `.env` file and set `LLM_PROVIDER` to 'gemini' or 'openai'")

if st.button("Test API Connection", type="primary"):
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

st.divider()

st.markdown("### Next Steps")
st.markdown("""
Once the API connection is working:
1. Phase 2: Build the UI scaffolding with sidebar
2. Phase 3: Implement state management
3. Phase 4: Develop LLM prompt engineering
4. Phase 5: Display generated meal plans
""")

st.divider()

st.markdown("### Configuration Help")
with st.expander("How to add your API key"):
    st.markdown("""
    1. Open `.env` file in your project directory
    2. Replace `YOUR_GEMINI_API_KEY_HERE` or `YOUR_OPENAI_API_KEY_HERE` with your actual API key
    3. Set `LLM_PROVIDER` to either 'gemini' or 'openai'
    4. Save the file and restart the Streamlit app
    
    **Getting API Keys:**
    - **Gemini**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    - **OpenAI**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
    
    **For Render deployment:**
    - Add these environment variables in your Render dashboard under Environment settings
    """)