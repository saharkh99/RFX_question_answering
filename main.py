
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import config
import PyPDF2
import glob
import os
import analysis
import pandas as pd
import generator
import embedding
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.documents import Document


if __name__ == "__main__":
    print("--------------- Analysis ------------------------")
    pdf_directory = '/home/sahar/Downloads/RFX_question_answering/documents/'
    pdf_files = glob.glob(os.path.join(pdf_directory, '*.pdf'))
    llm =  ChatOpenAI(api_key=config.OPENAI_API_KEY, temperature=0.0, model = "gpt-4o-mini")
    docs = []
    for pdf_file in pdf_files:
        try:
            with open(pdf_file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                first_page = reader.pages[0].extract_text()
                info = reader.metadata
                num_pages = len(reader.pages)
                content = ""
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    content += page.extract_text()
                print("#####################################################################")
                print(f'File: {pdf_file} - Pages: {num_pages}')
                print(generator.generate_insight(content,llm))
                print()
                docs.append(content)   
        except PyPDF2.errors.PdfReadError as e:
            print(f"Error reading {pdf_file}: {e}")

    print("------------ General Analysis ------------------")
    # df = analysis.process_documents(docs)
    # print(df.head())
    classifications = analysis.classify_documents(docs)
    for i, classification in enumerate(classifications):
        print(f"Document {i + 1}: {classification}")
    
    print("-------------Question Answering ------------------")
    # question - answering
    question = "what is the date document submitted?"
    splits = embedding.splitting_text_recursive([Document(page_content=docs[0])])
    vectorstore = Chroma.from_documents(documents=splits,
                                            embedding= OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY))

    docs = embedding.retrieve_from_chroma(vectorstore, query_vector=question)
    rag_generator = generator.generate_response(question, docs,llm)

    print(f"question: {question}")
    print(f"answer: {rag_generator}")
