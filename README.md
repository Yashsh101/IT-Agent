# IT-Agent

> AI agent that accepts natural language IT support requests and completes them by navigating a real browser — no DOM shortcuts, no API cheats.

## Demo

[View a 2-minute walkthrough here]

## What it does

The IT-Agent is an AI-powered automation system that:
- Takes natural language IT support requests (e.g., "reset password for john@company.com")
- Opens a real Chromium browser using browser-use 0.12.6 and Claude 3.5 Sonnet
- Navigates the IT admin panel, reads form labels, fills fields, and clicks buttons like a human would
- Handles complex multi-step conditional logic: "check if user exists → create if not → assign license"
- Returns a structured result showing exactly what was completed

## Architecture

```
Natural Language Request
      │
      ├─ FastAPI Server (:8000)
      │
      ├─ browser-use Agent (Claude 3.5 Sonnet)
      │
      └─ Real Chromium Browser
             │
             └─ Flask Admin Panel (:5000)
                    ├─ /users       (create, reset password, toggle status)
                    ├─ /licenses    (assign licenses)
                    └─ /audit       (action history)

Side: Slack Bot (optional) → FastAPI → Agent
```

## Project structure

```
IT-Agent/
├── admin_panel/
│   ├── app.py                 # Flask admin panel (5 routes, in-memory data)
│   └── templates/
│       ├── base.html          # Layout + navbar
│       ├── dashboard.html     # Statistics
│       ├── users.html         # User management
│       ├── licenses.html      # License management
│       └── audit.html         # Action history
├── agent/
│   ├── __init__.py            # Module exports
│   ├── agent.py               # browser-use agent (core)
│   └── server.py              # FastAPI wrapper
├── slack_bot/
│   ├── __init__.py
│   └── bot.py                 # Slack Bot integration
├── test_agent.py              # 5 test scenarios
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git configuration
└── README.md                  # This file
```

## Setup

### 1. Clone and install
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the services

**Terminal 1: Flask Admin Panel**
```bash
python admin_panel/app.py
# Running on http://127.0.0.1:5000
```

**Terminal 2: FastAPI Agent Server**
```bash
python agent/server.py
# Uvicorn running on http://0.0.0.0:8000
```

**Terminal 3: Run test suite**
```bash
python test_agent.py
```

## Running

### 4. Submit IT tasks via API

```bash
# Example 1: Reset password
curl -X POST http://localhost:8000/run-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Reset the password for john@company.com"}'

# Example 2: Create new user
curl -X POST http://localhost:8000/run-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Create a new user named Alex Kim with email alex@company.com and role Developer"}'

# Example 3: Assign license
curl -X POST http://localhost:8000/run-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Assign license L005 to emma@company.com"}'

# Example 4: Deactivate user
curl -X POST http://localhost:8000/run-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Deactivate the account for mike@company.com"}'

# Example 5: Conditional multi-step (BONUS)
curl -X POST http://localhost:8000/run-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Check if newuser@company.com exists. If they do not exist, create them with name New User and role Analyst. Then assign license L006 to newuser@company.com."}'
```

## Example tasks with curl commands

All 5 example tasks are shown above in the **Running** section. The test suite runs all of them:

```bash
python test_agent.py
```

Expected output:
```
============================================================
  IT-AGENT TEST SUITE
============================================================

Checking services...
  OK  FastAPI agent server :8000
  OK  Flask admin panel  :5000

Running 5 test scenarios...

[1] Simple — password reset
    Task: Reset the password for john@company.com
    PASS — 8s
    Result: Password reset for John Smith. Temporary password: A1B2C3D4

[2] Simple — create new user
    Task: Create a new user named Alex Kim with email alex@company.com and role Developer
    PASS — 6s
    Result: User alex@company.com created successfully with role Developer

[3] Simple — assign license
    Task: Assign license L005 to emma@company.com
    PASS — 5s
    Result: License L005 assigned to Emma Wilson

[4] Simple — deactivate account
    Task: Deactivate the account for mike@company.com
    PASS — 4s
    Result: User mike@company.com deactivated

[5] BONUS — conditional multi-step (check → create → assign)
    Task: Check if newuser@company.com exists. If they do not exist, create them with name New User and role Analyst. Then assign license L006 to newuser@company.com.
    PASS — 12s
    Result: User created and license assigned

============================================================
  RESULTS
============================================================

  OK  Simple — password reset
  OK  Simple — create new user
  OK  Simple — assign license
  OK  Simple — deactivate account
  OK  BONUS — conditional multi-step (check → create → assign)

  Score: 5/5
  All tests passed — ready to submit!
```

## Key decisions

| Decision | Reason |
|---|---|
| **browser-use over raw Playwright** | Built for LLM agents, handles dynamic content, retries, and action abstractions automatically |
| **headless=False** | Agent actions are visible and auditable — critical for demonstrating reliability and catching issues |
| **System prompt encodes navigation rules** | More reliable than letting the model explore; reduces hallucination; faster task completion |
| **Conditional logic in natural language** | Agent reads the page and decides, no hardcoded branching in Python — more flexible |
| **FastAPI wrapper** | Composable — any trigger (Slack, web UI, CLI) can call the same agent backend |

## Bonus features

### Slack Bot Integration

The `slack_bot/bot.py` module integrates with Slack. When a user mentions the bot:

```
@it-agent-bot reset password for john@company.com
```

The bot will:
1. Submit the task to the FastAPI agent server
2. Wait for the browser to complete the action
3. Post the result back to Slack

To enable: Configure SLACK_BOT_TOKEN and SLACK_APP_TOKEN in .env, then run:

```bash
python slack_bot/bot.py
```

---

**Status:** Production-ready. All imports verified. Browser automation tested.

**Model:** Claude 3.5 Sonnet  
**Browser:** Chromium (playwright-managed)  
**API:** FastAPI + browser-use  
**UI:** Flask with Bootstrap 5
