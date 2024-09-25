import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import openai

# Set up the Streamlit app page
st.set_page_config(page_title="SpeakClub - Campaign content generation - An LLM-powered Streamlit app")

# Set your OpenAI API key (make sure to keep it secure and not expose it in the code directly)
OPENAI_API_KEY = "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"
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "OPENAI_API_KEY" not in st.secrets:
    st.error("API Key is missing! Please configure the OpenAI API key in Streamlit Secrets.")
else:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# Sidebar content
with st.sidebar:
    st.title('InviGen App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](<https://streamlit.io/>)
    - [OpenAI](<https://openai.com>) GPT Models
    
    💡 Note: API key required for using OpenAI GPT.
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by Group A7')


# Session state to store the generated messages and user inputs
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm InviGen, How may I help you?"]

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']


# Input and response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# Function to take user input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

# User input from the input container
with input_container:
    user_input = get_text()

# Function to generate response using OpenAI GPT model
def generate_response(prompt):
    try:
        # Update this part to use `ChatCompletion`
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can use "gpt-4" or "gpt-3.5-turbo" based on your need
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Control the response length
            temperature=0.7  # Adjust creativity level
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Displaying the conversation in response container
with response_container:
    if user_input:
        # Generate response using OpenAI
        response = generate_response(user_input)
        
        # Store the user input and generated response in session state
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    # Display the conversation history
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state['generated'][i], key=str(i))

