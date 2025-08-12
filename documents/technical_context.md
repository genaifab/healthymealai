
# HealthyMeals AI Technical Context Document

**Version:** 1.0 **Date:** August 12, 2025 **Author:** [Your Name/Startup Name]  
### **1.0 Introduction**

- **1.1 Purpose:** This document outlines the recommended technology stack, application architecture, and key technical decisions for the working prototype. Its goal is to provide a clear, Python-native, and efficient development path for building a Streamlit application that interfaces directly with a Large Language Model (LLM).
    
- **1.2 Guiding Principles:**
    
    - **Python-Native:** The entire application, from UI to logic, will be built in Python.
        
    - **Speed to Prototype:** Leverage Streamlit's capabilities to build a functional, interactive web app quickly.
        
    - **API-Centric:** The architecture is centered around constructing a precise prompt, calling an external LLM API, and reliably parsing the structured response.
        

### **2.0 Recommended Technology Stack**

- **2.1 Application Framework: Streamlit**
    
    - **Why:** Streamlit turns Python scripts into shareable web apps, making it the ideal tool for data-centric prototypes and eliminating the need for separate front-end development.
        
- **2.2 Core Language: Python**
    
    - **Why:** The natural choice for AI/data applications and the language Streamlit is built on.
        
- **2.3 Package & Environment Management: `uv`**
    
    - **Why:** A modern, high-performance tool that will be used to create the virtual environment (`uv venv`) and manage all project dependencies (`uv add`).
        
- **2.4 API Communication: `httpx`**
    
    - **Why:** A modern, fully featured HTTP client for Python that supports synchronous and asynchronous operations, which is beneficial for handling API calls efficiently.
        
- **2.5 Data Handling: Pandas**
    
    - **Why:** While the LLM is the data source, Pandas remains invaluable for structuring, analyzing, and manipulating the parsed JSON response into a DataFrame for easier aggregation (like creating the grocery list).
        
- **2.6 Deployment: Streamlit Community Cloud**
    
    - **Why:** Offers a simple, free, and native way to deploy the prototype directly from a GitHub repository.
        

### **3.0 Application Architecture**

- **3.1 Overall Architecture: Single-Script Web App with Modular Logic**
    
    - The prototype will be orchestrated from a main `app.py` script. However, the core LLM interaction logic should be modularized for clarity and testability.
        
- **3.2 State Management & User Flow:**
    
    - **Stateful Logic:** We will use Streamlit's `st.session_state` to track the user's progress (e.g., `'onboarding'`, `'plan_view'`) and store their preferences from the UI.
        
    - **Application Flow:** The `app.py` script will use conditional logic based on `st.session_state.stage` to render the appropriate view, creating a multi-page feel within a single script.
        
- **3.3 LLM Interaction Module:**
    
    - This is the core of the application's "brain." It consists of three key parts:
        
    
    1. **Prompt Engineering:** A function `construct_llm_prompt(preferences)` will take the user's preferences from `st.session_state` and build a detailed, explicit prompt. **Crucially, this prompt will instruct the LLM to return its response as a well-structured JSON object.**
        
    2. **API Client:** A function `get_meal_plan_from_llm(prompt)` will handle the actual API call to the LLM. It will manage authentication using `st.secrets`, send the prompt, and handle potential HTTP errors.
        
    3. **Response Parser:** A function `parse_llm_response(response)` will take the raw JSON string from the LLM, validate its structure, and parse it into a clean Python dictionary or Pandas DataFrame. This function must include robust error handling for cases where the LLM returns malformed JSON.
        
- **3.4 Data Flow:**
    
    1. User fills out the **Onboarding UI**.
        
    2. Preferences are saved to `st.session_state`.
        
    3. `construct_llm_prompt()` creates the API prompt.
        
    4. `get_meal_plan_from_llm()` sends the prompt and gets a JSON string back.
        
    5. `parse_llm_response()` converts the string to a Python dictionary.
        
    6. The dictionary is stored in `st.session_state` and used to render the **Plan View** and **Grocery List**.
        

### **4.0 Integration Requirements**

- **4.1 External API Integration:**
    
    - The application will connect to a third-party LLM API (e.g., Gemini, OpenAI).
        
    - API keys **must** be stored securely. They should never be hardcoded in the script.
        
- **4.2 Internal Integration:** All internal integration is handled within the Streamlit script via function calls and access to the session state.
    

### **5.0 Performance & UX Considerations**

- **5.1 Perceived Performance:** The API call to the LLM will be the most time-consuming step. It is essential to provide immediate user feedback by wrapping the API call in a `st.spinner("Our AI is crafting your personalized plan...")`.
    
- **5.2 Error Handling:** The application must gracefully handle potential failure points:
    
    - **API Errors:** Display a user-friendly message if the LLM API is unavailable or returns an error code.
        
    - **Parsing Errors:** If the LLM returns a response that is not valid JSON, the app should not crash. It should catch the exception and display a message like, "There was an issue generating the plan. Please try adjusting your request or try again."
        
- **5.3 Caching:** While the primary data is dynamic, helper functions or static assets can be cached using Streamlit's caching decorators (`@st.cache_data`) to optimize performance where applicable.