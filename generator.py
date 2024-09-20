from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

def generate_response(question, docs , llm):
        retrieved_docs = docs
        context = "\n\n".join([doc[0].page_content for doc in retrieved_docs])
       
        ANSWER_PROMPT = ChatPromptTemplate.from_template(
            """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Be as verbose and educational in your response as possible.
        
            context: {context}
            Question: "{question}"
            Answer:
            """
        )

        chain = (
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            | ANSWER_PROMPT
            | llm
            | StrOutputParser()
        )

        ans = chain.invoke({"context":context, "question":question})
        return ans

def generate_insight(content,llm):
    retrieved_docs = content
    # context = "\n\n".join([doc[0].page_content for doc in retrieved_docs])

    ANSWER_PROMPT = ChatPromptTemplate.from_template("""
    You are given a document that is an RFX (Request for X) type such as bids, quotations, or requests. Your task is to extract the following information:

    1. **Value of the Request (in dollar terms)**: Identify and extract the total value of the request or any cost estimation mentioned in the document.
    2. **Category of the Document**: Determine whether the document is a Request for Proposal (RFP), Request for Quotation (RFQ), Invitation to Bid, Invitation to tender ,or Invitation to Quote.
    3. **Summary of the Document**: Provide a concise summary of the key details, including the purpose of the request, the main requirements, and any important deadlines or deliverables.
    4. ** stakeholders and companies**: Extract the name of the company or companies, and stackholders and persons mentioned in the document.
    5. **date of submittion**: Extract the date the document was submitted.
    6. **Helpful Insights**: Extract any other relevant information or insights that might be helpful, such as evaluation criteria, project timelines, or any special instructions.
    
    
    context: {context}
        Answer:
    """
    )

    chain = (
        {"context": RunnablePassthrough()}
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )

    ans = chain.invoke({"context":retrieved_docs})
    return ans