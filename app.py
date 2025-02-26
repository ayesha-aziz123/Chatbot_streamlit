
import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

st.markdown("""
    <style>
        .title {
            text-align: center;
            color: green;
            font-size: 2.5em;
            font-weight: bold;
        }
        @media (max-width: 768px) {
            .title {
                font-size: 2em;  /* Small screens par size thoda chhota */
            }
        }
        @media (max-width: 480px) {
            .title {
                font-size: 1.7em;  /* Mobile screens ke liye aur chhota */
                text-align:center
            }
        }
    </style>
    <h1 class="title">🤖 Gemini Pro - AI ChatBot</h1>
""", unsafe_allow_html=True)



GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.0-flash')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])



# st.markdown('<h1 style="color: green; text-align: center; ">🤖 Gemini Pro - AI ChatBot</h1>', unsafe_allow_html=True)


# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
