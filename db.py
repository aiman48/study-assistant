# db.py
import json, hashlib
from datetime import datetime
from pathlib import Path
from langchain_community.vectorstores import Chroma
from models import get_embeddings

CONV_DIR = Path("conversations")
PERSIST_DIR = ".chroma"
COLLECTION_NAME = "chat-history"
CONV_DIR.mkdir(parents=True, exist_ok=True)
Path(PERSIST_DIR).mkdir(parents=True, exist_ok=True)

def _conv_file(user_id: str) -> Path:
    return CONV_DIR / f"{user_id}.jsonl"

def _make_id(user_id: str, role: str, ts: str, content: str) -> str:
    return hashlib.sha1(f"{user_id}{role}{ts}{content}".encode("utf-8")).hexdigest()

def get_chroma():
    emb = get_embeddings()
    return Chroma(persist_directory=PERSIST_DIR, embedding_function=emb, collection_name=COLLECTION_NAME)

def save_message(user_id: str, role: str, content: str, session_id: str | None = None):
    ts = datetime.utcnow().isoformat()
    rec = {"user_id": user_id, "role": role, "content": content, "timestamp": ts, "session_id": session_id}
    with open(_conv_file(user_id), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    # also add to Chroma
    db = get_chroma()
    db.add_texts(
        texts=[content],
        metadatas=[{"user_id": user_id, "role": role, "timestamp": ts, "session_id": session_id}],
        ids=[_make_id(user_id, role, ts, content)],
    )
    db.persist()

def load_history(user_id: str, k: int = 20):
    path = _conv_file(user_id)
    if not path.exists(): return []
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    recs = [json.loads(l) for l in lines]
    return recs[-k:]

def get_memory_context(user_id: str, k: int = 20) -> str:
    recs = load_history(user_id, k)
    parts = []
    for r in recs:
        who = "Student" if r["role"] == "user" else "Assistant"
        parts.append(f"{who}: {r['content']}")
    return "\n".join(parts)

def export_conversation_file(user_id: str, target_dir: str = "samples") -> str:
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    recs = load_history(user_id, k=1_000_000)
    out = Path(target_dir) / f"{user_id}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps(recs, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(out)

def clear_history(user_id: str):
    p = _conv_file(user_id)
    if p.exists(): p.unlink()
