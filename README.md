# PDF RAG Chatbot

A simple chatbot that reads a PDF document and answers questions about its content. It uses **RAG (Retrieval-Augmented Generation)** — a technique that finds relevant parts of the document and feeds them to an AI model to generate accurate answers.

---

## What This Project Does

1. **Loads a PDF** — extracts all text from the document
2. **Splits text into chunks** — breaks the text into smaller overlapping pieces
3. **Creates embeddings** — converts each chunk into a list of numbers (vectors) that capture meaning
4. **Stores in a vector database** — saves chunks and their vectors for fast searching
5. **Retrieves relevant chunks** — when you ask a question, finds the most similar chunks
6. **Generates an answer** — feeds the question and retrieved chunks to an AI model to produce a response

---

## Project Structure

```
Pdf_RAG_LLM/
├── app.py                 # Command-line version (run in terminal)
├── streamlit_app.py       # Web version (run in browser)
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── data/
│   └── uploads/           # Uploaded PDFs are saved here
└── src/                   # Core modules (each does one thing)
    ├── pdf_loader.py      # Extract text from PDF
    ├── splitter.py        # Split text into chunks
    ├── embeddings.py      # Create embedding model
    ├── vector_store.py    # Build FAISS vector database
    ├── retriever.py       # Search for relevant chunks
    ├── llm.py             # Create language model (Ollama)
    └── rag.py             # Combine retrieval + generation
```

---

## What You Need to Install

### 1. Python 3.10+
Download from [python.org](https://www.python.org/downloads/)

### 2. Ollama (runs AI models locally)
- Download from [ollama.com](https://ollama.com/)
- After installing, open a terminal and run:
  ```bash
  ollama pull qwen3-embedding:0.6b
  ollama pull gemma3:12b
  ```
  These download the embedding model and the chat model.

### 3. Python packages
```bash
pip install -r requirements.txt
```

**requirements.txt contents:**
```
langchain
langchain-community
langchain-ollama
langchain-text-splitters
pypdf
faiss-cpu
streamlit
```

---

## How to Run

### Option A: Command Line (Terminal)
```bash
python app.py
```
Then type the path to your PDF (e.g., `data/uploads/myfile.pdf`) and start asking questions. Type `exit` to quit.

### Option B: Web Interface (Browser)
```bash
streamlit run streamlit_app.py
```
This opens a web page at `http://localhost:8501`. Upload a PDF, click "Process PDF", then ask questions in the text box.

---

## How Each Part Works (Simple Explanation)

### `src/pdf_loader.py` — PDF Text Extractor
- Opens the PDF file using `pypdf`
- Reads every page and pulls out the text
- Returns one big string with all the text

### `src/splitter.py` — Text Chunker
- Takes the long text string
- Cuts it into pieces of ~1000 characters
- Overlaps pieces by 200 characters so context isn't lost at boundaries
- Returns a list of chunks

### `src/embeddings.py` — Embedding Model Creator
- Creates an **embedding model** (qwen3-embedding:0.6b via Ollama)
- This model converts text into **vectors** (lists of 1024 numbers)
- Similar meanings = similar vectors (close in mathematical space)

### `src/vector_store.py` — Vector Database Builder
- Takes all chunks and the embedding model
- Converts each chunk to a vector
- Stores everything in **FAISS** (a fast vector search library)
- Returns a searchable database

### `src/retriever.py` — Search Tool
- Wraps the vector store with a simple search interface
- Given a question, finds the top `k` (default 4) most similar chunks
- Returns those chunks for the AI to read

### `src/llm.py` — Language Model Creator
- Creates the chat model (gemma3:12b via Ollama)
- This model generates human-like answers
- Temperature = 0 means consistent, factual answers

### `src/rag.py` — The Brain (Retrieval + Generation)
1. Takes your question
2. Uses retriever to find relevant chunks
3. Combines chunks into a "context" block
4. Builds a prompt with instructions + context + question
5. Sends to the language model
6. Returns the model's answer

### `app.py` — Command-Line App
- Asks for PDF path
- Builds the full pipeline once
- Loops: ask question → get answer → repeat

### `streamlit_app.py` — Web App
- File uploader for PDF
- "Process PDF" button builds the pipeline
- Text input for questions
- "Ask" button shows the answer
- Uses Streamlit's session state to remember the pipeline

---

## Key Concepts (For Your Professor)

| Concept | Simple Explanation |
|---------|-------------------|
| **RAG** | Instead of asking the AI to memorize everything, we give it the relevant pages from your PDF when you ask a question. |
| **Embeddings** | Text turned into numbers so a computer can measure similarity mathematically. |
| **Vector Store** | A database optimized for finding "closest" vectors (most similar text). |
| **Retriever** | The component that searches the vector store for relevant chunks. |
| **LLM** | Large Language Model — the AI that generates the final answer in natural language. |
| **Chunking** | Breaking long text into pieces so we can search precisely and fit into the AI's context window. |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "PDF not found" | Check the path; use forward slashes or raw strings on Windows |
| Ollama connection error | Make sure Ollama is running (`ollama serve`) and models are pulled |
| Slow first run | First run downloads model weights; subsequent runs are fast |
| Out of memory | Use smaller models (e.g., `gemma3:4b` instead of `gemma3:12b`) |

---

## Customization

Change models in code:
- **Embedding model**: Edit `src/embeddings.py` → `model="other-model"`
- **Chat model**: Edit `src/llm.py` → `model="other-model"`
- **Chunk size**: Edit `src/splitter.py` → `chunk_size=500`
- **Number of chunks retrieved**: Edit `src/retriever.py` → `k=6`

---

## License

Educational / Personal use.