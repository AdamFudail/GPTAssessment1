import time
import openai
import torch
import streamlit as st
from stqdm import stqdm
from diffusers import DiffusionPipeline


st.set_page_config(
    page_title="ChemAI",
)

with st.sidebar:
  with st.form("API KEY"):
    openai_api_key = st.text_input("OpenAI API key", value="", type="password")
    st.caption("*If you don't have an OpenAI API key, get it [here](https://platform.openai.com/account/api-keys).*")
    submitted_key = st.form_submit_button('Submit')



if submitted_key:
  try:
      openai.api_key = openai_api_key
      response = openai.Completion.create(engine="davinci", prompt="test")
  except Exception as e:
      st.warning(f'Invalid OpenAI API key: {e}')


#%%
#GPT-3.5-Paramters
#(A) Element Generator
element_gen = """
Generate a short summary for any element. This AI will output The name of an element,
The chemical symbol of an element,The atomic number of an element,The electron configuration of an element
The properties of an element, such as its atomic mass, density, and melting and boiling points depends on the user request.
This chat able to create summary of any elements in periodic table.
"""

Element_user1 = """
Can you give me a summary of oxygen?
"""

Element_response1 = """
Oxygen is Earth's most abundant element, and after hydrogen and helium,
it is the third-most abundant element in the universe. At standard temperature and pressure,
two atoms of the element bind to form dioxygen, a colorless and odorless diatomic gas with the formula O. 2.
"""

element_user2 = """
Can you give me a summary of neon?
"""

element_response2 = """
Neon is a chemical element with the symbol Ne and atomic number 10. It is a noble gas. Neon is a colorless, odorless, inert monatomic gas under standard conditions, with about two-thirds the density of air.
It was discovered (along with krypton and xenon) in 1898 as one of the three residual rare inert elements remaining in dry air, after nitrogen, oxygen, argon and carbon dioxide were removed.
Neon was the second of these three rare gases to be discovered and was immediately recognized as a new element from its bright red emission spectrum.
The name neon is derived from the Greek word, νέον, neuter singular form of νέος (neos), meaning 'new'.
Neon is chemically inert, and no uncharged neon compounds are known. The compounds of neon currently known include ionic molecules, molecules held together by van der Waals forces and clathrates.
"""

element_user3 = """
Can you give me the boiling points of iron?
"""

element_response3 = """
Iron has a Boiling Point of 2861°C, meaning at 2861°C it will turn to a Gas.
"""


  #%%

def element_ai(text_input):
    response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {
            "role":"system",
            "content": element_gen
        },

        {
            "role":"user",
            "content" : Element_user1
        },

        {
            "role":"assistant",
            "content": Element_response1
        },

        {
            "role":"user",
            "content" : element_user2
        },

        {
            "role":"assistant",
            "content": element_response2
        },

        {
            "role":"user",
            "content" : element_user3
        },

        {
            "role":"assistant",
            "content": element_response3
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
}
</style>
'''
st.markdown(justified_text_style, unsafe_allow_html=True)

info = """
I am ChemAI who is your chemistry assistant which able to help with your homework and your questions specifically about periodic table.
Ask me anything about elements in the periodic table and I will summarize the elements and give the picture of it.
It also allows you to generate an image of the elements by using Stable Diffusion XL.
"""

st.markdown("<h1 style='text-align: center; color: black;'>ChemAI</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([5,5])

col1.markdown(f'<div class="justified-text">{info}</div>', unsafe_allow_html=True)

form = col2.form

with form('input_form'):
      text_input = st.text_area("Input your question here")

      submitted = st.form_submit_button('Submit')

      text_inputs = [text_input]

if submitted:


    for i in stqdm(range(100), backend=True, frontend=True):
      time.sleep(0.5)

    element = element_ai(text_input)
    st.markdown('**_Output:_** ')
    st.write(element)


