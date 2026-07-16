# 📄 PDF RAG Assistant

A full-stack AI-powered PDF Question Answering application that allows users to upload PDF documents and ask questions in natural language. The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded PDFs and generate accurate responses using an LLM.

The project includes a complete authentication system with separate Login and Signup pages, ensuring that only authenticated users can access the application.

---

## 🚀 Features

- 🔐 User Authentication (JWT)
- 👤 Separate Login & Signup Pages
- 📂 Upload one or multiple PDF files
- 📖 Automatic PDF text extraction
- ✂️ Intelligent text chunking
- 🔎 Semantic search using FAISS
- 🤖 AI-powered question answering
- 💬 Interactive chat interface
- 🗂 Conversation history
- 📱 Responsive UI
- ⚡ FastAPI backend
- 🎨 Clean HTML, CSS & JavaScript frontend

---

## 🛠 Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- FastAPI
- Python
- JWT Authentication

### AI / NLP

- LangChain
- Sentence Transformers
- FAISS
- HuggingFace / Groq LLM

### Database

- MongoDB

---

# 📂 Project Structure

```
PDF-RAG-Assistant
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── auth
│   │   ├── services
│   │   ├── models
│   │   ├── database
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── login.html
│   ├── signup.html
│   ├── index.html
│   ├── css
│   ├── js
│   └── assets
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/pdf-rag-assistant.git

cd pdf-rag-assistant
```

---

## 2. Backend Setup

Navigate to backend

```bash
cd backend
```

Create virtual environment

### Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
MONGODB_URL=your_mongodb_connection

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

GROQ_API_KEY=your_groq_api_key
```

---

## 4. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# 🌐 Frontend

Open another terminal.

Navigate to frontend

```bash
cd frontend
```

Run a local server

```bash
python -m http.server 5500
```

Open

```
http://localhost:5500/login.html
```

---

# 🔑 Authentication Flow

```
Signup
   │
   ▼
Login
   │
   ▼
JWT Token Generated
   │
   ▼
PDF RAG Dashboard
```

---

# 📖 How It Works

1. Create an account.
2. Login using your credentials.
3. Upload one or multiple PDF files.
4. PDFs are converted into text.
5. Text is split into chunks.
6. Chunks are converted into embeddings.
7. Embeddings are stored in a FAISS vector database.
8. Ask questions in natural language.
9. Relevant chunks are retrieved.
10. The LLM generates an accurate answer based on the retrieved context.

---

# 📡 API Endpoints

## Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/signup` | Register user |
| POST | `/login` | User login |

---

## PDF

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/upload` | Upload PDF |
| POST | `/ask` | Ask question |

---

# 💡 Future Improvements

- Chat history
- Multiple chat sessions
- Drag & Drop upload
- PDF page citations
- Streaming AI responses
- Dark Mode
- Admin Dashboard
- Docker Support
- Unit Testing
- Rate Limiting
- Email Verification
- Password Reset

---

# 👨‍💻 Author

**Yashika Shakywal**

GitHub: https://github.com/yashikashakywal

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
