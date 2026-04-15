# IT-Agent

AI-driven IT support agent MVP built with FastAPI, Flask admin panel, and browser automation.

## Overview
IT-Agent is a prototype system that automates IT support-style workflows using an agent service and a lightweight admin interface.

## Features
- FastAPI-based agent backend
- Flask admin panel
- Environment-based configuration
- Demo script for local testing
- Modular folder structure for docs and scripts

## Tech Stack
- Python
- FastAPI
- Flask
- Uvicorn
- Browser automation tooling

## Project Structure
```text
IT-Agent/
├── admin_panel/
├── agent/
├── docs/
├── scripts/
├── slack_bot/
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup
### 1. Clone the repository
```bash
git clone https://github.com/Yashsh101/IT-Agent.git
cd IT-Agent
```

### 2. Create virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file using `.env.example` and add your local keys.

## Run locally

### Start admin panel
```bash
python -c "from admin_panel.app import app; app.run(host='127.0.0.1', port=5000, debug=False)"
```

### Start agent server
```bash
python -m uvicorn agent.server:app --host 127.0.0.1 --port 8000
```

### Run demo
```bash
python .\scripts\run_demo.py
```

## Current Status
This project is an MVP submission.

### Working
- Project structure and service separation
- FastAPI service startup
- Flask admin panel startup
- Environment-based configuration
- Local demo/testing scripts

### In Progress
- End-to-end stabilization of agent workflows
- Production hardening
- Better test coverage

## Known Issues
- Some automation flows may require additional stabilization
- This project is currently optimized for local MVP demonstration

## Documentation
- Architecture notes: `docs/ARCHITECTURE.md`
- Additional project notes: `docs/README.md`

## Security
- Do not commit `.env`
- Use `.env.example` only as a template
- Rotate keys if accidentally exposed during development

## Author
Yash Sharma
