import os
import pathlib
import json
from datetime import datetime
import streamlit as st
import google.generativeai as genai

# --- 1. SECURE AUTOMATIC PASTEL THEME CONFIGURATION ---
# Injects custom light/dark pastel palettes natively into Streamlit's config
config_dir = pathlib.Path(".streamlit")
config_dir.mkdir(exist_ok=True)
config_file = config_dir / "config.toml"

theme_content = """
[theme]
base = "auto"
primaryColor = "#D6BBFB"

[theme.light]
backgroundColor = "#FFF0F5"
secondaryBackgroundColor = "#E8EAFF"
textColor = "#2D3748"

[theme.dark]
backgroundColor = "#1A1A24"
secondaryBackgroundColor = "#25263A"
textColor = "#EDF2F7"
"""
config_file.write_text(theme_content)


# --- 2. GLOBAL PAGE ARCHITECTURE & CUTE CUSTOM CSS ---
st.set_page_config(
    page_title="ney // Ultra AI Assistant",
    page_icon="🌸",
    layout="wide"
)

# Cute UI enhancements using custom injected CSS
st.markdown("""
    <style>
    /* Soften metrics cards */
    .stMetric {
        background: linear-gradient(135deg, rgba(214, 187, 251, 0.2), rgba(255, 240, 245, 0.2));
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(214, 187, 251, 0.4);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    /* Style headers beautifully */
    h1 {
        background: linear-gradient(45deg, #B3C5FF, #D6BBFB, #FFC5E3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    /* Round corners on chat inputs */
    .stChatInputContainer {
        border-radius: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- 3. FAILSAFE SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.markdown("### 🌸 ney Settings Center")
    st.caption("Fine-tune configurations for optimal performance.")
    st.write("---")
    
    # AI Performance Adjustments
    ai_creativity = st.slider(
        "Creativity Profile (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        step=0.05,
        help="Lower values yield highly accurate response formatting; higher values increase wit."
    )
    
    # ANTI-GLITCH SAFETY TOGGLE: Allows switching models instantly if an API endpoint acts up
    model_tier = st.selectbox(
        "AI Engine Core",
        options=["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        help="Flash is incredibly fast; Pro handles deeply complex logical sequences."
    )
    
    st.write("---")
    st.markdown("#### ⚙️ Security Guard")
    
    # Secure API Extraction Check
    api_source = os.environ.get("GEMINI_API_KEY", "")
    if api_source:
        st.success("✨ System Authenticated via Environment")
    else:
        user_key = st.text_input("🔑 Provide Gemini Key:", type="password", placeholder="AI key...")
        if user_key:
            genai.configure(api_key=user_key)
            st.success("✨ System Authenticated Manually")
        else:
            st.warning("Awaiting secure key inputs to boot up AI pipelines.")


# --- 4. OPTIMIZED ZERO-GLITCH MODEL ENGINE ---
@st.cache_resource
def get_failsafe_model(temperature, chosen_model):
    system_instruction = (
        "Your name is ney. You are an exceptionally brilliant, professional, cute, "
        "and encouraging AI companion. You help users solve engineering problems, analyze "
        "data, and map out concepts. Keep responses exquisitely organized using markdown tables, "
        "bullet points, or bold structural accents. Always greet the user warmly as ney."
    )
    
    generation_config = {
        "temperature": temperature,
        "top_p": 0.90,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    return genai.GenerativeModel(
        model_name=chosen_model,
        generation_config=generation_config,
        system_instruction=system_instruction
    )

if api_source:
    genai.configure(api_key=api_source)

# Failsafe fallback execution block
try:
    model = get_failsafe_model(ai_creativity, model_tier)
except Exception as fallback_error:
    # If chosen core fails, default to secondary stable branch automatically
    try:
        model = get_failsafe_model(0.5, "gemini-1.5-flash")
    except Exception as severe_err:
        st.error(f"Critical System Initialization Halt: {severe_err}")


# --- 5. DATA PERSISTENCE & MEMORY PIPELINES ---
if "chat_session" not in st.session_state and 'model' in locals():
    st.session_state.chat_session = model.start_chat(history=[])
if "message_count" not in st.session_state:
    st.session_state.message_count = 0


# --- 6. USER INTERFACE HEADER DESIGN ---
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("<h1>🌸 meet ney</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic; opacity: 0.85;'>An advanced, pastel-optimized conversational platform</p>", unsafe_allow_html=True)

with col2:
    st.metric(label="Data Exchanges Secured", value=st.session_state.message_count)

st.write("---")


# --- 7. LIVE CONVERSATION RENDERING ---
# Render historical context maps safely from Streamlit memory stores
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        avatar = "🧑‍💻" if role == "user" else "🌸"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message.parts[0].text)

# Dynamic text entry frame
if user_query := st.chat_input("Message ney..."):
    if not api_source and 'user_key' in locals() and not user_key:
        st.error("Authentication Token Missing. Input valid operational API parameters in the sidebar settings panel.")
    else:
        # Prompt instantly reflected into the visual state
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_query)
        st.session_state.message_count += 1
            
        # Neural response generation thread
        with st.chat_message("assistant", avatar="🌸"):
            with st.spinner("ney is analyzing structural data..."):
                try:
                    response = st.session_state.chat_session.send_message(user_query)
                    st.markdown(response.text)
                    st.session_state.message_count += 1
                    st.rerun()
                except Exception as connection_error:
                    # Clear diagnostic handling so the interface never locks up or goes blank
                    st.error(f"Failsafe triggered. Message synchronization dropped: {connection_error}")


# --- 8. PROFESSIONAL EXTRA CREDIT DATA EXPORTER ---
st.write("---")
if "chat_session" in st.session_state and len(st.session_state.chat_session.history) > 0:
    export_text = f"# Operational Session Log with ney — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    for msg in st.session_state.chat_session.history:
        speaker = "User" if msg.role == "user" else "ney"
        export_text += f"### **{speaker}:**\n{msg.parts[0].text}\n\n---\n\n"
        
    st.download_button(
        label="📥 Download Data History Logs (.md)",
        data=export_text,
        file_name=f"ney_session_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
  )
  
