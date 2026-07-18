# 📚 PDF RAG Assistant

An AI-powered PDF Question Answering application that allows users to upload one or multiple PDF documents and ask questions in natural language. The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded documents and generate context-aware responses.

> Instead of relying solely on an LLM's knowledge, the assistant searches your uploaded documents and answers based on their content.

---

## 🚀 Live Demo

🔗 **Live Application:** https://your-live-link-here

---

## ✨ Features

- 📄 Upload one or multiple PDF documents
- 🤖 Ask questions in natural language
- 🔍 Semantic search using vector embeddings
- 📑 Context-aware answers from uploaded PDFs
- ⚡ FastAPI backend
- 🔐 User Authentication (Login & Signup)
- 📱 Responsive frontend
- 🚀 Deployed and accessible online

---

## 🛠 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- FastAPI
- Python

### AI & RAG
- LangChain
- FAISS
- Hugging Face Embeddings

### Database
- MongoDB

### Authentication
- JWT Authentication

### Deployment
- Render
- Netlify

---

# 📂 Project Structure

```
Pdf-Rag-Assistant/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── services/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── forgot-password.html
│   ├── reset-password.html
│   ├── style.css
│   ├── script.js
│   └── auth.js
│
├── render.yaml
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yashikashakywal/Pdf-Rag-Assistant.git

cd Pdf-Rag-Assistant
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
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`

Run backend

```bash
uvicorn app.main:app --reload
```

Backend runs on

```
http://127.0.0.1:8000
```

Swagger API

```
http://127.0.0.1:8000/docs
```

---

## 3. Frontend

Open

```
frontend/index.html
```

or serve it using VS Code Live Server.

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
MONGODB_URI=your_mongodb_uri

JWT_SECRET_KEY=your_secret

HUGGINGFACE_API_KEY=your_api_key

LLM_MODEL_NAME=your_model
```

---

# 🧠 How It Works

1. User uploads one or multiple PDF files.
2. PDFs are extracted and split into chunks.
3. Embeddings are generated using Hugging Face.
4. Chunks are stored in a FAISS vector database.
5. User asks a question.
6. Similar chunks are retrieved.
7. The LLM generates an answer using only the retrieved context.
8. The response is displayed to the user.

---

# 📸 Screenshots

Add screenshots here.

Example:

```
screenshots/
    home.png
    login.png
    upload.png
    chat.png
```

---

# 🎯 Challenges Faced

This project involved several real-world challenges:

- Dependency and package version conflicts
- Configuring FAISS and embedding models
- Managing environment variables during deployment
- Improving document retrieval quality
- Debugging API integration issues
- Deploying both frontend and backend successfully

These challenges helped me gain hands-on experience with AI application development, debugging, and deployment.

---

# 📚 What I Learned

- Retrieval-Augmented Generation (RAG)
- LangChain workflows
- Vector databases (FAISS)
- FastAPI development
- Authentication using JWT
- MongoDB integration
- REST API development
- AI application deployment
- Debugging complex dependency issues

---

# 🚀 Future Improvements

- Conversation memory
- Streaming responses
- PDF highlighting
- Chat history
- Admin dashboard
- OCR support for scanned PDFs
- Better citation support
- Docker support

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit a Pull Request.

---

# 👩‍💻 Author

**Yashika Shakywal**

GitHub: https://github.com/yashikashakywal

LinkedIn:www.linkedin.com/in/yashikashakywal

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub. It helps others discover the project and motivates further improvements.
