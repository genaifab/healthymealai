
# HealthyMeals AI Design Guidelines Document

**Version:** 1.0 **Date:** August 12, 2025 **Author:** [Your Name/Startup Name] 

### **1.0 Introduction**

- **1.1 Purpose:** To provide UI/UX principles, visual direction, and accessibility standards for the prototype. This guide will ensure a consistent, professional, and user-friendly experience.
    
- **1.2 Design Philosophy: "Healthy, Calm, and Clear"**
    
    - The design should feel organized, stress-free, and focused on well-being. Every design choice should contribute to a sense of clarity and ease for the busy professional.
        

### **2.0 Core UI/UX Principles**

- **2.1 Clarity Over Clutter:** The interface must be minimalist. If an element doesn't serve a clear purpose, it should be removed.
    
- **2.2 Effortless Navigation:** The user's journey should feel like a single, guided conversation. They should never feel lost or unsure of what to do next.
    
- **2.3 Control in the Sidebar, Content in the Main Area:** User inputs and controls will be housed in the sidebar, keeping the main page dedicated to displaying the meal plan and grocery list.
    

### **3.0 User Flow & Interaction Patterns (for Streamlit)**

This section defines how the UI/UX principles will be implemented using standard Streamlit components in a sidebar layout.

- **3.1 Layout: Sidebar for Controls**
    
    - The primary user interaction will happen in the `st.sidebar`. This is where the user will set all their preferences. The main column will be used exclusively for displaying the output.
        
- **3.2 Sidebar Text Wireframe:**
    
    ```
    +-----------------------------------------+
    | [LOGO/APP NAME]                         |
    | Nourish AI                              |
    |                                         |
    | ---                                     |
    |                                         |
    | Tell us about your needs:               |
    |                                         |
    | DIETARY PREFERENCES                     |
    | [ ] Vegetarian  [ ] Vegan               |
    | [ ] Gluten-Free [ ] Dairy-Free          |
    | [ ] Low-Glycemic                        |
    |                                         |
    | FOODS TO EXCLUDE                        |
    | [ e.g., mushrooms, cilantro      ]       |
    |                                         |
    | AVG. COOKING TIME                       |
    | <---o----------------> 45 min           |
    |                                         |
    | MEALS PER DAY                           |
    | (o) Breakfast, Lunch, Dinner            |
    | ( ) Lunch, Dinner                       |
    |                                         |
    | ---                                     |
    |                                         |
    | [    GENERATE MY WEEKLY PLAN    ]       |
    |                                         |
    +-----------------------------------------+
    ```
    
- **3.3 Main Content Area:**
    
    - **Initial State:** When the app first loads, the main area will display a welcome message and a call to action, pointing the user to the sidebar.
        
    - **Plan Display:** After generation, the main area will be populated with the 7-day meal plan, using `st.columns` and `st.expander` for a clean, interactive grid.
        
    - **Grocery List:** The grocery list will replace the meal plan in the main view when requested.
        

### **4.0 Visual Direction**

- **4.1 Color Palette:** Fresh, natural, and trustworthy.
    
    - **Primary (Brand Green):** `#2E8B57` (SeaGreen) - Used for headers, spinners, and primary accents.
        
    - **Accent (Action Orange):** `#FFA500` (Orange) - Used for the primary "Generate" button.
        
    - **Neutral Text:** `#333333` (Dark Gray) - For all body copy.
        
    - **Subtle Gray (Containers/Expanders):** `#F5F5F5` (WhiteSmoke) - For expander backgrounds to create separation.
        
- **4.2 Typography:** Clean, modern, and highly readable.
    
    - **Font Family:** **Poppins** (A clean, geometric sans-serif).
        
    - **Hierarchy:**
        
        - `st.title`: "Nourish AI"
            
        - `st.header`: "Your Weekly Meal Plan"
            
        - `st.subheader`: Sidebar sections and grocery list categories.
            
        - `st.write`/`st.markdown`: All body text.
            
- **4.3 Iconography:**
    
    - **Style:** Simple and universally understood. Use Streamlit's built-in support for emojis.
        
    - **Examples:** 🥗 for meals, 🥑 for ingredients, 🛒 for grocery list, 🗓️ for the plan.
        

### **5.0 Accessibility (A11y) Requirements**

- **5.1 Color Contrast:** The selected color palette must be checked for WCAG AA compliance.
    
- **5.2 Descriptive Labels:** All interactive widgets must have clear, explicit labels.
    
- **5.3 Readability:** The chosen font size and family support high readability.
    
- **5.4 Keyboard Navigation:** Standard Streamlit components are generally keyboard accessible. The entire flow should be navigable using only the Tab and Enter keys.