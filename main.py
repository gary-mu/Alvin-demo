from dotenv import load_dotenv 
import hmac
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

#Font title CSS
def set_dual_font_title():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Graphik&family=Playfair+Display&display=swap'); /* Import Graphik and Playfair Display */

        .custom-title {
            font-size: 40px;
        }
        .font-part1 {
            font-family: 'Graphik', sans-serif; 
        }
        .font-part2 {
            font-family: 'Playfair Display', serif;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)

set_dual_font_title()


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

#Checking password
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


#Start of the App
col1, col2 = st.columns([1, 2])
with col1:
    st.image("images/alvn_logo.jpeg")
with col2:
    st.markdown(
        '<h1 class="custom-title">'
        '<span class="font-part1">Ask </span>'  # First part of the title with first font
        '<span class="font-part2">Alvn : </span>'    # Second part of the title with second font
        '<br><span>Along + LVN AI Agent Demo</span>'    # Second part of the title with second font
        '</h1>',
        unsafe_allow_html=True
    )
    #st.markdown("Get the most relevant data from EduGraph’s knowledge graph ensuring you have high quality context data to pass to an LLM for your edtech application.")
    # st.title("Alvn - Along + LVN AI Agent Demo")
st.subheader("Welcome to Alvn - An AI agent that that uses pedagogically aligned insights to support each learner’s journey.")

message = st.text_area("Ask your questions to get the best strategies to help your students:", placeholder = 'Ask your question to get the best strategies to help your students') 
with stylable_container(
    "green",
    css_styles="""
    button {
        background-color: #574EFF;
        border: 1px solid white;
        font-weight: bold;
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
with st.container(border = True, height=500):
    st.markdown(st.session_state.result)

# Persist the "Schedule 1:1" button even after clicking it
with st.container(border = True):
    if st.session_state.show_schedule:
        st.markdown(f'<p style="color:black;font-weight: bold;text-decoration:underline;font-size:20px;height:40px;">Recommended actions:</p>', unsafe_allow_html=True)
        #st.markdown("**Recommended actions:**")
        if st.button("Schedule a check-in", type='primary', on_click=click_schedule_button, key = 'schedule'):
            st.session_state.show_schedule = True  # Mark it as scheduled
            st.session_state.schedule_status = "You have scheduled a 1:1 session with the student, check your calendar app"
            st.success(st.session_state.schedule_status)

    if st.session_state.schedule_clicked: 
        st.success(st.session_state.schedule_status)


    if st.session_state.clicked:
        st.success(st.session_state.schedule_status)

footer_html = """
<style>
.footer {
position: relative;
left: 0;
bottom: 0;
width: 100%;
margin: 0px;
background-color: #212866;
font-size: small;
color: white;
text-align: center;
overflow:auto;
}
</style>

<div style='text-align: center;', class="footer">
  <p>All student response data are synthetic data for demonstration purpose only.</p>
  <p>Evidence-based strategy sourced from Math 7-10 Model from <a href="https://lvp.digitalpromiseglobal.org/content-area/math-7-10">Digital Promise Website</a></p>
  <p>Usage under <a href="https://creativecommons.org/licenses/by-nc/4.0/">Creative Commons license </a></p>
  <img src="https://digitalpromise.org/wp-content/uploads/2022/01/DP_logo_2020.svg" alt="Digital Promise Logo" style="width:200px;height:100px;">
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

