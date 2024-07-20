import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to call the fine-tuned GPT-3.5 model
def call_finetuned_gpt(prompt, model="ft:gpt-3.5-turbo-0613:personal:dress-new:9lkuyaVt"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "StayStylist is your AI Fashion Stylist, crafting personalized fashion recommendations for every body and style, globally."},
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response_json = response.json()
    return response_json["choices"][0]["message"]["content"]

# Streamlit app
st.title("AI-Stylist LLM Trial")
st.markdown('Body Shape: <Body Shape>, Occasion:<Occasion Type>, Category: Dress. Recommend Multiple and most appropriate  and unique meta attributes (atleast 3 combination) of Dress ayttributes for each of the following: Length, Pattern, Neck, Print, Shape, Sleeve length, Sleeve styling.')
# Input from user
user_input = st.chat_input('Enter your Prompt')

if user_input:
    with st.spinner("Generating response..."):
        response = call_finetuned_gpt(user_input)
        st.write(f"{response}")


# Check if API key is loaded
if os.getenv('OPENAI_API_KEY') is None:
    st.warning("Please set your OpenAI API key in a .env file.")
