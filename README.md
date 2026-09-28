# Support Triage Agent

A small LangGraph agent that reads a customer support ticket, classifies its
category and urgency, and decides on its own whether to escalate it to a
human agent or auto-respond.

## How it works

```
classify_ticket → assess_urgency → (conditional) → escalate_to_human → END
                                                  └→ auto_respond      → END
```

- **classify_ticket**: assigns the ticket to `billing`, `technical`, `refund`, or `other`
- **assess_urgency**: rates urgency as `low`, `medium`, or `high`
- **routing**: if urgency is `high`, the agent escalates to a human; otherwise it
  drafts an automatic reply itself
- Each node is an independent LLM call (`gpt-4o-mini` via `langchain-openai`); the
  routing decision between escalation and auto-response is made by the graph
  itself based on the state, not by a fixed pipeline

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your OPENAI_API_KEY
python3 app/main.py
```

## Stack

Python, LangGraph, LangChain (OpenAI), `python-dotenv`.
