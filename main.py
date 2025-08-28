from langgraph.graph import StateGraph, END
import google.generativeai as genai
from langserve import add_routes
from fastapi import FastAPI

# 1. Configura Gemini
genai.configure(api_key="IL_TUO_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. Definisci lo stato
class State(dict):
    pass

# 3. Nodi del grafo
def start_node(state: State):
    user_input = state.get("input", "")
    return {"message": f"L'utente ha detto: {user_input}"}

def llm_node(state: State):
    message = state["message"]
    response = model.generate_content(message)
    return {"response": response.text}

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
