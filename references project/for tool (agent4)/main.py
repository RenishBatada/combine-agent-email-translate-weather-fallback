from typing import Union
from dotenv import load_dotenv
from langchain.agents import tool
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
import langchain_core.prompts
from langchain_groq import ChatGroq
from langchain.agents.output_parsers import ReActSingleInputOutputParser
import os
from langchain.schema import AgentAction, AgentFinish
from callbacks import AgentCallbackHandler


load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """
    This function calculates the length of the text passed to it.
    text: str -> text whose length is to be calculated
    return: int -> length of the text
    """

    print(f"\n\n\nCalculating length of the {text=}")

    text = text.strip("\n").strip("'").strip('"').strip('"""').strip("'''").strip("\t")
    return len(text)


if __name__ == "__main__":
    # print(get_text_length.invoke(input={"text":"Hello, World! i'm renish"}))
    tools = [get_text_length]

    template = """
        
        (Note : if you get tool output in {agent_scratchpad} then this means the tool is runned and output is given so return this as answer .)
        
        Answer the following questions as best you can. You have access to the following tools:

            {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
                            or
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Begin!

            Question: {input}
            Thought: {agent_scratchpad} (agent_scratchpad is the list of thoughts and actions taken so far with tool output if tool output given in the previous step kindly consider for answer)
            
            Output: AgentAction or AgentFinish object with the answer not both
            
            
    """

    # template = """
    # Answer the following questions as best you can. You have access to the following tools:

    #     {tools}

    # Use the following format:

    # Question: the input question you must answer
    # Thought: you should always think about what to do
    # Action: the action to take, should be one of [{tool_names}]
    # Action Input: the input to the action
    # Observation: the result of the action
    # ... (this Thought/Action/Action Input/Observation can repeat N times)
    # Thought: I now know the final answer
    # Final Answer: the final answer to the original input question (only if no action is required)
    # you must return the AgentAction or AgentFinish object with the final answer not both

    # Begin!

    # Question: {input}
    # Thought: {agent_scratchpad}
    # """

    
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=",".join([tool.name for tool in tools]),
    )

    llm = ChatGroq(
        temperature=0, model="llama-3.3-70b-versatile", stop=["\nObservation","nObservation"],
        callbacks=[AgentCallbackHandler()],
    )
    intermediate_steps = []

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: x["agent_scratchpad"],
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )



    agent_step = ""
    while not isinstance(agent_step, AgentFinish):
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            input={
                "input": "What is the length of the word:Renish",
                "agent_scratchpad": intermediate_steps,
            }
        )

        print(agent_step)

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = [tool for tool in tools if tool.name == tool_name][0]
            tool_input = agent_step.tool_input

            obersevation = tool_to_use.func(str(tool_input))
            print(f"\n\n\n\ntool output is {obersevation=}\n\n\n")
            
            
            new_agent_step = AgentAction(
                tool=agent_step.tool,
                tool_input=f"{agent_step.tool_input} | Previous Output: {obersevation}",
                log=f"{agent_step.log}\n Tool Output: {obersevation}"
            )
            
            this_step_result = new_agent_step
            
            # intermediate_steps.append((agent_step,{"tool output in privous step": str(obersevation)}))
            
            intermediate_steps.append(this_step_result)

            
            print(f"{intermediate_steps=}")
            a= input("Enter to continue")
    if isinstance(agent_step, AgentFinish):
        print("from result")
        print("/n"*5)
        print(agent_step.return_values["final_answer"])
        
