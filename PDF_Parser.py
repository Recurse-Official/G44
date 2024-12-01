import os
import streamlit as st
from utils import extract_content
from rag import query_output, update_vector_store




def main():
    st.title("Upload Related Documents")

    st.write("Upload the File")
    contract_pdfs = st.file_uploader("Upload PDFs", type=["pdf"] , accept_multiple_files=True)
    if contract_pdfs:
        with st.spinner('Extracting Content...'):
            st.session_state['contract_text'] =  extract_content(contract_pdfs)
            update_vector_store(st.session_state['contract_text'])
        st.success("Done!")
        st.toast('Contract extracted!')



    if 'contract_text' in st.session_state and st.session_state['contract_text'] != '':
        prompt = st.chat_input("On What topic, do you want to generate questions, let us know!")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            with st.spinner("Generating questions"):
                response = query_output(prompt)
                with st.chat_message("bot"):
                    st.write(response.text)





if __name__ == "__main__":
    main()

