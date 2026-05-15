# CA SaaS — AI-Powered Tool for Chartered Accountants

A full-stack B2B SaaS application built for India's 400,000+ practicing Chartered Accountants.

## 🚀 Features

- **Authentication** — CA Register & Login with JWT tokens
- **Client Management** — Add, view, update, delete clients with PAN details
- **Document Upload** — Upload ITR and notice PDFs with automatic text extraction
- **AI Assistant** — Summarize documents, draft ITD notice replies, ask questions
- **Anomaly Detection** — Scan all clients and flag suspicious patterns
- **Notice Tracker** — Track ITD notices with deadlines and status
- **React Frontend** — Clean web interface for all features

## 🛠️ Tech Stack

**Backend**
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- PyMuPDF (PDF text extraction)
- Groq AI (LLaMA 3.3)

**Frontend**
- React.js
- JavaScript
  
## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/allen745/ca-saas.git
cd ca-saas
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database
```bash
psql -U postgres
CREATE DATABASE ca_saas;
\q
```

### 5. Create .env file

### 6. Run the backend
```bash
uvicorn main:app --reload
```

### 7. Run the frontend
```bash
cd ca-saas-frontend
npm install
npm start
```

## 📡 API Endpoints

### Auth
- `POST /auth/register` — Register a new CA
- `POST /auth/login` — Login and get JWT token

### Clients
- `POST /clients/` — Add client
- `GET /clients/` — List all clients
- `GET /clients/{id}` — Get one client
- `PUT /clients/{id}` — Update client
- `DELETE /clients/{id}` — Delete client

### Documents
- `POST /documents/upload/{client_id}` — Upload PDF
- `GET /documents/{client_id}` — List documents
- `GET /documents/detail/{id}` — Get document

### AI
- `POST /ai/summarize/{document_id}` — Summarize document
- `POST /ai/draft-reply/{document_id}` — Draft ITD notice reply
- `POST /ai/ask/{document_id}` — Ask question about document

### Anomaly Detection
- `GET /anomaly/scan` — Scan all clients for anomalies

### Notice Tracker
- `POST /notices/` — Add notice
- `GET /notices/` — List all notices
- `GET /notices/overdue` — Get overdue notices
- `GET /notices/due-soon` — Get due soon notices
- `PUT /notices/{id}` — Update notice status
- `DELETE /notices/{id}` — Delete notice

## 🗺️ Roadmap

- [x] Block 1 — Authentication
- [x] Block 2 — Client Management
- [x] Block 3 — PDF Upload & Text Extraction
- [x] Block 4 — AI Features
- [x] Block 5 — Anomaly Detection
- [x] Block 6 — Notice Tracker
- [x] Block 7 — React Frontend
- [ ] Deploy to production
- [ ] Switch to Claude AI
- [ ] Mobile app

## 👨‍💻 Built By

Allen Christian — Building in public
- GitHub: github.com/allen745
- LinkedIn: linkedin.com/in/allen-stivanson-christian-74094237a

## 📄 License

MIT License
