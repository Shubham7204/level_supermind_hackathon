import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Social Media AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;  /* Increase max width for larger screens */
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .stButton button {
        border-radius: 20px;
        padding: 0.5rem 2rem;
        background-color: #1E88E5;
        color: white;
        border: none;
        width: 100%;
    }
    .response-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        border: 1px solid #ddd;
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
    }
    @media (min-width: 1024px) {
        .stTextArea textarea {
            font-size: 1.1rem;
        }
        .stButton button {
            font-size: 1.2rem;
        }
        .container {
            flex-direction: row;
            justify-content: space-between;
        }
        .stTextArea {
            width: 60%;
        }
        .stButton {
            width: 35%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Fetch values from the environment
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APP_TOKEN")
ENDPOINT = "socialmedia"

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)

    response_data = response.json()

    if 'outputs' in response_data and len(response_data['outputs']) > 0:
        output_message = response_data["outputs"][0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "No text in the response")
    else:
        output_message = "No valid outputs received"

    return output_message

def main():
    # Header with icon
    st.markdown('<h1 class="main-header">🤖 Social Media AI Assistant</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Welcome to the Social Media AI Assistant! Ask me anything about social media marketing, 
    strategy, content creation, or analytics.
    """)
    
    # Create a responsive container
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Create two columns for a better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        message = st.text_area(
            "Your Question",
            placeholder="E.g., 'Which post should I do more images or reels? Support with some statistics.'",
            height=100
        )
    
    with col2:
        st.write(" ")
        st.write(" ")
        submit_button = st.button("Ask AI 🚀", use_container_width=True)
    
    # Close the container
    st.markdown('</div>', unsafe_allow_html=True)

    # History management
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if submit_button and message.strip():
        try:
            with st.spinner("🤔 Thinking..."):
                response_message = run_flow(message)
            
            # Add to history
            st.session_state.chat_history.append({
                "question": message,
                "answer": response_message
            })
            
            # Clear input
            message = ""

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### Conversation History")
        for chat in reversed(st.session_state.chat_history):
            with st.container():
                st.markdown("**You asked:**")
                st.markdown(f">{chat['question']}")
                st.markdown("**AI Response:**")
                with st.markdown('<div class="response-container">', unsafe_allow_html=True):
                    st.markdown(chat['answer'])
                st.markdown("---")

    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        Powered by Langflow API • Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
