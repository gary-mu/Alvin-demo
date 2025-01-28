from dotenv import load_dotenv 
import requests
import os 
import streamlit as st

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "6d400d27-daa8-4515-abb1-f651b3fb82dd"
FLOW_ID = "828e9c78-a492-427c-9e8c-a4a92d8d226f"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN") 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ENDPOINT = "Math_7_10" # The endpoint name of the flow


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


def main():
    st.title("Alvn - Along + LVN AI Agent Demo")
    st.subheader("Welcome to Alvn - An AI agent that that uses pedagogically aligned insights to support each learner’s journey.")
    st.write("Ask your questions to get the best strategies to help your students")

    message = st.text_area("Enter your questions here", placeholder = 'Ask your question to get the best strategies to help your students') 

    if st.button("Ask Alvn", type="primary"):
        if not message.strip():
            st.error("Please enter a question")
            return
        try: 
            with st.spinner("Thinking...feel free to grab a beverage while you wait"):
                response = run_flow(message)
            result = response['outputs'][0]['outputs'][0]['results']['message']['text']
            st.markdown(result)
        except Exception as e:
            st.error("An error occurred: " + str(e))

if __name__ == "__main__":
    main()

footer_html = """<div style='text-align: center;'>
  <p>All data are synthtic data for demonstration purpose.</p>
  <p>Evidence-based strategy sourced from Math 7-10 Model from <a href="https://lvp.digitalpromiseglobal.org/content-area/math-7-10">Digital Promise Website</a></p>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)

