import os
import pickle
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

'''enter your openai api key'''
os.environ["OPENAI_API_KEY"] = "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"

'''Add the path to your pdf file'''
reader = PdfReader('AntBuddy.pdf')

raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

'''Divide the input data into chunks
    This will help in reducing the embedding size as we will se in the code
    as well as reduce the token size for the query,'''
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)


embeddings = OpenAIEmbeddings(disallowed_special=())
docsearch = FAISS.from_texts(texts, embeddings)


with open("testbot.pkl", 'wb') as f:
    pickle.dump(docsearch, f)
