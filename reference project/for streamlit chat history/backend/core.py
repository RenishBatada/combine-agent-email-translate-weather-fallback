import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chains.retrieval import create_retrieval_chain

from langchain import hub

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_pinecone import PineconeVectorStore

from langchain_ollama import ChatOllama, OllamaEmbeddings
from typing import Dict, Any, List

from langchain.chains.history_aware_retriever import create_history_aware_retriever

Index_name = os.getenv("INDEX_NAME")


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> dict:
    embeddings = OllamaEmbeddings(
        model="llama3.2:latest",
        base_url="http://127.0.0.1:11434",
    )

    docsearch = PineconeVectorStore(index_name=Index_name, embedding=embeddings)
    chat = ChatOllama(temperature=0, model="llama3.2")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    stuff_document_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    history_aware_retrieval = create_history_aware_retriever(
        llm=chat,
        retriever=docsearch.as_retriever(),
        prompt=rephrase_prompt,
    )

    qa = create_retrieval_chain(
        history_aware_retrieval, combine_docs_chain=stuff_document_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})

    fromated_result = {
        "query": result["input"],
        "answer": result["answer"],
        "source": result["context"],
    }

    return fromated_result


if __name__ == "__main__":
    # res = run_llm(query="What is a LangChain Chain?")
    res = run_llm(query="What is Large Language Model (LLM)?")
    print("*" * 50)

    print(res["answer"])
