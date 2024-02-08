from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

## initialize the streamlit instance
st.set_page_config(page_title="Chat Bot")
st.header("Gemini Chat Bot")

## intialize the session state for chat history if it doesn't work

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] =[]

input = st.text_input("Input: ",key='input')

submit = st.button('Ask the question')

history = st.button('Show chat history')

if submit and input:
    response = get_gemini_response(input)
    ## add user query and response to the session chat history
    st.session_state['chat_history'].append(("User",input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))
if history:
    st.subheader("Chat history is")

    for role,text in st.session_state['chat_history']:
        st.write(f'{role}:- {text}')
