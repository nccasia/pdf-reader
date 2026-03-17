# CV Extraction API

A FastAPI service that extracts structured candidate information from CV files (PDF, DOC, DOCX) using an LLM backend (`api-llm.nccsoft.vn`). Supports both text-based and OCR-based extraction, for single files and batches of URLs.

## Features

- Extract CV data from uploaded files (`PDF`, `DOC`, `DOCX`)
- OCR-based extraction for scanned PDFs via Google Cloud Vision
- Batch extraction from multiple remote URLs (up to 10)
- Clean architecture: domain → use cases → infrastructure → API

## Extracted fields

| Field | Description |
|---|---|
| `fullname` | Candidate name |
| `email` | Email address |
| `phone_number` | Phone number |
| `dob` | Date of birth (`dd/mm/yyyy`) |
| `address` | Address |
| `gender` | Gender |
| `position` | Applied position |
| `note` | Notable certifications / GPA |

## Project structure

```
app/
├── config.py                    # Environment variables & constants
├── main.py                      # FastAPI app entry point
├── domain/
│   └── interfaces.py            # IFileParser, ILLMClient abstractions
├── use_cases/
│   └── extract_cv.py            # Business logic (ExtractCVUseCase)
├── infrastructure/
│   ├── llm/
│   │   ├── client.py            # LLMClient (api-llm.nccsoft.vn)
│   │   └── prompts.py           # System / user prompt templates
│   └── parsers/
│       ├── file_parser.py       # PDF text + OCR parsing
│       └── url_fetcher.py       # Remote URL text/OCR fetching
└── api/
    ├── schemas.py               # Pydantic request/response models
    └── routers/
        └── cv_router.py         # FastAPI route handlers
```

## API endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/check-connection` | Health check |
| `POST` | `/extract-cv` | Extract CV from uploaded file (text) |
| `POST` | `/extract-cv-vision` | Extract CV from uploaded file (OCR) |
| `POST` | `/extract-multifile` | Extract CVs from multiple URLs (text) |
| `POST` | `/extract-multifile-vision` | Extract CVs from multiple URLs (OCR) |

Interactive docs available at `http://localhost:8000/docs`.

## Setup

### 1. Clone & create virtual environment

```bash
git clone <repo-url>
cd pdf-reader
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

```env
GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
CORS_ORIGIN=' "https://frontend.example.com" '
LLM_API_URL="https://llm.nccsoft.vn"
LLM_MODEL_NAME="Qwen3.5-35B-A3B"
```

> `GOOGLE_APPLICATION_CREDENTIALS` is only required for OCR endpoints (`/extract-cv-vision`, `/extract-multifile-vision`).

### 3. Run locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Deployment (Ubuntu Server)

Use the provided shell script to install and register the service with `systemd`:

```bash
chmod +x startup.sh
./startup.sh -p 1300 -host "0.0.0.0"
```

Manage the service:

```bash
# Check status
sudo systemctl status extract_cv.service

# Stop
sudo systemctl stop extract_cv.service

# Restart
sudo systemctl restart extract_cv.service
```
