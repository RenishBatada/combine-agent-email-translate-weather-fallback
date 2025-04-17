from typing import Set
from backend.core import run_llm
import time

import streamlit as st


# if "user_prompt_history" not in st.session_state:
#     st.session_state["user_prompt_history"] = []

# if "chat_answer_history" not in st.session_state:
#     st.session_state["chat_answer_history"] = []


if (
    "user_prompt_history" not in st.session_state
    and "chat_answer_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answer_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""

    source_list = sorted(source_urls)

    sources_string = "Sources:\n"

    for i, source in enumerate(source_list):
        sources_string += f"{i+1}. {source}\n"

    return sources_string


st.header("LangChain Documentation Helper")

user_prompt = st.text_input(
    placeholder="Enter your question here ...",
    label="Ask a question about LangChain Documentation",
)

if user_prompt:
    with st.spinner("Generating answer ..."):

        time.sleep(1)

        generated_answer = run_llm(
            user_prompt, chat_history=st.session_state["chat_history"]
        )

        source = set([doc.metadata["source"] for doc in generated_answer["source"]])

        formatted_response = f"""
            {generated_answer["answer"]} 
            \n \n 
            {create_sources_string(source)}
            """

        st.session_state["user_prompt_history"].append(user_prompt)
        st.session_state["chat_answer_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", user_prompt))
        st.session_state["chat_history"].append(("ai", formatted_response))


if st.session_state["chat_answer_history"]:
    with st.expander("Chat History", expanded=True):

        for i in reversed(range(len(st.session_state["chat_answer_history"]))):

            st.chat_message("user").write(
                f" {st.session_state['user_prompt_history'][i]}"
            )
            st.chat_message("assistant").write(
                f"{st.session_state['chat_answer_history'][i]}"
            )
