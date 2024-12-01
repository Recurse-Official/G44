import streamlit as st
from rag import answer_query

st.title("Help Assistant")

if 'contract_text' in st.session_state and st.session_state['contract_text'] != '':
        prompt = st.chat_input("If you have any doubts, let us know!")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            with st.spinner("Answering Your Query"):
                response = answer_query(prompt)
                with st.chat_message("bot"):
                    st.write(response.text)

else:
     st.write("Upload file in PDF parser :)")