# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HealthyMeals AI is a Streamlit-based prototype application that leverages Large Language Models (LLMs) to generate personalized meal plans for busy professionals. The app focuses on whole, non-processed foods and creates weekly meal plans based on user dietary preferences.

## Technology Stack

- **Framework**: Streamlit (Python web app framework)
- **Language**: Python 3.13
- **Package Manager**: uv (for virtual environment and dependency management)
- **LLM Integration**: External API (Gemini or OpenAI)
- **Data Processing**: Pandas
- **HTTP Client**: httpx
- **Deployment Target**: Streamlit Community Cloud

## Development Commands

### Environment Setup
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv add streamlit pandas httpx

# Install from pyproject.toml
uv pip install -e .
```

### Running the Application
```bash
# Run the main application (when app.py is created)
streamlit run app.py

# Run the current placeholder
python main.py
```

### Dependency Management
```bash
# Add a new dependency
uv add <package-name>

# Generate requirements.txt for deployment
uv pip freeze > requirements.txt
```

## Architecture & Key Components

### Application Structure
The application follows a single-script architecture with modular logic:

1. **Main Script (`app.py`)**: Orchestrates the entire application using Streamlit
2. **State Management**: Uses `st.session_state` to track user progress through stages:
   - `'onboarding'`: User preference collection
   - `'plan_view'`: Display generated meal plan
   - `'grocery_list'`: Show consolidated shopping list

### Core Modules (to be implemented)

1. **LLM Interaction Module**:
   - `construct_llm_prompt(preferences)`: Builds detailed JSON-formatted prompt from user preferences
   - `get_meal_plan_from_llm(prompt)`: Handles API authentication and calls
   - `parse_llm_response(response)`: Validates and parses JSON response with error handling

2. **UI Components**:
   - **Sidebar**: All user controls and preferences (dietary restrictions, excluded foods, cooking time, meals per day)
   - **Main Area**: Displays generated content (welcome message → meal plan → grocery list)

3. **Data Flow**:
   ```
   User Input (Sidebar) → Session State → LLM Prompt → API Call → JSON Response → Parse → Display
   ```

### Key Design Patterns

- **Sidebar-based Navigation**: All controls in `st.sidebar`, content in main area
- **Session State Management**: Track user journey and store preferences
- **Error Handling**: Graceful handling of API failures and JSON parsing errors
- **Loading Feedback**: Use `st.spinner()` during API calls

## Important Implementation Notes

### LLM Integration
- **Critical**: Always request structured JSON output from the LLM in prompts
- Store API keys securely in `.streamlit/secrets.toml` (never hardcode)
- Include robust error handling for malformed JSON responses

### UI/UX Guidelines
- Follow "Healthy, Calm, and Clear" design philosophy
- Use color palette:
  - Primary Green: `#2E8B57`
  - Action Orange: `#FFA500`
  - Text: `#333333`
  - Background: `#F5F5F5`
- Typography: Poppins font family
- Use emojis for visual enhancement (🥗 meals, 🥑 ingredients, 🛒 grocery list)

### Performance Considerations
- Wrap API calls in `st.spinner()` for user feedback
- Use `@st.cache_data` decorator for cacheable helper functions
- Handle API timeouts and rate limits gracefully

## Development Phases (from Project Plan)

Current project is in initial setup phase. The planned development follows:

1. **Phase 1**: Foundation & API Setup (environment, dependencies, API connection)
2. **Phase 2**: UI Scaffolding with Sidebar
3. **Phase 3**: State Management & Onboarding Logic
4. **Phase 4**: LLM Prompt Engineering & Response Parsing
5. **Phase 5**: Displaying the Meal Plan
6. **Phase 6**: Grocery List Generation & Display
7. **Phase 7**: Styling and Visual Polish
8. **Phase 8**: Final Review, Error Handling & Deployment

## Key Features to Implement

1. **User Onboarding**: Capture dietary preferences via sidebar form
2. **Live AI Generation**: Generate weekly meal plans via LLM API
3. **Dynamic Recipe View**: Expandable recipe details for each meal
4. **Consolidated Grocery List**: Aggregated, categorized shopping list

## Testing Approach

Currently no test framework is configured. When implementing tests:
- Consider using pytest for unit tests
- Test LLM response parsing with various JSON structures
- Validate error handling for API failures
- Test state management transitions

## Security Notes

- Never commit API keys or secrets
- Use Streamlit's secrets management for sensitive data
- Validate and sanitize all user inputs before sending to LLM
- Handle PII data according to privacy requirements