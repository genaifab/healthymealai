# HealthyMeals AI Technical Context Document

**Version:** 2.0 **Date:** Updated December 2024 **Original Author:** [Your Name/Startup Name]  

### **1.0 Introduction**

- **1.1 Purpose:** This document outlines the technology stack, application architecture, and key technical decisions for the HealthyMeals AI prototype. It provides a clear, Python-native, and efficient development path for building a Streamlit application that interfaces directly with Large Language Models (LLMs).
    
- **1.2 Guiding Principles:**
    
    - **Python-Native:** The entire application is built in Python using a single `app.py` file.
        
    - **Speed to Prototype:** Leverages Streamlit's capabilities for rapid interactive web app development.
        
    - **API-Centric:** Architecture centered around constructing precise prompts, calling OpenAI's API, and reliably parsing structured JSON responses.
        
    - **Production-Ready:** Uses environment variables for configuration, making deployment flexible across platforms.
        

### **2.0 Technology Stack (As Implemented)**

- **2.1 Application Framework: Streamlit v1.48.0**
    
    - **Implementation:** Single-page app with sidebar navigation and session state management.
    - **Why:** Streamlit turns Python scripts into shareable web apps without requiring separate front-end development.
        
- **2.2 Core Language: Python 3.13**
    
    - **Implementation:** All application logic in a single `app.py` file (871 lines).
    - **Why:** Natural choice for AI/data applications and Streamlit's native language.
        
- **2.3 Package & Environment Management: uv**
    
    - **Implementation:** Virtual environment managed via `uv sync`, dependencies in `pyproject.toml`.
    - **Why:** Modern, high-performance tool for Python package management.
        
- **2.4 API Communication: httpx v0.28.1**
    
    - **Implementation:** Used for all OpenAI API calls with 60-second timeout for meal generation.
    - **Why:** Modern HTTP client supporting synchronous operations with robust error handling.
        
- **2.5 Data Handling: Pandas v2.3.1**
    
    - **Implementation:** Used for structuring meal plan data and grocery list aggregation.
    - **Why:** Powerful data manipulation for parsing and organizing LLM responses.
        
- **2.6 Configuration Management: python-dotenv v1.1.1**
    
    - **Implementation:** `.env` file for API keys and configuration, NOT Streamlit secrets.
    - **Why:** Platform-agnostic deployment (works on Render, Heroku, etc.), easier local development.
        
- **2.7 Deployment Target: Flexible (Render, Streamlit Cloud, Heroku)**
    
    - **Implementation:** Uses environment variables making it deployable to any platform.
    - **Requirements.txt:** Minimal dependencies for easy deployment.
        

### **3.0 Application Architecture (As Built)**

- **3.1 Overall Architecture: Single-Script Web App**
    
    - **Implementation:** Complete application in `app.py` with inline functions.
    - **Structure:** Functions defined at top, Streamlit UI code follows, no separate modules.
        
- **3.2 State Management & User Flow:**
    
    - **Session State Variables:**
        - `stage`: Current view ('onboarding', 'generating', 'plan_view', 'grocery_list')
        - `preferences`: User's dietary selections
        - `meal_plan`: Generated meal plan JSON
        - `grocery_list`: Aggregated shopping list
        - `selected_model`: Currently selected OpenAI model
    
    - **Application Flow:** Conditional rendering based on `st.session_state.stage`.
        
- **3.3 Core Functions:**
    
    1. **`construct_llm_prompt(preferences)`**
        - Maps user profiles to dietary requirements
        - Handles emoji prefixes in UI selections
        - Creates structured JSON prompt for 1-day or 3-day plans
        - Explicitly requests JSON-only response
    
    2. **`get_meal_plan_from_llm(prompt, model=None)`**
        - Uses OpenAI API (Gemini scaffolding present but not implemented)
        - Configurable model selection (GPT-4o-mini, GPT-4o, GPT-4-turbo, GPT-3.5-turbo)
        - 60-second timeout for API calls
        - Returns raw response text or error message
    
    3. **`parse_llm_response(response)`**
        - Validates JSON structure
        - Handles malformed responses gracefully
        - Returns parsed dictionary or error
    
    4. **`generate_grocery_list(meal_plan)`**
        - Smart ingredient categorization (Produce, Proteins, Dairy, Grains & Pantry, Frozen, Other)
        - Deduplication and quantity consolidation
        - Returns categorized dictionary
        
- **3.4 Data Flow (As Implemented):**
    
    1. User configures preferences in sidebar (model, profile, exclusions, duration, meals)
    2. Preferences saved to `st.session_state`
    3. Button click triggers stage change to 'generating'
    4. `construct_llm_prompt()` creates JSON-formatted prompt
    5. `get_meal_plan_from_llm()` calls OpenAI API with selected model
    6. `parse_llm_response()` validates and parses JSON response
    7. Meal plan displayed with expandable recipe cards
    8. Grocery list generated on demand with smart categorization
        

### **4.0 Integration Details**

- **4.1 OpenAI API Integration:**
    
    - **Authentication:** API key from `.env` file via `os.getenv("OPENAI_API_KEY")`
    - **Models Supported:** GPT-4o-mini (default), GPT-4o, GPT-4-turbo, GPT-3.5-turbo
    - **Token Limits:** 4000 max_tokens for all models
    - **Temperature:** 0.7 for balanced creativity
    - **Error Handling:** Comprehensive error messages for connection, authentication, rate limits
    
- **4.2 Configuration Management:**
    
    - **NOT USING Streamlit Secrets:** Decision made for deployment flexibility
    - **Using .env file:**
        ```env
        OPENAI_API_KEY=sk-proj-...
        LLM_PROVIDER=openai
        OPENAI_MODEL=gpt-4o-mini
        ```
    - **Deployment:** Environment variables set on hosting platform
    

### **5.0 UI/UX Implementation**

- **5.1 Design System:**
    
    - **Typography:** Poppins font family via Google Fonts
    - **Color Palette:**
        - Primary Green: #2E8B57
        - Accent Orange: #FFA500
        - Neutral Text: #333333
        - Subtle Gray: #F5F5F5
    - **Layout:** Sidebar for controls, main area for content
    - **Visual Elements:** Emojis for sections and visual enhancement
    
- **5.2 User Interface Components:**
    
    - **Sidebar:**
        - Model selector dropdown
        - User profile radio buttons
        - Excluded foods text input
        - Plan duration radio (1-day or 3-day)
        - Meals per day radio
        - Generate button
    
    - **Main Area:**
        - Welcome/instructions (onboarding stage)
        - Loading spinner (generating stage)
        - Meal plan grid with expandable cards (plan_view stage)
        - Categorized grocery list (grocery_list stage)
        

### **6.0 Performance & Error Handling**

- **6.1 Performance Optimizations:**
    
    - **API Timeout:** 60 seconds for meal plan generation
    - **Loading Feedback:** Spinner with encouraging messages during generation
    - **Session State:** Preserves data across reruns avoiding redundant API calls
    
- **6.2 Error Handling (Enhanced in v1.0.0):**
    
    - **Connection Errors:** Clear messaging about internet/service issues
    - **Authentication Errors:** Specific guidance for API key problems
    - **Rate Limiting:** Instructions to wait before retrying
    - **Parsing Errors:** Technical details in expandable section for debugging
    - **Model Compatibility:** Removed non-working GPT-5 models, safe fallback to GPT-4o-mini
    
- **6.3 User Experience:**
    
    - **Progressive Disclosure:** Expandable recipe details reduce visual clutter
    - **Clear Navigation:** Action buttons for moving between views
    - **Error Recovery:** Always provides path back to preferences
    

### **7.0 Deployment Configuration**

- **7.1 Required Files:**
    
    - `app.py`: Main application (871 lines)
    - `.env`: Configuration (not in repo)
    - `.env.example`: Template for configuration
    - `requirements.txt`: Minimal dependencies
    - `pyproject.toml`: uv project configuration
    
- **7.2 Environment Variables:**
    
    - `OPENAI_API_KEY`: Required for API access
    - `LLM_PROVIDER`: Set to 'openai' (Gemini not implemented)
    - `OPENAI_MODEL`: Default model selection (optional)
    
- **7.3 Deployment Platforms:**
    
    - **Render:** Primary target, uses .env variables
    - **Streamlit Cloud:** Supported via requirements.txt
    - **Heroku:** Compatible with Procfile addition
    - **Local:** uv for development environment
    

### **8.0 Development Workflow**

- **8.1 Local Setup:**
    ```bash
    git clone https://github.com/genaifab/healthymealai.git
    cd healthymealai
    uv sync
    cp .env.example .env
    # Add API key to .env
    uv run streamlit run app.py
    ```
    
- **8.2 Development Commands:**
    ```bash
    # Run application
    uv run streamlit run app.py
    
    # Add dependencies
    uv add package-name
    
    # Generate requirements.txt
    uv pip freeze > requirements.txt
    ```
    
- **8.3 Version History:**
    - v0.1-v0.4: Foundation through LLM integration
    - v0.5-v0.6: Meal plan display and grocery lists
    - v0.7.1: Model selection enhancement
    - v1.0.0: Production release with stable models
    

### **9.0 Key Technical Decisions**

1. **Single File Architecture:** Chose simplicity over modularity for prototype speed
2. **.env over Streamlit Secrets:** Platform flexibility was prioritized
3. **No Database:** Session state only, no persistence between sessions
4. **JSON-Only LLM Responses:** Structured data for reliable parsing
5. **60-Second Timeout:** Balance between complex plans and user patience
6. **Removed GPT-5 Models:** Stability over bleeding-edge features
7. **Smart Categorization:** Hard-coded categories for grocery list organization

### **10.0 Future Considerations**

- **Potential Enhancements:**
    - User accounts and meal plan history
    - Recipe regeneration for individual meals
    - Nutritional analysis integration
    - Shopping list export formats
    - Multi-language support
    
- **Technical Debt:**
    - Single file could be modularized for larger team development
    - No automated testing framework
    - Hard-coded ingredient categories could use ML classification
    
- **Scaling Considerations:**
    - Would need database for user persistence
    - Consider caching common meal plans
    - Rate limiting for multi-user deployment