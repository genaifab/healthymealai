import streamlit as st
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Core LLM functions for meal plan generation
def construct_llm_prompt(preferences):
    """
    Construct a detailed prompt for the LLM based on user preferences.
    Returns a string prompt that instructs the LLM to return JSON.
    """
    # Map user profiles to dietary requirements
    profile_map = {
        "Standard Healthy Eating": "Focus on whole foods, balanced nutrition, lean proteins, whole grains, and plenty of vegetables. Avoid processed foods.",
        "Low-Sugar/Pre-Diabetic Friendly": "Low glycemic index foods only. NO added sugars, NO refined carbohydrates, NO white bread/pasta/rice. Focus on complex carbs, lean proteins, and non-starchy vegetables.",
        "Vegetarian": "No meat or fish. Include diverse plant proteins (legumes, tofu, tempeh, quinoa). Ensure complete proteins and adequate B12, iron, and omega-3 sources.",
        "Gluten-Free": "Absolutely NO wheat, barley, rye, or cross-contaminated oats. Use rice, quinoa, corn, certified gluten-free oats, and other safe grains."
    }
    
    dietary_requirements = profile_map.get(preferences['user_profile'], "")
    excluded_foods = preferences.get('excluded_foods', '')
    meals_per_day = preferences.get('meals_per_day', 'Breakfast, Lunch, Dinner')
    
    # Determine which meals to include
    if "Breakfast" in meals_per_day:
        meal_list = ["breakfast", "lunch", "dinner"]
    else:
        meal_list = ["lunch", "dinner"]
    
    prompt = f"""You are a professional nutritionist creating a personalized 3-day meal plan.

DIETARY REQUIREMENTS:
{dietary_requirements}

EXCLUDED FOODS (must not appear in any recipe):
{excluded_foods if excluded_foods else "None"}

MEALS NEEDED PER DAY:
{', '.join(meal_list)}

Create a complete 3-day meal plan following these rules:
1. Use ONLY whole, non-processed ingredients
2. Each recipe should be completable in 45 minutes or less
3. Provide variety - no recipe should repeat
4. Include complete nutritional balance for each day
5. Recipes should be practical for busy professionals

Return ONLY a valid JSON object with this exact structure (no additional text):
{{
  "week_plan": {{
    "monday": {{
      {', '.join([f'"{meal}": {{"name": "Recipe Name", "prep_time": "X minutes", "ingredients": ["ingredient 1", "ingredient 2"], "instructions": ["step 1", "step 2"], "calories": 000, "protein": "00g"}}' for meal in meal_list])}
    }},
    "tuesday": {{ ... same structure ... }},
    "wednesday": {{ ... same structure ... }}
  }}
}}

Remember: Return ONLY the JSON object, no explanations or markdown formatting."""
    
    return prompt

def get_meal_plan_from_llm(prompt):
    """
    Send prompt to LLM API and return the raw response.
    """
    provider = os.getenv("LLM_PROVIDER", "openai")
    
    if provider == "openai":
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
                    "role": "system",
                    "content": "You are a professional nutritionist. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        try:
            with httpx.Client() as client:
                response = client.post(url, json=data, headers=headers, timeout=60.0)
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content'], None
                else:
                    return None, f"API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return None, f"Connection Error: {str(e)}"
    
    else:
        # Gemini implementation would go here
        return None, "Gemini API not yet implemented"

def parse_llm_response(response_text):
    """
    Parse the LLM's JSON response into a Python dictionary.
    Handles errors gracefully.
    """
    try:
        # Clean the response - remove markdown formatting if present
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        # Parse JSON
        meal_plan = json.loads(cleaned)
        
        # Validate structure
        if "week_plan" not in meal_plan:
            return None, "Invalid response structure: missing 'week_plan'"
        
        days = ["monday", "tuesday", "wednesday"]  # Only validate 3 days for testing
        for day in days:
            if day not in meal_plan["week_plan"]:
                return None, f"Invalid response structure: missing '{day}'"
        
        return meal_plan, None
        
    except json.JSONDecodeError as e:
        return None, f"Failed to parse JSON: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

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

st.set_page_config(
    page_title="Healthy Meals AI",
    page_icon="🥗",
    layout="wide"
)

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'onboarding'
if 'preferences' not in st.session_state:
    st.session_state.preferences = {}
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = None

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
    if st.button(
        "🚀 Generate My Weekly Plan",
        type="primary",
        use_container_width=True
    ):
        # Capture preferences and transition to plan view
        st.session_state.preferences = {
            'user_profile': user_profile,
            'excluded_foods': excluded_foods,
            'meals_per_day': meals_per_day
        }
        st.session_state.stage = 'generating'
        st.session_state.meal_plan = None  # Clear any existing plan
        st.rerun()

# Main content area based on current stage
if st.session_state.stage == 'onboarding':
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

elif st.session_state.stage == 'generating':
    # Generation phase - show spinner and generate meal plan
    st.markdown("## 🚀 Generating Your Personalized Meal Plan...")
    
    with st.spinner("Creating your meal plan... This may take up to 60 seconds..."):
        # Generate the prompt
        prompt = construct_llm_prompt(st.session_state.preferences)
        
        # Call the LLM API
        response_text, error = get_meal_plan_from_llm(prompt)
        
        if error:
            st.error(f"❌ Failed to generate meal plan: {error}")
            st.info("Please try again or check your API configuration.")
            if st.button("← Back to Preferences"):
                st.session_state.stage = 'onboarding'
                st.rerun()
        else:
            # Parse the response
            meal_plan, parse_error = parse_llm_response(response_text)
            
            if parse_error:
                st.error(f"❌ Failed to parse meal plan: {parse_error}")
                st.info("Please try again - the AI response was not in the expected format.")
                if st.button("← Back to Preferences"):
                    st.session_state.stage = 'onboarding'
                    st.rerun()
            else:
                # Success! Store and display
                st.session_state.meal_plan = meal_plan
                st.session_state.stage = 'plan_view'
                st.rerun()

elif st.session_state.stage == 'plan_view':
    # Plan view - display the generated meal plan
    st.markdown("## 🥗 Your Personalized 3-Day Meal Plan")
    
    if st.session_state.meal_plan:
        # Display preferences
        with st.expander("📋 Your Preferences", expanded=False):
            st.write("**Profile:**", st.session_state.preferences.get('user_profile'))
            st.write("**Excluded Foods:**", st.session_state.preferences.get('excluded_foods') or "None")
            st.write("**Meals per Day:**", st.session_state.preferences.get('meals_per_day'))
        
        st.divider()
        
        # Display the 3-day meal plan using columns
        days = ["monday", "tuesday", "wednesday"]
        day_names = ["Monday", "Tuesday", "Wednesday"] 
        
        cols = st.columns(3)
        
        for i, (day, day_name) in enumerate(zip(days, day_names)):
            with cols[i]:
                st.subheader(f"📅 {day_name}")
                
                if day in st.session_state.meal_plan["week_plan"]:
                    day_meals = st.session_state.meal_plan["week_plan"][day]
                    
                    # Display each meal for this day
                    for meal_type, meal_data in day_meals.items():
                        with st.expander(f"🍽️ {meal_type.title()}", expanded=False):
                            st.markdown(f"**{meal_data.get('name', 'Unknown Recipe')}**")
                            st.write(f"⏱️ **Prep Time:** {meal_data.get('prep_time', 'N/A')}")
                            
                            if meal_data.get('calories'):
                                st.write(f"🔥 **Calories:** {meal_data.get('calories')}")
                            if meal_data.get('protein'):
                                st.write(f"💪 **Protein:** {meal_data.get('protein')}")
                            
                            if meal_data.get('ingredients'):
                                st.write("**🥑 Ingredients:**")
                                for ingredient in meal_data['ingredients']:
                                    st.write(f"• {ingredient}")
                            
                            if meal_data.get('instructions'):
                                st.write("**👩‍🍳 Instructions:**")
                                for j, instruction in enumerate(meal_data['instructions'], 1):
                                    st.write(f"{j}. {instruction}")
                else:
                    st.error(f"No meal plan data for {day_name}")
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Generate New Plan"):
                st.session_state.stage = 'generating'
                st.session_state.meal_plan = None
                st.rerun()
        
        with col2:
            if st.button("← Back to Preferences"):
                st.session_state.stage = 'onboarding'
                st.rerun()
    
    else:
        st.error("No meal plan data available. Please generate a new plan.")
        if st.button("← Back to Preferences"):
            st.session_state.stage = 'onboarding'
            st.rerun()

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