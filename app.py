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
    # Map user profiles to dietary requirements (handle emoji prefixes)
    profile_map = {
        "🥗 Standard Healthy Eating": "Focus on whole foods, balanced nutrition, lean proteins, whole grains, and plenty of vegetables. Avoid processed foods.",
        "Standard Healthy Eating": "Focus on whole foods, balanced nutrition, lean proteins, whole grains, and plenty of vegetables. Avoid processed foods.",
        "🍃 Low-Sugar/Pre-Diabetic Friendly": "Low glycemic index foods only. NO added sugars, NO refined carbohydrates, NO white bread/pasta/rice. Focus on complex carbs, lean proteins, and non-starchy vegetables.",
        "Low-Sugar/Pre-Diabetic Friendly": "Low glycemic index foods only. NO added sugars, NO refined carbohydrates, NO white bread/pasta/rice. Focus on complex carbs, lean proteins, and non-starchy vegetables.",
        "🌱 Vegetarian": "No meat or fish. Include diverse plant proteins (legumes, tofu, tempeh, quinoa). Ensure complete proteins and adequate B12, iron, and omega-3 sources.",
        "Vegetarian": "No meat or fish. Include diverse plant proteins (legumes, tofu, tempeh, quinoa). Ensure complete proteins and adequate B12, iron, and omega-3 sources.",
        "🌾 Gluten-Free": "Absolutely NO wheat, barley, rye, or cross-contaminated oats. Use rice, quinoa, corn, certified gluten-free oats, and other safe grains.",
        "Gluten-Free": "Absolutely NO wheat, barley, rye, or cross-contaminated oats. Use rice, quinoa, corn, certified gluten-free oats, and other safe grains."
    }
    
    dietary_requirements = profile_map.get(preferences['user_profile'], "")
    excluded_foods = preferences.get('excluded_foods', '')
    plan_duration = preferences.get('plan_duration', '3-Day Meal Plan')
    meals_per_day = preferences.get('meals_per_day', 'Breakfast, Lunch, Dinner')
    
    # Determine which meals to include (handle emoji prefixes)
    if "Breakfast" in meals_per_day or "🌅" in meals_per_day:
        meal_list = ["breakfast", "lunch", "dinner"]
    else:
        meal_list = ["lunch", "dinner"]
    
    # Determine number of days and day structure
    if "1-Day" in plan_duration:
        num_days = 1
        days_structure = '"monday": { ... same structure ... }'
        days_list = ["monday"]
    else:  # 3-Day
        num_days = 3
        days_structure = '"monday": { ... same structure ... }, "tuesday": { ... same structure ... }, "wednesday": { ... same structure ... }'
        days_list = ["monday", "tuesday", "wednesday"]
    
    prompt = f"""You are a professional nutritionist creating a personalized {num_days}-day meal plan.

DIETARY REQUIREMENTS:
{dietary_requirements}

EXCLUDED FOODS (must not appear in any recipe):
{excluded_foods if excluded_foods else "None"}

MEALS NEEDED PER DAY:
{', '.join(meal_list)}

Create a complete {num_days}-day meal plan following these rules:
1. Use ONLY whole, non-processed ingredients
2. Each recipe should be completable in 45 minutes or less
3. Provide variety - no recipe should repeat{' across days' if num_days > 1 else ''}
4. Include complete nutritional balance for each day
5. Recipes should be practical for busy professionals

Return ONLY a valid JSON object with this exact structure (no additional text):
{{
  "week_plan": {{
    {days_structure.replace('{ ... same structure ... }', '{ ' + ', '.join([f'"{meal}": {{"name": "Recipe Name", "prep_time": "X minutes", "ingredients": ["ingredient 1", "ingredient 2"], "instructions": ["step 1", "step 2"], "calories": 000, "protein": "00g"}}' for meal in meal_list]) + ' }')}
  }}
}}

Remember: Return ONLY the JSON object, no explanations or markdown formatting."""
    
    return prompt

def get_meal_plan_from_llm(prompt, model=None):
    """
    Send prompt to LLM API and return the raw response.
    """
    provider = os.getenv("LLM_PROVIDER", "openai")
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        # Use provided model or fall back to environment variable or default
        if model is None:
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

def generate_grocery_list(meal_plan):
    """
    Generate a consolidated grocery list from the meal plan.
    Aggregates ingredients and categorizes them.
    """
    # Ingredient categorization
    categories = {
        "Produce": ["tomato", "onion", "garlic", "bell pepper", "spinach", "lettuce", "carrot", "celery", 
                   "cucumber", "avocado", "lemon", "lime", "apple", "banana", "berry", "broccoli", 
                   "zucchini", "mushroom", "potato", "sweet potato", "herbs", "parsley", "cilantro",
                   "basil", "arugula", "kale", "cabbage", "cauliflower", "asparagus", "green beans"],
        
        "Proteins": ["chicken", "beef", "pork", "fish", "salmon", "tuna", "shrimp", "eggs", "tofu", 
                    "tempeh", "beans", "lentils", "chickpeas", "quinoa", "nuts", "almonds", "walnuts",
                    "peanuts", "seeds", "chia", "hemp", "turkey", "lamb"],
        
        "Dairy": ["milk", "cheese", "yogurt", "butter", "cream", "sour cream", "cottage cheese",
                 "mozzarella", "parmesan", "feta", "ricotta", "greek yogurt"],
        
        "Grains & Pantry": ["rice", "bread", "pasta", "flour", "oats", "cereal", "crackers", "oil",
                           "olive oil", "coconut oil", "vinegar", "soy sauce", "salt", "pepper", 
                           "spices", "honey", "maple syrup", "stock", "broth", "canned tomatoes",
                           "coconut milk", "tahini", "peanut butter", "vanilla", "baking powder"],
        
        "Frozen": ["frozen vegetables", "frozen fruit", "frozen berries", "ice"],
        
        "Other": []  # Catch-all category
    }
    
    # Collect all ingredients
    ingredients = []
    
    for day_name, day_meals in meal_plan["week_plan"].items():
        for meal_name, meal_data in day_meals.items():
            if "ingredients" in meal_data:
                ingredients.extend(meal_data["ingredients"])
    
    # Clean and normalize ingredients
    cleaned_ingredients = []
    for ingredient in ingredients:
        # Basic cleaning - remove quantities and common prefixes
        clean_ingredient = ingredient.lower().strip()
        # Remove common quantity indicators
        clean_ingredient = clean_ingredient.replace("cups of", "").replace("cup of", "")
        clean_ingredient = clean_ingredient.replace("tablespoons of", "").replace("tablespoon of", "")
        clean_ingredient = clean_ingredient.replace("teaspoons of", "").replace("teaspoon of", "")
        clean_ingredient = clean_ingredient.replace("ounces of", "").replace("ounce of", "")
        clean_ingredient = clean_ingredient.replace("pounds of", "").replace("pound of", "")
        clean_ingredient = clean_ingredient.replace("slices of", "").replace("slice of", "")
        clean_ingredient = clean_ingredient.replace("pieces of", "").replace("piece of", "")
        clean_ingredient = clean_ingredient.replace("cloves of", "").replace("clove of", "")
        clean_ingredient = clean_ingredient.strip()
        
        if clean_ingredient:
            cleaned_ingredients.append((ingredient, clean_ingredient))  # Keep original for display
    
    # Remove duplicates while preserving original formatting
    unique_ingredients = {}
    for original, cleaned in cleaned_ingredients:
        if cleaned not in unique_ingredients:
            unique_ingredients[cleaned] = original
    
    # Categorize ingredients
    categorized_list = {category: [] for category in categories.keys()}
    
    for cleaned, original in unique_ingredients.items():
        categorized = False
        for category, keywords in categories.items():
            if category == "Other":
                continue
            for keyword in keywords:
                if keyword in cleaned:
                    categorized_list[category].append(original)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            categorized_list["Other"].append(original)
    
    # Remove empty categories and sort ingredients
    final_list = {}
    for category, items in categorized_list.items():
        if items:
            final_list[category] = sorted(set(items))
    
    return final_list

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
        
        # Determine expected days based on plan duration (fallback to 3 days if not specified)
        plan_data = meal_plan.get("week_plan", {})
        expected_days = ["monday"] if len(plan_data) == 1 else ["monday", "tuesday", "wednesday"]
        
        for day in expected_days:
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
    # Use selected model from session state
    model = st.session_state.get('selected_model', 'gpt-4o-mini')
    
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

# Custom CSS for styling and color palette
st.markdown("""
<style>
    /* Import Poppins font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Apply Poppins font globally */
    .main * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Color palette variables */
    :root {
        --primary-green: #2E8B57;
        --accent-orange: #FFA500;
        --neutral-text: #333333;
        --subtle-gray: #F5F5F5;
        --white: #FFFFFF;
    }
    
    /* Main title styling */
    .main h1 {
        color: var(--primary-green) !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    /* Header and subheader styling */
    .main h2 {
        color: var(--primary-green) !important;
        font-weight: 500 !important;
        margin-top: 2rem !important;
    }
    
    .main h3 {
        color: var(--neutral-text) !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--subtle-gray) !important;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background-color: var(--accent-orange) !important;
        border-color: var(--accent-orange) !important;
        color: var(--white) !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #E6940A !important;
        border-color: #E6940A !important;
    }
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {
        background-color: var(--primary-green) !important;
        border-color: var(--primary-green) !important;
        color: var(--white) !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #265B47 !important;
        border-color: #265B47 !important;
    }
    
    /* Regular button styling */
    .stButton > button {
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--subtle-gray) !important;
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border-color: var(--primary-green) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Radio button styling */
    .stRadio > label {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        color: var(--neutral-text) !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > label {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        color: var(--neutral-text) !important;
    }
    
    /* Success/Info message styling */
    .stSuccess {
        background-color: #D4EDDA !important;
        border-color: var(--primary-green) !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background-color: #E3F2FD !important;
        border-radius: 8px !important;
    }
    
    /* Spinner color */
    .stSpinner > div {
        border-top-color: var(--primary-green) !important;
    }
    
    /* Column spacing improvements */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Card-like appearance for meal expanders */
    .streamlit-expanderContent {
        background-color: var(--white) !important;
        border-radius: 0 0 8px 8px !important;
        padding: 1rem !important;
        border: 1px solid #E0E0E0 !important;
        border-top: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'onboarding'
if 'preferences' not in st.session_state:
    st.session_state.preferences = {}
if 'meal_plan' not in st.session_state:
    st.session_state.meal_plan = None
if 'grocery_list' not in st.session_state:
    st.session_state.grocery_list = None
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "gpt-4o-mini"

# Title in main area
st.title("🥗 Healthy Meals AI")
st.markdown("### 🌟 *Personalized meal plans for busy professionals*")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model Selection
    st.subheader("🤖 AI Model")
    
    model_options = {
        "gpt-5-nano": "GPT-5 Nano - Latest & Ultra-fast",
        "gpt-5-mini": "GPT-5 Mini - Latest & Efficient",
        "gpt-4o-mini": "GPT-4o Mini - Fast & Cost-effective",
        "gpt-4o": "GPT-4o - Balanced Performance", 
        "gpt-4-turbo": "GPT-4 Turbo - High Quality",
        "gpt-3.5-turbo": "GPT-3.5 Turbo - Basic & Speedy"
    }
    
    selected_model = st.selectbox(
        "Choose your AI model:",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=list(model_options.keys()).index(st.session_state.selected_model),
        help="Higher quality models provide better recipes but take longer and cost more"
    )
    
    # Update session state when model changes
    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.rerun()
    
    # Show confirmation of selected model
    st.success(f"✅ **Selected:** {model_options[selected_model]}")
    
    st.divider()
    st.header("🎯 Your Preferences")
    
    # User Persona Selection
    st.subheader("👤 Your Profile")
    user_profile = st.radio(
        "Which best describes you?",
        [
            "🥗 Standard Healthy Eating",
            "🍃 Low-Sugar/Pre-Diabetic Friendly", 
            "🌱 Vegetarian",
            "🌾 Gluten-Free"
        ],
        help="Select the meal plan type that best fits your needs"
    )
    
    # Excluded Foods
    st.subheader("🚫 Foods to Exclude")
    excluded_foods = st.text_input(
        "List any specific foods to avoid:",
        placeholder="e.g., mushrooms, cilantro, seafood",
        help="Separate multiple items with commas"
    )
    
    # Plan Duration
    st.subheader("📅 Plan Duration")
    plan_duration = st.radio(
        "Select your meal plan duration:",
        ["📋 1-Day Meal Plan", "📋 3-Day Meal Plan"],
        index=1,  # Default to 3-day
        help="Choose how many days of meals to generate"
    )
    
    # Meals per Day
    st.subheader("🍽️ Meals per Day")
    meals_per_day = st.radio(
        "Select your daily meals:",
        ["🌅 Breakfast, Lunch, Dinner", "☀️ Lunch, Dinner"],
        help="Choose which meals to include each day"
    )
    
    # Divider before button
    st.divider()
    
    # Generate button
    if st.button(
        "🚀 Generate My Meal Plan",
        type="primary",
        use_container_width=True
    ):
        # Capture preferences and transition to plan view
        st.session_state.preferences = {
            'user_profile': user_profile,
            'excluded_foods': excluded_foods,
            'plan_duration': plan_duration,
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
    st.markdown("*Our AI chef is crafting delicious, healthy recipes just for you...*")
    st.markdown("---")
    
    with st.spinner("🍳 Creating your meal plan... This may take up to 60 seconds..."):
        # Generate the prompt
        prompt = construct_llm_prompt(st.session_state.preferences)
        
        # Call the LLM API with selected model
        response_text, error = get_meal_plan_from_llm(prompt, st.session_state.selected_model)
        
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
    plan_duration = st.session_state.preferences.get('plan_duration', '3-Day Meal Plan')
    duration_text = plan_duration.replace(' Meal Plan', '')
    
    st.markdown(f"## 🥗 Your Personalized {duration_text} Meal Plan")
    
    if st.session_state.meal_plan:
        # Display preferences
        with st.expander("📋 Your Preferences", expanded=False):
            st.write("**Profile:**", st.session_state.preferences.get('user_profile'))
            st.write("**Plan Duration:**", st.session_state.preferences.get('plan_duration'))
            st.write("**Excluded Foods:**", st.session_state.preferences.get('excluded_foods') or "None")
            st.write("**Meals per Day:**", st.session_state.preferences.get('meals_per_day'))
        
        st.divider()
        
        # Determine days to display based on what's available in the meal plan
        available_days = list(st.session_state.meal_plan["week_plan"].keys())
        day_name_map = {
            "monday": "Monday",
            "tuesday": "Tuesday", 
            "wednesday": "Wednesday",
            "thursday": "Thursday",
            "friday": "Friday"
        }
        
        # Create columns based on number of days
        cols = st.columns(len(available_days))
        
        for i, day in enumerate(available_days):
            with cols[i]:
                day_name = day_name_map.get(day, day.title())
                st.subheader(f"📅 {day_name}")
                
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
        
        st.divider()
        
        # Action buttons with better spacing and styling
        st.markdown("---")
        st.markdown("### 🎯 What's Next?")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🛒 Create Grocery List", type="secondary", use_container_width=True):
                # Generate grocery list and switch to grocery view
                st.session_state.grocery_list = generate_grocery_list(st.session_state.meal_plan)
                st.session_state.stage = 'grocery_list'
                st.rerun()
        
        with col2:
            if st.button("🔄 Generate New Plan", use_container_width=True):
                st.session_state.stage = 'generating'
                st.session_state.meal_plan = None
                st.session_state.grocery_list = None
                st.rerun()
        
        with col3:
            if st.button("⚙️ Change Preferences", use_container_width=True):
                st.session_state.stage = 'onboarding'
                st.rerun()
    
    else:
        st.error("No meal plan data available. Please generate a new plan.")
        if st.button("← Back to Preferences"):
            st.session_state.stage = 'onboarding'
            st.rerun()

elif st.session_state.stage == 'grocery_list':
    # Grocery list view - display the consolidated shopping list
    plan_duration = st.session_state.preferences.get('plan_duration', '3-Day Meal Plan')
    duration_text = plan_duration.replace(' Meal Plan', '')
    
    st.markdown(f"## 🛒 Your {duration_text} Grocery List")
    
    if st.session_state.grocery_list:
        # Display meal plan info
        with st.expander("📋 Based on Your Meal Plan", expanded=False):
            st.write("**Profile:**", st.session_state.preferences.get('user_profile'))
            st.write("**Plan Duration:**", st.session_state.preferences.get('plan_duration'))
            st.write("**Meals per Day:**", st.session_state.preferences.get('meals_per_day'))
        
        st.divider()
        
        # Display grocery list by categories
        st.markdown("### 🥗 Organized by Store Section")
        
        # Create columns for categories (max 3 columns for readability)
        categories = list(st.session_state.grocery_list.keys())
        
        if len(categories) <= 3:
            cols = st.columns(len(categories))
        else:
            # Split into multiple rows if more than 3 categories
            cols = st.columns(3)
        
        for i, (category, items) in enumerate(st.session_state.grocery_list.items()):
            col_index = i % 3 if len(categories) > 3 else i
            
            with cols[col_index]:
                # Category emoji mapping
                category_emoji = {
                    "Produce": "🥬",
                    "Proteins": "🥩", 
                    "Dairy": "🥛",
                    "Grains & Pantry": "🌾",
                    "Frozen": "🧊",
                    "Other": "📦"
                }
                
                emoji = category_emoji.get(category, "📦")
                st.subheader(f"{emoji} {category}")
                
                # Display items as checkboxes for easy shopping
                for item in items:
                    st.markdown(f"☐ {item}")
                
                # Add some spacing between categories
                if len(categories) > 3 and (i + 1) % 3 == 0 and i < len(categories) - 1:
                    st.markdown("---")
        
        # Summary stats
        st.divider()
        total_items = sum(len(items) for items in st.session_state.grocery_list.values())
        st.info(f"📊 **Total Items:** {total_items} across {len(categories)} categories")
        
        # Action buttons with improved styling
        st.markdown("---")
        st.markdown("### 🎯 Ready to Shop?")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("📋 Back to Meal Plan", use_container_width=True):
                st.session_state.stage = 'plan_view'
                st.rerun()
        
        with col2:
            if st.button("🔄 Regenerate List", use_container_width=True):
                # Regenerate grocery list from current meal plan
                st.session_state.grocery_list = generate_grocery_list(st.session_state.meal_plan)
                st.rerun()
        
        with col3:
            if st.button("⚙️ Change Preferences", use_container_width=True):
                st.session_state.stage = 'onboarding'
                st.rerun()
    
    else:
        st.error("No grocery list data available. Please generate a meal plan first.")
        if st.button("← Back to Meal Plan"):
            st.session_state.stage = 'plan_view'
            st.rerun()

# Temporary API test section (will be removed in later phases)
st.divider()
with st.expander("🔧 API Connection Test (Development Only)"):
    st.markdown("### Testing LLM API Connection")
    
    provider = os.getenv("LLM_PROVIDER", "gemini")
    # Use selected model from session state instead of environment variable
    if provider == "openai":
        model = st.session_state.get('selected_model', 'gpt-4o-mini')
    else:
        model = "gemini-pro"
    
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
    # Use selected model from session state
    model = st.session_state.get('selected_model', 'gpt-4o-mini')
    
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