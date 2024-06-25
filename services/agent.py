import operator

from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from langgraph.graph import END, StateGraph
from services.prompts import SYSTEM_PROMPT
from typing import TypedDict, Annotated
from services.custom_logger import logger
from services.llm import LLM
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


async def legislatia(message, history):
    agent = Agent(LLM,
                  tools=[QueryRenaissanceProgram()],
                  system=SYSTEM_PROMPT)
    messages = format_messages_for_agent(message, history)
    whole_response = ''
    async for event in agent.graph.astream_events(
        {"messages": messages},
        version="v1"
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "LangGraph"
            ):
                logger.info(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                )
        elif kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                # print(content, end="|")
                whole_response += content
                yield whole_response
