from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Business context for session memory
business_context = """
Answer these questions based on this context: The data is from a small, family-owned hotel located in Port Madison, Wisconsin, that has been in business for 
several years. The hotel owners have some basic technical skills and are looking to use GA4 data to improve their website’s performance, particularly focusing 
on increasing bookings and attracting more guests. Keep insights clear, actionable, and free from jargon. The hotel caters primarily to leisure travelers and 
is focused on enhancing guest experiences, providing a relaxing atmosphere, and increasing local tourism. A key conversion event for the hotel is a visitor 
completing a booking on the website. The data you’re working with is from this month, summarized for the whole time period.
"""

def initialize_llm_context():
    if "session_summary" not in st.session_state:
        st.session_state["session_summary"] = business_context

def query_gpt(prompt, data_summary=""):
    try:
        session_summary = st.session_state.get("session_summary", "")
        full_prompt = f"{session_summary}\n\nData Summary:\n{data_summary}\n\nUser Question: {prompt}"

        # Send the prompt to GPT-4 through the OpenAI client instance
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data analyst with a focus on digital growth and conversion optimization."},
                {"role": "user", "content": full_prompt}
            ]
        )
        
        # Access the response using dot notation
        answer = response.choices[0].message.content
        st.session_state["session_summary"] += f"\nUser: {prompt}\nModel: {answer}\n"
        
        return answer

    except Exception as e:
        return f"Error: {e}"


def query_gpt_keywordbuilder(prompt, data_summary=""):
    try:
        full_prompt = f"\n\nData Summary:\n{data_summary}\n\nUser Question: {prompt}"
    
        # Send the prompt to GPT-4 through the OpenAI client instance
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data analyst with a focus on digital growth and conversion optimization."},
                {"role": "user", "content": full_prompt}
            ]
        )
        
        # Access the response using dot notation
        answer = response.choices[0].message.content
        
        return answer

    except Exception as e:
        return f"Error: {e}"
