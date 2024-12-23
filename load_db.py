import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# from pathlib import Path
# from pprint import pprint
# from langchain import hub
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama
# from langchain.schema.document import Document

load_dotenv()


#### Call embedding function for vector store entry and retrieval ####
def get_embedding_function():
    embeddgings = OllamaEmbeddings(model="nomic-embed-text:latest")
    return embeddgings


#### Initialize the vectore databse with connection to local API  ####
def vector_store_init():
    vector_store = Qdrant.from_documents(
        split_documents(),                              # Pass chunked documents to upload to vector DB   
        get_embedding_function(),                                   # Call the embeeding function to store the correct vectors for each chunk 
        url=os.environ['VECTOR_DB_URL'],
        collection_name=os.environ['DB_COLLECTION']                    # Name of collection to store the vector data in can be changed via enviroment variables 
        )
    return vector_store


#### Load the vector database with xlsx documents  ####
def load_excel():

    excel_docs = []                                                     # Initialize list to store all xlsx files in directory 

#### Os walk to crawl through /Data folder for documents ####
    for root, dirs, files in os.walk("./Data"):
        for file in files:
            if file.endswith(".xlsx"):
                excel_docs.append(os.path.join(root, file))


    data = []                                                           # Initialize list to store json documents in  
    
#### Convert xlsx to json documents and append to list ####
    for docs in excel_docs:
        excel_data_df = pd.read_excel(docs, sheet_name='Sheet1')
        excel_data_df.to_json('output.json',orient='records')


        loader = JSONLoader(
        file_path='./output.json',
        jq_schema='.[]',
        text_content=False)

        pages = loader.load()

        data.extend(pages)

    #pprint(len(data))

    return data

#### Split json documents into chunks ####
def split_documents():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,                                        # Change the size of the chunks for accuracy tuning 
        chunk_overlap=0)                                          # Change the overlap size between chunks for better context 
    chunks = text_splitter.split_documents(load_excel())

    #print(len(chunks))
    return chunks

# load_xlsx()

def main():
    vector_store_init()

if __name__ == "__main__":
    main()


















# xl_docs = load_excel()
# split_chunks = split_documents(xl_docs)
# store = vector_store_init(split_chunks)

# retriever = store.as_retriever(search_type="similarity", search_kwargs = {'k': 5}) #, 'fetch_k': 100, 'lambda_mult': 1


# context = retriever.invoke('What is the go live date for SAS0024754')


# model = ChatOllama(model="llama3.2:3b", base_url=os.environ['OLLAMA_URL'])

# # print(model.invoke('hello'))


# prompt = """
#     You are an assistant named Pen-I.
#     You are  designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, you are able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
#     You are constantly learning and improving, and your capabilities are constantly evolving. You are able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, you are able to generate your own text based on the input recieved, allowing you to engage in discussions and provide explanations and descriptions on a wide range of topics.
#     Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, You are here to assist.

#     Use the the following piecese of retreived context to answer questions. Make sure your answer is relevant to the question and is based on the context only.  If you do not know the answer, just say that you don't know.
#     Question: {question}
#     Context: {context}
#     Answer:

# """

# prompt = ChatPromptTemplate.from_template(prompt)


# def format_context(context):
#     return "\n\n".join([c.page_content for c in context])

# # print(format_context(context))

# rag_chain = (
#     {"context": retriever | format_context, "question": RunnablePassthrough()}
#     | prompt
#     | model
#     | StrOutputParser()
# )
 
# final_answer = rag_chain.invoke('What is the go live date for SAS0024754')

# print(final_answer)
