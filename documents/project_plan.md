# Healthy Meals AI Project Plan

**Version:** 1.0 **Date:** August 12, 2025 **Objective:** To provide a phased development roadmap for building the working prototype using Streamlit, a sidebar UI, and a live LLM for recipe generation.

#### **Phase 1: Foundation & API Setup**

- **Goal:** Establish the project environment and verify successful communication with the LLM API.
    
- **Deliverables:**
    
    1. Initialized local Git repository and a Python virtual environment created using `uv venv`.
        
    2. Dependencies (`streamlit`, `pandas`, `httpx`) installed using `uv add`.
        
    3. Secure setup for the LLM API key using Streamlit's secrets management (`.streamlit/secrets.toml`).
        
    4. A basic `app.py` script that makes a test call to the LLM API and prints the response to the terminal.
        
- **Dependencies:** Access to an LLM API, `uv` installed.
    
- **Validation:**
    
    - ✅ The `streamlit run app.py` command executes without error.
        
    - ✅ The script successfully receives and displays a response from the LLM API.
        

#### **Phase 2: UI Scaffolding with Sidebar**

- **Goal:** Build the static user interface based on the Design Guidelines.
    
- **Deliverables:**
    
    1. An `app.py` script that uses `st.sidebar` to display all the UI widgets for user preferences (multiselect, text input, slider, radio buttons).
        
    2. A prominent "Generate My Weekly Plan" button located at the bottom of the sidebar.
        
    3. The main content area displays a simple welcome message and a call-to-action pointing the user to the controls in the sidebar.
        
- **Dependencies:** Phase 1.
    
- **Validation:**
    
    - ✅ The app layout renders correctly with a sidebar for controls and a main content area.
        
    - ✅ All UI widgets are present in the sidebar as per the text wireframe. Interactivity is not required yet.
        

#### **Phase 3: State Management & Onboarding Logic**

- **Goal:** Make the sidebar form interactive and manage the application's state.
    
- **Deliverables:**
    
    1. Implementation of `st.session_state` to manage the application's view (e.g., `st.session_state.stage`) and store user preferences.
        
    2. Logic that captures all inputs from the sidebar widgets and stores them in `st.session_state` when the "Generate My Weekly Plan" button is clicked.
        
    3. The main content area transitions from the welcome message to a placeholder "plan view" upon button click.
        
- **Dependencies:** Phase 2.
    
- **Validation:**
    
    - ✅ After filling out the form and clicking the button, the selected preferences can be printed to the terminal to confirm they were saved correctly in the session state.
        

#### **Phase 4: LLM Prompt Engineering & Response Parsing**

- **Goal:** Develop the core logic to prompt the LLM and reliably parse its response.
    
- **Deliverables:**
    
    1. A Python function `construct_llm_prompt(preferences)` that creates a detailed text prompt based on the user's stored preferences, explicitly instructing the LLM to return a **JSON object**.
        
    2. A function `get_meal_plan_from_llm(prompt)` that handles the API call and returns the raw response.
        
    3. A robust `parse_llm_response(response)` function that converts the LLM's JSON string into a clean Python dictionary and handles potential parsing errors.
        
- **Dependencies:** Phase 1.
    
- **Validation:**
    
    - ✅ The prompt function generates a clear, detailed prompt incorporating user choices.
        
    - ✅ The parsing function successfully converts a sample valid JSON response into the expected Python dictionary format and gracefully handles a sample invalid one.
        

#### **Phase 5: Displaying the Meal Plan**

- **Goal:** Render the dynamically generated meal plan in the main content area.
    
- **Deliverables:**
    
    1. Integration of the Phase 4 functions into `app.py`.
        
    2. When the user clicks "Generate," the LLM is called, and the resulting parsed plan is displayed in the main content area.
        
    3. The UI uses `st.columns` for the 7-day layout and `st.expander` for each meal, allowing users to view recipe details.
        
    4. A loading spinner (`st.spinner`) is shown during the API call.
        
- **Dependencies:** Phase 3, Phase 4.
    
- **Validation:**
    
    - ✅ A 7-day meal plan is displayed on the screen after the loading spinner.
        
    - ✅ The plan's content clearly reflects the preferences selected in the sidebar.
        

#### **Phase 6: Grocery List Generation & Display**

- **Goal:** Create and display a consolidated, categorized grocery list for the week.
    
- **Deliverables:**
    
    1. A "Create Grocery List" button is added to the UI (e.g., as a tab or below the meal plan).
        
    2. A Python function that iterates through the generated meal plan dictionary, aggregates all ingredients, and consolidates quantities.
        
    3. A new view that displays the ingredients grouped by category (e.g., Produce, Proteins, Pantry).
        
- **Dependencies:** Phase 5.
    
- **Validation:**
    
    - ✅ The grocery list correctly aggregates ingredients from the generated plan.
        
    - ✅ The list is clearly categorized and easy to read.
        

#### **Phase 7: Styling and Visual Polish**

- **Goal:** Apply the visual design to transform the functional app into a polished prototype.
    
- **Deliverables:**
    
    1. Implementation of the color palette, typography, and spacing defined in the Design Guidelines.
        
    2. Addition of emoji icons to enhance visual appeal.
        
    3. A clean, professional-looking UI that aligns with the "Healthy, Calm, and Clear" philosophy.
        
- **Dependencies:** Phase 6.
    
- **Validation:**
    
    - ✅ The prototype's visual appearance matches the Design Guidelines.
        
    - ✅ The application feels cohesive and professionally designed.
        

#### **Phase 8: Final Review, Error Handling & Deployment**

- **Goal:** Ensure the prototype is robust, bug-free, and shareable.
    
- **Deliverables:**
    
    1. Implementation of user-facing error handling (e.g., for API failures or parsing errors).
        
    2. A `requirements.txt` file generated using `uv pip freeze > requirements.txt`.
        
    3. The project code pushed to a GitHub repository.
        
    4. The application successfully deployed to Streamlit Community Cloud, with API keys configured in the deployment environment.
        
- **Dependencies:** Phase 7.
    
- **Validation:**
    
    - ✅ The entire user flow can be completed on the live, deployed app without errors.
        
    - ✅ The app handles API errors gracefully with a user-friendly message.
        
    - ✅ The prototype is accessible via a public URL.