from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langgraph.pregel.main import Runnable
from prompts import SYSTEM_PROMPT
from langchain_ollama import ChatOllama

model: BaseChatModel = ChatOllama(model="gemma3", temperature=0)

agent: Runnable = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT
)

def ask_question(msg: str, context: str) -> str:
    prompt: str = f"Answer only using the following context:\n\n{context}\n\nQuestion: {msg}"
    result: dict = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    response: str = result["messages"][-1].content
    return response
