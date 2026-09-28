from typing import TypedDict

from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


class State(TypedDict):
    ticket: str
    category: str
    urgency: str
    decision: str

def escalate_to_human(state: State) -> State:
     prompt = f"Bu destek talebini musteri temsilcisine yonlendir.\n\nTalep: {state['ticket']}"
     response = llm.invoke(prompt)
     return {"decision": response.content}
def auto_respond(state: State) -> State:
     prompt = f"Bu destek talebini otomatik olarak cevapla.\n\nTalep: {state['ticket']}"
     response = llm.invoke(prompt)
     return {"decision": response.content}
def route(state: State) -> str:
    if state["urgency"] == "high":
        return "escalate"
    return "auto_respond"    

def assess_urgency(state: State) -> State:
     prompt = f"Bu destek talebini şu kategorilerden birine ata: low, medium, high Sadece kategori adını yaz.\n\nTalep: {state['ticket']}"
     response = llm.invoke(prompt)
     return {"urgency": response.content}
      

def classify_ticket(state: State) -> State:
    prompt = f"Bu destek talebini şu kategorilerden birine ata: billing, technical, refund, other. Sadece kategori adını yaz.\n\nTalep: {state['ticket']}"
    response = llm.invoke(prompt)
    return {"category": response.content}


graph = StateGraph(State)
graph.add_node("classify_ticket", classify_ticket)
graph.add_node("assess_urgency",assess_urgency)
graph.add_node("escalate_to_human", escalate_to_human)
graph.add_node("auto_respond", auto_respond)
graph.set_entry_point("classify_ticket")
graph.add_edge("classify_ticket", "assess_urgency")
graph.add_conditional_edges(
    "assess_urgency",   # bu node bitince
    route,               # bu fonksiyonu çalıştır
    {
        "escalate": "escalate_to_human",   # "escalate" dönerse buraya git
        "auto_respond": "auto_respond",     # "auto_respond" dönerse buraya git
    },
)
graph.add_edge("escalate_to_human", END)
graph.add_edge("auto_respond", END)

app= graph.compile()
result = app.invoke({"ticket": "Faturamda yanlış tutar var, param iade edilsin istiyorum"})
print(result)