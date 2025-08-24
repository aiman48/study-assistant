# chain.py
from typing import List
from pydantic import BaseModel, Field
import json
from json_repair import repair_json

from models import get_gemini_chat
from db import get_memory_context, save_message

SYSTEM_INSTRUCTION = """
You are StudyBuddy — a highly knowledgeable, helpful, and friendly study assistant. 
You explain concepts like a tutor (clear, concise, step-by-step) and also give examples 
when useful.

Your response MUST always be in JSON with these keys:

- answer: (string) a direct, clear explanation in natural language, like how ChatGPT would answer.
- key_points: (array of 3–6 bullet strings) short, focused takeaways.
- follow_up_questions: (array of 2 short questions) things the student might ask next.
- references: (array of strings) external references or sources if available, otherwise [].

Do NOT add extra text outside JSON. Output only valid JSON.
"""

class StudyAnswer(BaseModel):
    answer: str = Field(default="")
    key_points: List[str] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)

def _build_prompt(history: str, question: str) -> str:
    return (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"Chat history:\n{history}\n\n"
        f"Student question:\n{question}\n\n"
        f"Respond with a single JSON object ONLY (no markdown, no prose)."
    )

def _parse_to_schema(text: str) -> StudyAnswer:
    if "{" in text and "}" in text:
        try:
            fixed = repair_json(text[text.find("{"):])
            obj = json.loads(fixed)
            obj.setdefault("answer", "")
            obj.setdefault("key_points", [])
            obj.setdefault("follow_up_questions", [])
            obj.setdefault("references", [])
            return StudyAnswer(**obj)
        except Exception:
            pass
    return StudyAnswer(answer=text.strip())

def invoke_chat(user_id: str, question: str, memory_k: int = 12) -> StudyAnswer:
    history = get_memory_context(user_id, k=memory_k)
    prompt = _build_prompt(history, question)

    llm = get_gemini_chat()
    resp = llm.invoke(prompt)   # Gemini supports string prompts
    text = getattr(resp, "content", None) or getattr(resp, "text", None) or str(resp)

    parsed = _parse_to_schema(text)

    # persist
    save_message(user_id, "user", question)
    save_message(user_id, "assistant", parsed.answer)

    return parsed
