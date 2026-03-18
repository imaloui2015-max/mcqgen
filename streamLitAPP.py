import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.MCQGenrator import quiz_chain, review_chain
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st

#read our response.json
with open(r'C:\Users\USER\mcqgen\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQ Generator App end to end application with langchain and google gemini")

#create a form using streamlit form
with st.form("user_inputs"):
    #upload file
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    #input fields
    mcq_count = st.number_input("NO. of MCQs", min_value=3, max_value=50)

    #subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #Quiz_tone
    tone = st.text_input("Complexity level of Qestiosn", max_chars=20, placeholder="Simple")

    #ADD Button
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                #read file
                text = read_file(uploaded_file)
                response = quiz_chain.invoke({
                    "text":text,
                    "number":mcq_count,
                    "subject":subject,
                    "tone":tone,
                    "response_json":json.dumps(RESPONSE_JSON)})
                review = review_chain.invoke({
                    "subject":subject,
                    "quiz":response
                })

                #st.write(response)
            
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred while generating MCQs. Please try again.")

            else:
                if isinstance(response, dict):
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("ERROR")
                    else:
                        st.error("ERROR")
                else:
                    st.write(response)
                
        

