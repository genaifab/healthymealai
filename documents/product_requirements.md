### HealthyMeals AI Product Requirements Document

**Version:** 2.0 **Date:** Updated December 2024 **Original Author:** [Your Name/Startup Name]  

### **1.0 Introduction**

- **1.1 Vision:** To make healthy eating effortless for busy professionals by leveraging powerful generative AI models to create personalized meal plans using whole, non-processed foods.
    
- **1.2 Project Goal:** Successfully developed a production-ready interactive prototype that demonstrates the core user journey and the dynamic capabilities of using live Large Language Models (LLMs). This prototype showcases key features to potential investors and early-adopter customers.
    
- **1.3 Document Purpose:** This document captures the implemented requirements, features, user flows, and technical decisions of the completed HealthyMeals AI v1.0.0 prototype built with Streamlit and OpenAI's API.
    

### **2.0 The Problem & Target User**

- **2.1 Problem Statement:** Busy professionals with diverse dietary needs want to improve their health by eating whole, unprocessed foods, but lack the time and expertise for consistent meal planning. This leads them to rely on unhealthy, processed convenience foods, which negatively impacts their well-being.
    
- **2.2 Target User Personas (As Implemented):**
    
    - **2.2.1 Standard Healthy Eating (Baseline)**
        
        - **Profile Name:** "Standard Healthy Eating"
        - **Implementation:** Focuses on whole foods, balanced nutrition, lean proteins, whole grains, and plenty of vegetables
        - **Goals:** Improve energy and focus, reduce reliance on takeout and processed snacks
        - **UI Representation:** First option in profile selector with emoji icon
            
    - **2.2.2 Low-Sugar/Pre-Diabetic Friendly**
        
        - **Profile Name:** "Low-Sugar/Pre-Diabetic Friendly"
        - **Implementation:** Strictly low glycemic index foods, NO added sugars, NO refined carbohydrates
        - **Goals:** Manage blood sugar with reliable meal options for specific medical needs
        - **UI Representation:** Second option with health-focused emoji
            
    - **2.2.3 Vegetarian**
        
        - **Profile Name:** "Vegetarian"
        - **Implementation:** No meat or fish, diverse plant proteins (legumes, tofu, tempeh, quinoa)
        - **Goals:** Complete proteins with adequate B12, iron, and omega-3 sources
        - **UI Representation:** Third option with plant-based emoji
            
    - **2.2.4 Gluten-Free**
        
        - **Profile Name:** "Gluten-Free"
        - **Implementation:** Absolutely NO wheat, barley, rye, or cross-contaminated oats
        - **Goals:** Safe grain alternatives like rice, quinoa, corn, certified gluten-free oats
        - **UI Representation:** Fourth option with grain emoji
            

### **3.0 Achieved Prototype Objectives**

- **Primary Objective (✅ Achieved):** Successfully demonstrates the complete user journey:
    - Setting preferences through intuitive sidebar controls
    - Generating personalized meal plans directly from OpenAI's LLM
    - Viewing expandable recipe details with ingredients and instructions
    - Creating smart, categorized grocery lists
    
- **Secondary Objectives (✅ Achieved):**
    
    - Real-time AI personalization with unique plans based on user preferences
    - Focus on whole, non-processed foods in all generated meals
    - Clean, professional UI with Poppins typography and custom color scheme
    - Model selection capability for quality/speed trade-offs
        

### **4.0 Core Features & Functionality (As Implemented)**

- **4.1 Feature 1: User Preferences & Configuration (✅ Complete)**
    
    - **AI Model Selection:** Dropdown with 4 OpenAI models (GPT-4o-mini, GPT-4o, GPT-4-turbo, GPT-3.5-turbo)
    - **User Profile Selection:** Radio buttons for 4 dietary profiles with emoji indicators
    - **Food Exclusions:** Text input for foods to avoid (e.g., "mushrooms, cilantro")
    - **Plan Duration:** Radio selection for 1-Day or 3-Day meal plans
    - **Meals per Day:** Radio selection for 2 meals (Lunch, Dinner) or 3 meals (Breakfast, Lunch, Dinner)
    - **Implementation:** All controls in sidebar using Streamlit components
            
- **4.2 Feature 2: Live AI Meal Plan Generation (✅ Complete)**
    
    - **Generate Button:** "Generate My Meal Plan" (updated from "Weekly Plan")
    - **Loading Experience:** Spinner with encouraging message during 30-60 second generation
    - **API Integration:** OpenAI API with 60-second timeout
    - **JSON Structure:** Enforced JSON-only responses for reliable parsing
    - **Plan Flexibility:** Generates 1-day (Monday) or 3-day (Monday-Wednesday) plans
        
- **4.3 Feature 3: Dynamic Recipe View (✅ Complete)**
    
    - **Display Format:** Streamlit columns layout (3 columns for 3-day, 1 for 1-day)
    - **Expandable Cards:** Click meal names to reveal recipe details
    - **Recipe Contents:**
        - Meal name with emoji indicator
        - Prep time
        - Ingredients list (bulleted)
        - Instructions (numbered steps)
        - Nutritional info (calories, protein) when provided by LLM
    - **Visual Design:** Cards with subtle gray backgrounds and rounded corners
        
- **4.4 Feature 4: Smart Grocery List (✅ Enhanced)**
    
    - **Generation:** "Create Grocery List" button on meal plan view
    - **Categorization:** Automatic sorting into 6 categories:
        - Produce (vegetables, fruits, herbs)
        - Proteins (meats, fish, legumes, nuts)
        - Dairy (milk products, cheese, yogurt)
        - Grains & Pantry (rice, pasta, oils, spices)
        - Frozen (frozen vegetables and fruits)
        - Other (uncategorized items)
    - **Deduplication:** Smart consolidation of repeated ingredients
    - **Display:** Clean categorized view with item counts
        

### **5.0 Implemented User Flow**

1. **Landing:** User sees welcome message with instructions to use sidebar
2. **Configuration:** User selects AI model and dietary preferences in sidebar
3. **Generation:** Click "Generate My Meal Plan" triggers loading state
4. **API Call:** System sends JSON prompt to OpenAI (60-second timeout)
5. **Plan Display:** Generated meal plan appears in expandable card layout
6. **Recipe Exploration:** User clicks meals to view detailed recipes
7. **Grocery List:** Optional generation of categorized shopping list
8. **Iteration:** Options to regenerate plan or adjust preferences

### **6.0 Technical Implementation**

- **6.1 UI/UX (✅ Implemented):**
    - Poppins font family via Google Fonts
    - Color palette: Green (#2E8B57), Orange (#FFA500), Gray (#F5F5F5)
    - Responsive sidebar layout with emoji enhancements
    - Professional styling with custom CSS
    
- **6.2 LLM Integration (✅ Complete):**
    
    - **Provider:** OpenAI API (Gemini scaffolding present but not implemented)
    - **Models:** 4 stable models (removed non-working GPT-5 variants)
    - **JSON Format:** Strictly enforced structured responses
    - **Error Handling:** Comprehensive user-friendly error messages
    - **Configuration:** Environment variables via .env file (NOT Streamlit secrets)
        
- **6.3 Platform (✅ Delivered):**
    - Streamlit v1.48.0 web application
    - Single file architecture (app.py, 871 lines)
    - Session state management for data persistence
    
- **6.4 Package Management (✅ As Specified):**
    - uv for virtual environment and dependency management
    - pyproject.toml for project configuration
    - requirements.txt for deployment compatibility
    

### **7.0 Scope Boundaries (Maintained)**

**Not Implemented (As Planned):**
- User accounts or login functionality
- Data persistence between sessions
- Meal swapping or individual recipe regeneration
- Detailed macro/micronutrient tracking
- Backend database or API
- Custom AI model training

**Additional Limitations:**
- No Gemini API integration (OpenAI only)
- No 5-day or 7-day plans (1-day and 3-day only)
- No export functionality for grocery lists
- No mobile app version

### **8.0 Success Metrics (✅ Achieved)**

- **User Flow Completion:** ✅ Users can navigate entire flow without errors
    - Comprehensive error handling prevents crashes
    - Clear navigation between all application states
    
- **Personalization Demonstration:** ✅ Generated plans reflect preferences
    - Dietary restrictions properly enforced
    - Excluded foods consistently avoided
    - Meal variety maintained
    
- **Reliable Parsing:** ✅ JSON responses consistently parsed
    - Robust error handling for malformed responses
    - Technical details available for debugging
    - Fallback options for parsing failures
    
- **Value Proposition Clarity:** ✅ Clear demonstration of AI value
    - Real-time generation shows AI capability
    - Personalization evident in output
    - Professional presentation ready for investors

### **9.0 Performance Characteristics**

- **Generation Time:** 30-60 seconds for meal plans
- **API Timeout:** 60 seconds maximum wait
- **Model Performance:**
    - GPT-4o-mini: Fast, reliable, cost-effective (default)
    - GPT-4o: Balanced quality and speed
    - GPT-4-turbo: Highest quality, slower
    - GPT-3.5-turbo: Fastest, most economical
- **Error Recovery:** Always provides path back to preferences

### **10.0 Deployment & Distribution**

- **GitHub Repository:** github.com/genaifab/healthymealai
- **Documentation:** Comprehensive README with setup instructions
- **Configuration:** Environment variables for flexible deployment
- **Platforms Supported:** 
    - Local development with uv
    - Render (primary target)
    - Streamlit Cloud
    - Heroku
    - Any Python hosting platform

### **11.0 Version History**

- **v0.1-v0.4:** Foundation and LLM integration phases
- **v0.5:** Meal plan display implementation
- **v0.6:** Grocery list and refinements
- **v0.7.1:** Model selection enhancement
- **v1.0.0:** Production release with stable models
- **Current:** v1.0.0 with updated documentation

### **12.0 Future Product Roadmap**

**Potential Enhancements:**
1. User accounts with meal plan history
2. 5-day and 7-day meal plans
3. Individual meal regeneration
4. Grocery list export (PDF, shopping apps)
5. Nutritional analysis dashboard
6. Recipe rating and favorites
7. Meal prep instructions and timing
8. Integration with grocery delivery services
9. Mobile application
10. Multi-language support

**Technical Improvements:**
1. Implement Gemini API as alternative
2. Add recipe image generation
3. Implement caching for common requests
4. Add automated testing suite
5. Modularize codebase for team development