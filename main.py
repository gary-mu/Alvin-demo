from dotenv import load_dotenv 
import requests
import re
import os 
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6d400d27-daa8-4515-abb1-f651b3fb82dd"
FLOW_ID = "7d79c49f-06ed-432d-976f-a3180a996e8a" #LVN Prototype v1
ENDPOINT = "Math_7_10-2" # The endpoint name of the flow

#most likely do not need to update
APPLICATION_TOKEN = os.environ.get("APP_TOKEN") 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = None
    
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

#Helper functions
def click_ask_alvin_button():
    st.session_state.ask_alvn_clicked = True

def click_schedule_button():
    st.session_state.schedule_clicked = True
    st.session_state.show_schedule = True 


# Initialize session state variables
if 'clicked' not in st.session_state:
    st.session_state.clicked = False
if 'result' not in st.session_state:
    st.session_state.result = ''
if 'show_schedule' not in st.session_state:
    st.session_state.show_schedule = False
    
if 'scheduled' not in st.session_state:
    st.session_state.schedule_clicked = False  # Track if "Schedule 1:1" was clicked
    st.session_state.schedule_status = ''


#Start of the App
st.title("Alvn - Along + LVN AI Agent Demo")
st.subheader("Welcome to Alvn - An AI agent that that uses pedagogically aligned insights to support each learner’s journey.")
st.write("Ask your questions to get the best strategies to help your students")

message = st.text_area("Enter your questions here", placeholder = 'Ask your question to get the best strategies to help your students') 
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #574EFF;
        border: 1px solid white;
        color: white;
    }""",
):
    if st.button("Ask Alvn", type="primary", key = 'ask_alvn', on_click=click_ask_alvin_button):
        if not message.strip():
            st.error("Please enter a question")
            st.stop()
        try: 
            st.session_state.show_schedule = False # Reset "Schedule 1:1" button visibility
            with st.spinner("Thinking...feel free to grab a beverage while you wait"):
                response = run_flow(message)
            result = response['outputs'][0]['outputs'][0]['results']['message']['text']
            st.session_state.result = result

            pattern = r"(check*in|strategy|monitor)"  # Regex pattern for keywords
            if re.search(pattern, st.session_state.result, re.IGNORECASE):  # Case-insensitive search
                st.session_state.show_schedule = True  # Enable "Schedule 1:1" button
                    

        except Exception as e:
            st.error("An error occurred: " + str(e))



# Ensure the result persists after interactions
st.markdown(st.session_state.result)

# Persist the "Schedule 1:1" button even after clicking it
if st.session_state.show_schedule:
    st.markdown("**Recommended action:**")
    if st.button("Schedule 1:1", type='primary', on_click=click_schedule_button, key = 'schedule'):
        st.session_state.show_schedule = True  # Mark it as scheduled
        st.session_state.schedule_status = "You have scheduled a 1:1 session with the student, check your calendar app"
        st.success(st.session_state.schedule_status)

if st.session_state.schedule_clicked: 
    st.success(st.session_state.schedule_status)


if st.session_state.clicked:
    st.success(st.session_state.schedule_status)

footer_html = """<div style='text-align: center;'>
  <p>All student response data are synthtic data for demonstration purpose only.</p>
  <p>Evidence-based strategy sourced from Math 7-10 Model from <a href="https://lvp.digitalpromiseglobal.org/content-area/math-7-10">Digital Promise Website</a></p>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)

