import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document

st.title("Class_1_Demo")

# Initialize state variables
urls = st.text_area("Enter the URLs of the 5 Wikipedia pages", height=100)
page_strings = ""
hops = ""

# Load the content of each Wikipedia page as a Document object
def load_pages(urls):
    from langchain.document_loaders import WebBaseLoader
    loader = WebBaseLoader(urls)
    docs = loader.load()
    return docs

# Scrape the Wikipedia pages and calculate the number of hops between pages
def webScraper(page_strings):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0
    )
    system_template = """You are a web scraper tasked with calculating the number of hops between Wikipedia pages."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please scrape the Wikipedia pages and calculate the number of hops between the following pages: {page_strings}."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(page_strings=page_strings)
    return result # returns string   

# Get input from the user
if st.button("Submit"):
    if urls:
        pages = load_pages(urls)
        page_strings = "".join([doc.page_content for doc in pages])
        hops = webScraper(page_strings)

# Display the number of hops between pages
st.markdown(f"The number of hops between pages is: {hops}")
