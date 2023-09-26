import time
import openai
import torch
import streamlit as st
from stqdm import stqdm


st.set_page_config(
    page_title="ChemAI",
)
# Access the OpenAI API key from the secrets.toml file
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Set the API key for OpenAI
openai.api_key = openai_api_key


  #%%
def element_ai(text_input):
    response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {
            "role":"system",
            "content":"""
                Generate a short summary for any element. This AI will output The name of an element,
                The chemical symbol of an element,The atomic number of an element,The electron configuration of an element
                The properties of an element, such as its atomic mass, density, and melting and boiling points depends on the user request.
                This chat able to create summary of any elements in periodic table.
                """
        },

        {
            "role":"user",
            "content" : """
                        Can you give me a summary of oxygen?
                        """
        },

        {
            "role":"assistant",
            "content": """
                        Oxygen is Earth's most abundant element, and after hydrogen and helium,
                        it is the third-most abundant element in the universe. At standard temperature and pressure,
                        two atoms of the element bind to form dioxygen, a colorless and odorless diatomic gas with the formula O. 2.
                        """
        },
        {
            "role":"user",
            "content" : text_input
        }
        ],
    max_tokens = 1000,
    temperature = 1
    )

    elementer = response['choices'][0]['message']['content']
    return elementer


#%%
# Setup Streamlit App
# Define custom styles for justified text
justified_text_style = '''
<style>
.justified-text {
    text-align: justify;
    font-family: "Times New Roman"
}
</style>
'''
st.markdown(justified_text_style, unsafe_allow_html=True)

info = """
I am ChemAI who is your chemistry assistant which able to help with your homework and your questions specifically about periodic table.
Ask me anything about elements in the periodic table.
"""

title = """
    font-size: 48px;
    font-weight: bold;
    color: #FFFFFF;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 10px;
"""
st.markdown(
    f'<h1 style="{title}">ChemAI</h1>',
    unsafe_allow_html=True
)

st.sidebar.markdown(f'<div class="justified-text">{info}</div>', unsafe_allow_html=True)

with st.form(key='my_form'):
      text_input = st.text_area("Input your question here")
      submitted = st.form_submit_button('Submit')
    
if submitted:


    for i in stqdm(range(100), backend=True, frontend=True):
      time.sleep(0.5)

    element = element_ai(text_input)
    st.markdown('**_Output:_** ')
    st.write(element)


