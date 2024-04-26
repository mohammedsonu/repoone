import json
import openai
import streamlit as st
import os

api_key = st.secrets["open_keys"]
css = """
<style>
    h1 {
        color: yellow;  /* Adjust the color as needed */
    },
    h2 {
        color: green;  /* Change the color as needed */
    }

</style>
"""

st.title("Mnemonic Generator Hackathon")

def GenerateV(inputquestion):
    predefined="""As an expert in creating mnemonics, you are tasked with developing a memorable sentence that aids students in learning a specific concept. Additionally, please provide the exact words that the mnemonic represents.I want the ouput in JSON format.
[
{
"mnemonics":,
"input"
}
]
The topic for this mnemonic is"""
    final_prompt=" ".join([predefined,str(inputquestion)])
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-1106",
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                        {"role": "user", "content": final_prompt
                        }
                    ]
                )
    return response['choices'][0]['message']['content']

query = st.text_input("Enter the Topic to Search")
if st.button('Search'):
    summary = GenerateV(query)
    
    def is_valid_json(data):
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False
    # Extracting values
    check_json=is_valid_json(summary)
    if check_json==True:
            data_dict = json.loads(summary)
            mnemonic_sentence = data_dict['mnemonics']
            exact_words = data_dict['input']
            st.markdown(css, unsafe_allow_html=True)
            st.title(mnemonic_sentence)
            st.markdown(css, unsafe_allow_html=True)
            st.subheader(exact_words)


    else:
        summary = GenerateV(query)
        if check_json==True:
            data_dict = json.loads(summary)
            mnemonic_sentence = data_dict['mnemonics']
            exact_words = data_dict['input']
            st.markdown(css, unsafe_allow_html=True)
            st.title(mnemonic_sentence)
            st.markdown(css, unsafe_allow_html=True)
            st.subheader(exact_words)
  
        else:
            summary = GenerateV(query)
            if check_json==True:
                data_dict = json.loads(summary)
                mnemonic_sentence = data_dict['mnemonics']
                exact_words = data_dict['input'] 
                st.markdown(css, unsafe_allow_html=True) 
                st.title(mnemonic_sentence)
                st.markdown(css, unsafe_allow_html=True)
                st.subheader(exact_words)

                          


