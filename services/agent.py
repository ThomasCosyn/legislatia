import operator
import os

from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from langchain_mistralai import ChatMistralAI
from langgraph.graph import END, StateGraph
from services.prompts import SYSTEM_PROMPT
from typing import TypedDict, Annotated
from services.tools import QueryRenaissanceProgram
from services.utils import format_messages_for_agent


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_mixtral)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_mixtral(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if t['name'] not in self.tools:
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'],
                                       name=t['name'],
                                       content=str(result)))
        print("Back to the model!")
        return {'messages': results}


def legislatia(message, history):
    model = ChatMistralAI(
        model="Mixtral-8x22B-Instruct-v0.1",
        api_key=os.getenv("OVH_AI_ENDPOINTS_ACCESS_TOKEN"),
        endpoint="https://mixtral-8x22b-instruct-v01.endpoints.kepler.ai.cloud.ovh.net/api/openai_compat/v1",  # noqa
        max_tokens=1000
    )
    agent = Agent(model,
                  tools=[QueryRenaissanceProgram()],
                  system=SYSTEM_PROMPT)
    messages = format_messages_for_agent(message, history)
    result = agent.graph.invoke({'messages': messages})
    return result['messages'][-1].content
