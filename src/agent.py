from langchain.agents import create_agent
from prompts import SYSTEM_PROMPT

agent = create_agent(
    model="ollama:gemma3",
    system_prompt=SYSTEM_PROMPT
)

def ask_question(msg: str) -> str:
    result: dict = agent.invoke({"messages": [{"role": "user", "content": msg}]})
    response: str = result["messages"][-1].content
    return response