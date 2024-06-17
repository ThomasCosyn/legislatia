from langchain_core.messages import AIMessage, HumanMessage


def format_messages_for_agent(message, history):
    """
    Formats the messages for the agent by creating a list of HumanMessage and
    AIMessage objects.

    Args:
        message (str): The current message from the user.
        history (list): A list of question-answer pairs representing the
        conversation history.

    Returns:
        list: A list of HumanMessage and AIMessage objects representing the
        formatted messages.
    """
    messages = []
    for qa in history:
        messages.append(HumanMessage(content=qa[0]))
        messages.append(AIMessage(content=qa[1]))
    messages.append(HumanMessage(content=message))
    return messages
