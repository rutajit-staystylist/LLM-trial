import streamlit as st
import requests

# Function to call the fine-tuned GPT-3.5 model
def call_finetuned_gpt(prompt, model="ft:gpt-4o-2024-08-06:personal:dress-gpt4-new:A6kjHO1g"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['openai']['api_key']}"
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

    # Debugging: Log the entire response
    st.write(response_json)

    # Check if the response contains the expected structure
    if "choices" in response_json and len(response_json["choices"]) > 0 and "message" in response_json["choices"][0]:
        return response_json["choices"][0]["message"]["content"]
    else:
        return "Error: Unexpected response format. Please try again."

# Streamlit app
st.title("AI-Stylist LLM Trial")
st.subheader('Prompt Format')
st.markdown('Body Shape:<Body Shape> , Occasion:<Occassion>, Category: Dress. Suggest at least   5  meta attributes  examples for each of the following -Length, Pattern, Neck, Print,  Shape, Sleeve length, Sleeve styling. OUTPUT FORMAT{ Length: 5 ATTRIBUTES, Pattern: 5 attributes and so on..}')
# Input from user
user_input = st.chat_input('Enter your Prompt')

if user_input:
    with st.spinner("Generating response..."):
        response = call_finetuned_gpt(user_input)
        st.write(f"{response}")

# Check if API key is loaded
if 'api_key' not in st.secrets['openai']:
    st.warning("Please set your OpenAI API key in the secrets file.")
else:
    st.success("API key loaded successfully.")

