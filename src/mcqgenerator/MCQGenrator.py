import os
import json
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file,get_table_data
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(dotenv_path=".env", override=True)

mykeys = os.getenv("KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=mykeys,
    temperature=0.3
)

quiz_template = """
Text:{text}

You are an expert MCQ maker.

Create {number} multiple choice questions for {subject} students in {tone} tone.

### RESPONSE_JSON
{response_json}
"""
quiz_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=quiz_template
)

parser = StrOutputParser()
quiz_chain = quiz_prompt | llm | parser

review_template ="""
You are an expert English writer.

Evaluate the complexity of the following quiz for {subject} students.

Quiz:
{quiz}
"""

review_prompt = PromptTemplate(
    input_variables=["subject","quiz"],
    template=review_template
)

parser = StrOutputParser()
review_chain = review_prompt | llm | parser

quiz = quiz_chain.invoke({
    "text":"AI transferme",
    "number":5,
    "subject":"computer science",
    "tone":"simple",
    "response_json":"{}"
})

review = review_chain.invoke({
    "subject":"Computer Science",
    "quiz":quiz
})

print("QUIZ:\n",quiz)
print("\nREVIEW:\n",review)

