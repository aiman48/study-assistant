
# 📚 Study Assistant Chatbot

A study assistant chatbot built with **LangChain**, **Google Gemini** (LLM), and **Hugging Face embeddings**.
The assistant can answer study-related questions, maintain conversation memory, and present **structured output** in a clear format.
It includes an **excellent Streamlit UI** with chat history, memory, and export functionality.

---

## 🚀 Features

✅ Uses **Gemini** as the main LLM
✅ Uses **Hugging Face embeddings** + **Chroma** for conversation memory
✅ Custom **prompt template** → always returns structured JSON:

```json
{
  "answer": "...",
  "key_points": ["...", "..."],
  "follow_up_questions": ["...", "..."],
  "references": ["...", "..."]
}
```

✅ **Streamlit UI** with:

* Chat window (like ChatGPT)
* Structured output sections (Answer, Key Points, Follow-ups, References)
* Sidebar memory viewer
* Export and clear conversation options

✅ **Persistent memory** — conversations are saved with Chroma and JSON logs.

---

## 🛠️ Tech Stack

* [LangChain](https://www.langchain.com/)
* [Google Gemini](https://ai.google.dev/)
* [Hugging Face Embeddings](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)
* [ChromaDB](https://www.trychroma.com/)
* [Streamlit](https://streamlit.io/)

---

## 📂 Project Structure

```
study-assistant/
│── app.py            # Streamlit UI
│── chain.py          # LangChain pipeline (prompt + LLM + memory)
│── models.py         # Gemini + Hugging Face embeddings setup
│── db.py             # Conversation persistence (Chroma + JSON logs)
│── .env              # API keys and model configs
│── requirements.txt  # Dependencies
│── README.md         # Documentation
```

---

## ⚙️ Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/aiman48/study-assistant.git
cd study-assistant-langchain
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add API keys

Create a `.env` file in the root folder:

```ini
# Gemini API (Google AI Studio)
GOOGLE_API_KEY=your_gemini_api_key_here

# Hugging Face
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# Model settings
HF_EMBED_MODEL=sentence-transformers/all-mpnet-base-v2
GEMINI_MODEL=gemini-1.5-flash
```

### 5️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🎮 Usage

1. Open the Streamlit UI in your browser (link shown after running).

2. Type your study questions (e.g., *"Explain supervised learning"*)

3. The assistant will respond with:

   * 📖 **Answer** (natural explanation)
   * 🔑 **Key Points** (bullet notes)
   * 🤔 **Follow-up Questions**
   * 📚 **References**

4. Sidebar shows memory of past chats.

5. Export or clear conversation anytime.

---

## 🧠 Example

**Question:**

> "Explain machine learning models."

**Structured Output:**

```json
{
  "answer": "Machine learning models are algorithms that learn patterns from data...",
  "key_points": [
    "Supervised, unsupervised, reinforcement learning",
    "Models include decision trees, neural networks, SVMs",
    "Used in predictions, classification, recommendations"
  ],
  "follow_up_questions": [
    "What is supervised learning?",
    "How are neural networks trained?"
  ],
  "references": [
    "https://scikit-learn.org/",
    "https://en.wikipedia.org/wiki/Machine_learning"
  ]
}
```

---

## 📌 Requirements Checklist

✔️ LangChain
✔️ Gemini (LLM)
✔️ Hugging Face embeddings
✔️ Memory (Chroma)
✔️ Prompt Template (structured JSON)
✔️ Structured Output
✔️ Messages (chat UI with history)
✔️ Streamlit excellent UI

---
