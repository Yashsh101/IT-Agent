# IT-Agent

AI-driven IT support agent MVP built with FastAPI, Flask admin panel, and browser automation.

## Overview

IT-Agent is a prototype system designed to automate IT support-style workflows using an agent service, a lightweight admin interface, and local automation tooling.

This project was built as an MVP to explore how AI agents can assist with operational support tasks such as workflow execution, request handling, and task orchestration.

## Features

- FastAPI-based agent backend
- Flask admin panel for local control and monitoring
- Environment-based configuration using `.env`
- Demo and verification scripts for local testing
- Modular project structure with separated docs and scripts

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
├── requirements.txt
└── stress_test.py
```

## Tech Stack

- Python
- FastAPI
- Flask
- Uvicorn
- Browser automation tooling

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Yashsh101/IT-Agent.git
cd IT-Agent
```

### 2. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example` and add your local credentials.

## Run Locally

### Start the admin panel

```powershell
python -c "from admin_panel.app import app; app.run(host='127.0.0.1', port=5000, debug=False)"
```

### Start the agent server

```powershell
python -m uvicorn agent.server:app --host 127.0.0.1 --port 8000
```

### Run the demo script

```powershell
python .\scripts\run_demo.py
```

## Current Status

This repository is an MVP submission.

### Working

- Project structure and service separation
- FastAPI service startup
- Flask admin panel startup
- Local environment-based configuration
- Basic demo/testing script flow

### In Progress

- Full end-to-end stabilization of all agent workflows
- Better production readiness
- Improved test coverage and deployment polish

## Known Issues

- Some automation flows may require additional stabilization
- This project is currently optimized for local MVP demonstration rather than production deployment

## Documentation

- Architecture notes: `docs/ARCHITECTURE.md`
- Additional project notes: `docs/README.md`

## Security

- Do not commit `.env`
- Use `.env.example` only as a template
- Rotate keys immediately if they are accidentally exposed

## Future Improvements

- Better error handling and retry logic
- Improved UI/UX in the admin panel
- More reliable end-to-end workflow execution
- Better logging, observability, and deployment support

## Author

Yash Sharma
