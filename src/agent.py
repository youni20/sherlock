from langchain.agents import create_agent

agent = create_agent(
    model="ollama:gemma3",
    system_prompt="Answer simply and give concise short answers. straight to the point."
)

def ask_question(msg: str) -> str:
    result: dict = agent.invoke({"messages": [{"role": "user", "content": msg}]})
    response: str = result["messages"][-1].content
    return response