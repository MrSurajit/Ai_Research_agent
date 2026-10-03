# 🤖 AI Research Agent

An AI-powered research and file analysis assistant built with **Streamlit, Agno, Groq, and DuckDuckGo**.

The application allows users to ask questions, search the web, and upload files directly in the chat to ask the AI to analyze or work with their content.

## ✨ Features

- 🤖 AI-powered chat assistant
- 🔎 Web research using DuckDuckGo
- 🧠 Groq-powered AI responses
- 📎 Upload files directly in the chat
- 📄 PDF support
- 📝 TXT support
- 📃 DOCX support
- 📊 CSV support
- 📈 Excel/XLSX support
- 💬 Chat history
- 🗑️ Clear conversation
- 💾 SQLite database support
- 🌐 Streamlit web interface

## 📎 File Upload

Users can upload a file directly from the chat input and ask the AI to perform different tasks.

For example:

> Summarize this document.

> Extract all email addresses.

> Find the important information on page 5.

> Analyze this Excel file.

> Explain this document in simple language.

The user can ask questions using natural language instead of selecting from a fixed list of operations.

## 🛠️ Technologies

- Python
- Streamlit
- Agno
- Groq
- DuckDuckGo
- SQLite
- Pandas
- PyPDF
- python-docx
- OpenPyXL

## ▶️ Run the Application 
  streamlit run app.py

## 🚀 Future Improvements


RAG for large documents

Multi-file conversations

Automatic data visualization

Python code execution

Download generated files

PDF report generation

User authentication

Cloud deployment

## 📁 Project Structure

```text
AI_agent/
│
├── app.py
├── agent.py
├── requirement.txt
├── README.md
└── .gitignore



