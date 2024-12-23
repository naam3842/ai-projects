import os
from langchain_qdrant import QdrantVectorStore
from load_db import get_embedding_function
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from retrieval import format_context
# import argparse
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

load_dotenv('./.env')

def rag_lookup(query):
    

    PROMPT_TEMPLATE = """
    You are an assistant named Pen-I.
    You are  designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, you are able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    You are constantly learning and improving, and your capabilities are constantly evolving. You are able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, you are able to generate your own text based on the input recieved, allowing you to engage in discussions and provide explanations and descriptions on a wide range of topics.
    Only respond to questions that you are able to answer, and be sure to provide accurate and relevant responses based on the context provided.
    Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, You are here to assist.

    Use the the following piecese of retreived context to answer questions. Make sure your answer is relevant to the question and is based on the context only.  If you do not know the answer, just say that you don't know.
    Question: {question}
    Context: {context}
    Answer:

    """

    #### Prepare DB ####
    
    DB = QdrantVectorStore.from_existing_collection(
            collection_name=os.environ['DB_COLLECTION'],
            embedding=get_embedding_function(),
            url=os.environ['VECTOR_DB_URL']
        )
    
    results = DB.similarity_search(query, k=5)                                                      # Get 5 similar documents to the query

    rag_context = format_context(results)                                                           # Format the context for the prompt template

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)                             # Load our custom PROMPT_TEMPLATE

    prompt = prompt_template.format(question=query, context=rag_context)                            # Create the prompt for the the chat model to respond to 

    model = ChatOllama(model=os.environ["CHAT_MODEL"], base_url=os.environ['OLLAMA_URL'])           # Load the chat model from environment file

    final_answer = model.invoke(prompt)

    return final_answer.content

