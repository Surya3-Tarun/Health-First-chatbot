import streamlit as st
import google.generativeai as genai
import random
import os

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="HealthFirst AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS STYLING
# =========================
custom_css = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: #EEF8F4;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background-color: #EEF8F4;
}

[data-testid="stMainBlockContainer"] {
    background-color: #EEF8F4;
    padding-top: 0 !important;
}

[data-testid="stHeader"] {
    background-color: #EEF8F4;
}

/* Navigation Bar */
.navbar {
    background-color: #EEF8F4;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #E0EDE8;
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar-logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0F2230;
    letter-spacing: -0.5px;
}

.navbar-nav {
    display: flex;
    gap: 2rem;
    list-style: none;
}

.nav-item {
    color: #666;
    text-decoration: none;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    transition: all 0.3s ease;
}

.nav-item:hover {
    background-color: #DDF5EC;
    color: #0D8B78;
}

.nav-item.active {
    background-color: #DDF5EC;
    color: #0D8B78;
}

/* Hero Section */
.hero-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: center;
    padding: 4rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

.hero-left {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: #0F2230;
    line-height: 1.2;
    font-family: 'Georgia', 'Garamond', serif;
    letter-spacing: -1px;
}

.hero-title-teal {
    color: #0D8B78;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #666;
    line-height: 1.6;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
}

.btn-primary {
    background-color: #0D8B78;
    color: white;
}

.btn-primary:hover {
    background-color: #0A6F63;
    transform: translateY(-2px);
}

.btn-secondary {
    background-color: white;
    color: #0D8B78;
    border: 2px solid #0D8B78;
}

.btn-secondary:hover {
    background-color: #F0F0F0;
    transform: translateY(-2px);
}

.hero-disclaimer {
    font-size: 0.9rem;
    color: #999;
    margin-top: 0.5rem;
}

.hero-right {
    display: flex;
    justify-content: center;
}

.preview-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(13, 139, 120, 0.08);
    max-width: 400px;
    width: 100%;
}

.preview-header {
    font-size: 1rem;
    font-weight: 600;
    color: #0D8B78;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.preview-message {
    background-color: #0D8B78;
    color: white;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    font-size: 0.95rem;
    line-height: 1.5;
    align-self: flex-end;
    max-width: 80%;
}

.preview-response {
    background-color: #DDF5EC;
    padding: 1rem;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #333;
}

.response-section {
    margin-bottom: 1rem;
}

.response-section-title {
    font-weight: 600;
    color: #0D8B78;
    margin-bottom: 0.3rem;
}

.response-section-items {
    margin-left: 0.5rem;
    font-size: 0.9rem;
    color: #666;
}

/* Feature Cards */
.feature-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    padding: 4rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

.feature-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(13, 139, 120, 0.05);
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(13, 139, 120, 0.1);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.feature-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0F2230;
    margin-bottom: 0.5rem;
}

.feature-desc {
    color: #666;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.feature-link {
    color: #0D8B78;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
}

/* Emergency Banner */
.emergency-banner {
    background-color: #E8F5F0;
    border-left: 4px solid #0D8B78;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    color: #0D8B78;
    font-size: 0.95rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Chat Page */
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

.chat-messages {
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.message {
    padding: 1rem 1.5rem;
    border-radius: 12px;
    line-height: 1.6;
}

.message-user {
    background-color: #0D8B78;
    color: white;
    align-self: flex-end;
    max-width: 70%;
}

.message-assistant {
    background-color: #DDF5EC;
    color: #333;
    align-self: flex-start;
    max-width: 100%;
}

/* Suggestion Cards */
.suggestions-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.suggestion-card {
    background: white;
    border: 2px solid #E0EDE8;
    border-radius: 12px;
    padding: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.95rem;
    color: #333;
    text-align: center;
}

.suggestion-card:hover {
    border-color: #0D8B78;
    background-color: #F5FDFB;
    transform: translateY(-2px);
}

/* Chat Input */
.chat-input-container {
    display: flex;
    gap: 0.75rem;
    margin-top: 2rem;
}

.chat-input-box {
    flex: 1;
    padding: 1rem 1.5rem;
    border: 2px solid #DDF5EC;
    border-radius: 20px;
    font-size: 0.95rem;
    font-family: inherit;
    transition: all 0.3s ease;
}

.chat-input-box:focus {
    outline: none;
    border-color: #0D8B78;
    box-shadow: 0 0 0 3px rgba(13, 139, 120, 0.1);
}

.chat-send-btn {
    background-color: #0D8B78;
    color: white;
    border: none;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    cursor: pointer;
    font-size: 1.2rem;
    transition: all 0.3s ease;
}

.chat-send-btn:hover {
    background-color: #0A6F63;
    transform: scale(1.05);
}

/* BMI Calculator */
.bmi-section {
    max-width: 900px;
    margin: 3rem auto;
    padding: 0 2rem;
}

.bmi-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #0F2230;
    text-align: center;
    margin-bottom: 1rem;
}

.bmi-description {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
    font-size: 1rem;
}

.bmi-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 2px 12px rgba(13, 139, 120, 0.05);
}

.bmi-inputs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
}

.bmi-input-group {
    display: flex;
    flex-direction: column;
}

.bmi-input-label {
    font-weight: 600;
    color: #0F2230;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.bmi-input {
    padding: 0.75rem 1rem;
    border: 2px solid #E0EDE8;
    border-radius: 8px;
    font-size: 1rem;
    font-family: inherit;
    transition: all 0.3s ease;
}

.bmi-input:focus {
    outline: none;
    border-color: #0D8B78;
    box-shadow: 0 0 0 3px rgba(13, 139, 120, 0.1);
}

.bmi-helper {
    color: #999;
    font-size: 0.85rem;
    margin-top: 1rem;
    text-align: center;
}

.bmi-categories {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-top: 2rem;
}

.bmi-category {
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    background-color: #F5F5F5;
}

.bmi-category-range {
    font-weight: 700;
    color: #0D8B78;
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
}

.bmi-category-name {
    color: #333;
    font-weight: 600;
    font-size: 0.95rem;
}

/* Tips Page */
.tips-section {
    max-width: 1200px;
    margin: 3rem auto;
    padding: 0 2rem;
}

.tips-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #0F2230;
    text-align: center;
    margin-bottom: 0.5rem;
}

.tips-subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
    font-size: 1rem;
}

.featured-tip {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 2px 12px rgba(13, 139, 120, 0.05);
    margin-bottom: 3rem;
}

.featured-tip-label {
    color: #0D8B78;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}

.featured-tip-title {
    font-size: 2rem;
    font-weight: 700;
    color: #0F2230;
    margin-bottom: 1rem;
}

.featured-tip-desc {
    color: #666;
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.new-tip-btn {
    background-color: #0D8B78;
    color: white;
    padding: 0.7rem 1.5rem;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.new-tip-btn:hover {
    background-color: #0A6F63;
}

.tips-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
}

.tip-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(13, 139, 120, 0.05);
}

.tip-card-title {
    font-weight: 700;
    color: #0F2230;
    margin-bottom: 0.5rem;
    font-size: 1rem;
}

.tip-card-desc {
    color: #666;
    font-size: 0.9rem;
    line-height: 1.5;
}

.tip-card-highlighted {
    background-color: #DDF5EC;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-container {
        grid-template-columns: 1fr;
        padding: 2rem 1rem;
    }
    
    .feature-cards {
        grid-template-columns: 1fr;
    }
    
    .bmi-inputs {
        grid-template-columns: 1fr;
    }
    
    .tips-grid {
        grid-template-columns: 1fr;
    }
    
    .navbar-nav {
        gap: 1rem;
    }
    
    .suggestions-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# =========================
# NAVIGATION STATE
# =========================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Landing"

# =========================
# NAVIGATION BAR
# =========================
col_logo, col_nav = st.columns([1, 4])

with col_logo:
    st.markdown('<div class="navbar-logo">🩺 HealthFirst</div>', unsafe_allow_html=True)

with col_nav:
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        if st.button("Assistant", key="nav_assistant", use_container_width=True):
            st.session_state.current_page = "Assistant"
    
    with nav_col2:
        if st.button("BMI", key="nav_bmi", use_container_width=True):
            st.session_state.current_page = "BMI"
    
    with nav_col3:
        if st.button("Tips", key="nav_tips", use_container_width=True):
            st.session_state.current_page = "Tips"

st.divider()

# =========================
# CURRENT PAGE ROUTING
# =========================
current_page = st.session_state.current_page

# =========================
# BMI CALCULATOR PAGE
# =========================
if current_page == "BMI":
    st.markdown('<div class="bmi-section">', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">⚖️</div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="bmi-title">BMI Calculator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="bmi-description">A quick body-mass-index estimate. BMI is a general guide — it doesn\'t tell the whole story of health.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="bmi-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0, key="weight_input")
    
    with col2:
        height = st.number_input("Height (meters)", min_value=0.5, value=1.75, key="height_input")
    
    st.markdown('<p class="bmi-helper">Enter your weight and height to see your BMI.</p>', unsafe_allow_html=True)
    
    # Auto-calculate BMI
    if weight > 0 and height > 0:
        bmi = weight / (height ** 2)
        
        st.markdown('<div class="bmi-categories">', unsafe_allow_html=True)
        
        st.markdown('<div class="bmi-category"><div class="bmi-category-range">< 18.5</div><div class="bmi-category-name">Underweight</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="bmi-category"><div class="bmi-category-range">18.5 - 24.9</div><div class="bmi-category-name">Normal</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="bmi-category"><div class="bmi-category-range">25 - 29.0</div><div class="bmi-category-name">Overweight</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="bmi-category"><div class="bmi-category-range">≥ 30</div><div class="bmi-category-name">Obese</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HEALTH TIPS PAGE
# =========================
elif current_page == "Tips":
    st.markdown('<div class="tips-section">', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center;"><div style="font-size: 2rem; margin-bottom: 0.5rem;">💡</div></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="tips-title">Daily Health Tips</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tips-subtitle">One small habit at a time. Tap refresh for a new one.</p>', unsafe_allow_html=True)
    
    tips = [
        ("Less sugar", "Cut sugary drinks first; they're the easiest big win for most people."),
        ("Hydrate", "Drink 2-3 liters of water across the day. Add a glass with each meal."),
        ("Move 30", "Walk briskly for at least 30 minutes — split into shorter bursts if needed."),
        ("Sleep 7-8h", "Keep a consistent bedtime. Dim screens 30 minutes before sleep."),
        ("Eat the rainbow", "Include colorful vegetables and fruits in your daily meals."),
        ("Screen breaks", "Take a 5-minute break from screens every 30 minutes."),
    ]
    
    # Featured tip
    featured = random.choice(tips)
    st.markdown('<div class="featured-tip">', unsafe_allow_html=True)
    st.markdown(f'<div class="featured-tip-label">TODAY\'S TIP</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="featured-tip-title">{featured[0]}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="featured-tip-desc">{featured[1]}</p>', unsafe_allow_html=True)
    
    if st.button("New tip", key="new_tip_btn"):
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Other tips grid
    st.markdown('<div class="tips-grid">', unsafe_allow_html=True)
    for tip_title, tip_desc in tips:
        if tip_title != featured[0]:
            if tip_title == "Less sugar":
                st.markdown(f'<div class="tip-card tip-card-highlighted"><div class="tip-card-title">{tip_title}</div><div class="tip-card-desc">{tip_desc}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="tip-card"><div class="tip-card-title">{tip_title}</div><div class="tip-card-desc">{tip_desc}</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AI HEALTH ASSISTANT PAGE
# =========================
elif current_page == "Assistant":
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="emergency-banner">ℹ️ General information only. For emergencies (chest pain, trouble breathing, severe bleeding, stroke signs) call your local emergency number immediately.</div>', unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message message-user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message message-assistant">{message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Suggestion cards
    if len(st.session_state.messages) == 0:
        st.markdown('<div class="suggestions-grid">', unsafe_allow_html=True)
        suggestions = [
            "I have a sore throat and mild fever",
            "What should I do for a minor burn?",
            "I've had a headache all day — how can I relieve it?",
            "When is a cough serious enough to see a doctor?"
        ]
        for suggestion in suggestions:
            st.markdown(f'<div class="suggestion-card">{suggestion}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Describe your symptoms...", key="chat_input")
    
    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Emergency check
        emergency_keywords = [
            "chest pain", "difficulty breathing", "heart attack",
            "stroke", "unconscious", "severe bleeding"
        ]
        
        is_emergency = any(
            word in user_input.lower()
            for word in emergency_keywords
        )
        
        if is_emergency:
            response = "🚨 EMERGENCY ALERT\n\nYour symptoms may indicate a serious condition.\n\nPlease seek immediate medical attention or call emergency services."
        else:
            # Gemini-based healthcare classification
            classification_prompt = f"""
Classify if the following query is healthcare-related or not.

Query: {user_input}

Respond with ONLY 'YES' if it's healthcare-related, or 'NO' if it's not.
Do not provide any explanation.
"""
            
            try:
                classification_result = model.generate_content(classification_prompt)
                classification_response = classification_result.text.strip().upper()
            except Exception as e:
                classification_response = "YES"
            
            if classification_response != "YES":
                response = "❌ Sorry, I can only answer healthcare-related questions.\n\nExamples:\n• I have fever and cough\n• What are the symptoms of diabetes?\n• How to reduce headache?\n• What should I do for stomach pain?"
            else:
                prompt = f"""
You are HealthFirst AI, a healthcare information assistant.

Rules:
1. Answer ONLY healthcare-related questions.
2. Do not answer coding, sports, movies, politics, history, entertainment or general knowledge questions.
3. Provide:
   - Possible causes
   - Home remedies
   - First aid tips
   - When to consult a doctor
4. Do not provide a medical diagnosis.

User Question:
{user_input}
"""
                
                try:
                    result = model.generate_content(prompt)
                    response = result.text
                except Exception as e:
                    response = f"Error: {e}"
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# LANDING PAGE (Default)
# =========================
else:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    
    # Left side
    st.markdown('<div class="hero-left">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Health questions,<br><span class="hero-title-teal">answered with care.</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Describe a symptom and HealthFirst will walk you through likely causes, home remedies, first-aid steps, and clear signs of when to see a doctor.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Start a conversation →", key="start_conv", use_container_width=True):
            st.session_state.current_page = "Assistant"
            st.rerun()
    
    with col2:
        if st.button("Today's tip", key="today_tip", use_container_width=True):
            st.session_state.current_page = "Tips"
            st.rerun()
    
    st.markdown('<p class="hero-disclaimer">ℹ️ General information only — not a substitute for professional medical advice.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right side - Preview card
    st.markdown('<div class="hero-right">', unsafe_allow_html=True)
    st.markdown('<div class="preview-card">', unsafe_allow_html=True)
    st.markdown('<div class="preview-header">🤖 HealthFirst Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="preview-message">I\'ve had a sore throat and mild fever since yesterday.</div>', unsafe_allow_html=True)
    st.markdown('<div class="preview-response">', unsafe_allow_html=True)
    st.markdown('<div class="response-section"><div class="response-section-title">Likely cause</div><div class="response-section-items">Often a viral upper-respiratory infection. Usually settles in a few days.</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="response-section"><div class="response-section-title">Try at home</div><div class="response-section-items">• Warm fluids, salt-water gargle<br>• Rest and paracetamol for fever</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="response-section"><div class="response-section-title" style="color: #E74C3C;">See a doctor if</div><div class="response-section-items">Fever > 39°C, trouble breathing, or symptoms last beyond 5 days.</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature cards
    st.markdown('<div class="feature-cards">', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">🤖</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="feature-title">AI Health Assistant</h3>', unsafe_allow_html=True)
    st.markdown('<p class="feature-desc">Share your symptoms. Get likely causes, home care, first-aid steps, and red flags.</p>', unsafe_allow_html=True)
    if st.button("Open assistant →", key="open_assistant", use_container_width=True):
        st.session_state.current_page = "Assistant"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">⚖️</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="feature-title">BMI Calculator</h3>', unsafe_allow_html=True)
    st.markdown('<p class="feature-desc">Quick body-mass-index check with friendly guidance on what the result means.</p>', unsafe_allow_html=True)
    if st.button("Calculate BMI →", key="calc_bmi", use_container_width=True):
        st.session_state.current_page = "BMI"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">💡</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="feature-title">Daily Health Tips</h3>', unsafe_allow_html=True)
    st.markdown('<p class="feature-desc">A small, doable habit every day — from hydration to sleep and movement.</p>', unsafe_allow_html=True)
    if st.button("See today's tip →", key="see_tips", use_container_width=True):
        st.session_state.current_page = "Tips"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)