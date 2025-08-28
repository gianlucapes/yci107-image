from langgraph.graph import StateGraph, END
import google.generativeai as genai
from langserve import add_routes
from fastapi import FastAPI
from config import settings
from pydantic import BaseModel
from typing import Optional

# 1. Configura Gemini
genai.configure(api_key=settings.api_google)
model = genai.GenerativeModel()

class State(BaseModel):
    input: str
    prompt: str
    message: str = ""
    response: str = ""


def start_node(state: State):
    return State(input=state.input, message=f"L'utente ha detto: {state.input}", response="")

def llm_node(state: State):
    response_text = model.generate_content(state.message).text
    return State(input=state.input, message=state.message, response=response_text)


# 4. Costruisci il workflow
workflow = StateGraph(State)
workflow.add_node("start", start_node)
workflow.add_node("llm", llm_node)
workflow.set_entry_point("start")
workflow.add_edge("start", "llm")
workflow.add_edge("llm", END)

# 5. Compila
app_graph = workflow.compile()

# 6. Integrazione con LangServe
app = FastAPI()
add_routes(app, app_graph, path="/graph")
# Avvio: uvicorn server:app --reload