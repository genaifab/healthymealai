### HealthyMeals AI Product Requirements Document

**Version:** 1.0 **Date:** August 12, 2025 **Author:** [Your Name/Startup Name]  

### **1.0 Introduction**

- **1.1 Vision:** To make healthy eating effortless for busy professionals by leveraging a powerful generative AI model to create personalized meal plans using whole, non-processed foods.
    
- **1.2 Project Goal:** To develop a simple, interactive prototype that demonstrates the core user journey and the dynamic capabilities of using a live Large Language Model (LLM). This prototype will be used to showcase the key features to potential investors and early-adopter customers.
    
- **1.3 Document Purpose:** To provide the developer with a clear set of requirements, features, user flows, and constraints necessary to build the working prototype using Streamlit and a live LLM API.
    

### **2.0 The Problem & Target User**

- **2.1 Problem Statement:** Busy professionals with diverse dietary needs want to improve their health by eating whole, unprocessed foods, but lack the time and expertise for consistent meal planning. This leads them to rely on unhealthy, processed convenience foods, which negatively impacts their well-being.
    
- **2.2 Target User Personas:**
    
    - **2.2.1 The Time-Crunched Achiever (Baseline)**
        
        - **Name:** Sarah Jenkins
            
        - **Age:** 32
            
        - **Profession:** Senior Marketing Manager
            
        - **Goals:** Improve energy and focus, reduce reliance on takeout and processed snacks, spend less mental energy on "what's for dinner?"
            
        - **Frustrations:** Works 50+ hours a week, finds meal planning overwhelming and most recipes too complex for a weekday.
            
    - **2.2.2 The Health-Conscious Professional (Pre-Diabetic)**
        
        - **Name:** Maria Rodriguez
            
        - **Age:** 45
            
        - **Profession:** Lawyer
            
        - **Goals:** Manage blood sugar by eating low-glycemic index foods, strictly avoid added sugars and refined carbohydrates.
            
        - **Frustrations:** Confused by conflicting dietary advice online; needs simple, reliable meal options that fit her specific medical needs without requiring constant research.
            
    - **2.2.3 The Ethical Eater (Vegetarian)**
        
        - **Name:** Ben Carter
            
        - **Age:** 28
            
        - **Profession:** Software Developer
            
        - **Goals:** Ensure he gets complete proteins, discover new and interesting vegetarian recipes, and avoid falling back on monotonous meals like pasta or simple salads.
            
        - **Frustrations:** Struggles to find variety in quick, high-protein vegetarian meals; worries about potential nutritional gaps in his diet.
            
    - **2.2.4 The Sensitive Gut (Gluten-Free)**
        
        - **Name:** Alex Chen
            
        - **Age:** 37
            
        - **Profession:** Architect
            
        - **Goals:** Strictly avoid all sources of gluten to manage digestive health, find satisfying and flavorful alternatives to common wheat-based foods, and ensure his meals are exciting.
            
        - **Frustrations:** The constant vigilance required to check for hidden gluten, the high cost and often poor taste of packaged gluten-free products, and the risk of cross-contamination.
            

### **3.0 Prototype Goals & Objectives**

- **Primary Objective:** Clearly demonstrate the core user journey: setting preferences, generating a personalized meal plan _directly from an LLM_, viewing a recipe, and creating a grocery list.
    
- **Secondary Objectives:**
    
    - Showcase the power of real-time AI personalization by generating a unique plan that directly reflects user-inputted preferences.
        
    - Illustrate the app's focus on whole, non-processed foods in the generated meals.
        
    - Provide a clean, intuitive, and visually appealing user interface concept.
        

### **4.0 Core Features & Functionality (The "What")**

This prototype will consist of four main features, representing a single, linear user flow powered by an LLM.

- **4.1 Feature 1: Simplified User Onboarding & Preferences**
    
    - A simple form to capture essential user data that will be used to construct the LLM prompt.
        
    - **Inputs:**
        
        - Common dietary restrictions (Checkboxes: Vegetarian, Vegan, Gluten-Free, Dairy-Free, Low-Glycemic).
            
        - Key foods to exclude (Simple text input field, e.g., "mushrooms, cilantro").
            
        - Preferred average cooking time (Slider or buttons: e.g., "<15 min", "<30 min", "<45 min").
            
        - Number of meals per day to plan for (e.g., Breakfast, Lunch, Dinner).
            
- **4.2 Feature 2: Live AI Meal Plan Generation**
    
    - A main dashboard screen with a prominent button: **"Generate My Weekly Plan"**.
        
    - Upon clicking, the system constructs a detailed prompt from the user's preferences and sends it to the LLM API.
        
    - The app will wait for the response and then display a 7-day meal plan (Monday - Sunday) based on the LLM's output.
        
    - The view will be a simple grid or list showing the meal names for each day.
        
- **4.3 Feature 3: Dynamic Recipe View**
    
    - Users can click on any meal name in the plan.
        
    - This action opens a simple view (e.g., a Streamlit expander) displaying the recipe details as provided by the LLM:
        
        - **Meal Name:** e.g., "Lemon Herb Baked Salmon with Roasted Asparagus"
            
        - **Ingredients List:** A bulleted list of whole-food ingredients.
            
        - **Simple Instructions:** A numbered list of simple steps for preparation.
            
- **4.4 Feature 4: Consolidated Grocery List**
    
    - On the main meal plan view, there will be a button: **"Create Grocery List for the Week"**.
        
    - Clicking this button will navigate to a new screen that displays all ingredients from the entire week's meal plan, as parsed from the LLM response.
        
    - The list must be:
        
        - **Consolidated:** Total quantities for repeated ingredients are calculated.
            
        - **Categorized:** Grouped by simple, intuitive categories (e.g., Produce, Proteins, Pantry/Dry Goods).
            

### **5.0 User Flow & Wireframe Sketch**

- **User Flow:**
    
    1. User opens the app and is presented with the **Onboarding Form** (Feature 4.1).
        
    2. User completes the preferences and clicks "Generate My Weekly Plan".
        
    3. A **loading spinner** appears while the app calls the LLM API.
        
    4. The **Weekly Meal Plan** (Feature 4.2), generated by the LLM, is displayed.
        
    5. User clicks on a meal name to expand the **Dynamic Recipe View** (Feature 4.3).
        
    6. User closes the recipe and returns to the plan, then clicks "Create Grocery List for the Week".
        
    7. The **Categorized Grocery List** (Feature 4.4) is displayed.
        

### **6.0 Non-Functional & Technical Requirements**

- **6.1 UI/UX:** The interface should be clean, minimal, and modern, following the Design Guidelines.
    
- **6.2 LLM Integration:**
    
    - The application will integrate with a third-party LLM API (e.g., Gemini or OpenAI).
        
    - **Critical Requirement:** The prompt sent to the LLM must explicitly request the output in a structured **JSON format**. This is essential for reliably parsing the meal plan, recipes, and ingredients.
        
    - The application must handle the API call asynchronously, showing a loading indicator to the user.
        
- **6.3 Platform:** A web-based application built with **Streamlit**.
    
- **6.4 Package Management:** Development will use **`uv`** for creating the virtual environment and managing packages.
    

### **7.0 What's Out of Scope for this Prototype**

- User accounts, login, or saving data between sessions.
    
- Training or fine-tuning a proprietary AI model.
    
- Allowing the user to "re-roll" or swap individual meals.
    
- Calorie, macro, or detailed nutritional information (unless the LLM provides it easily).
    
- A backend database. All data is transient and exists only for the current session.
    

### **8.0 Success Metrics for the Prototype**

- **Completion of User Flow:** A user can successfully navigate the entire flow described in Section 5.0 without errors.
    
- **Demonstrates Personalization:** The LLM-generated meal plan is high-quality and clearly reflects the preferences selected during onboarding.
    
- **Reliable Parsing:** The application consistently and accurately parses the JSON response from the LLM to display the plan and grocery list.
    
- **Clarity of Value Proposition:** A potential investor or customer viewing the prototype can clearly understand the unique value of using a live AI to generate meal plans.