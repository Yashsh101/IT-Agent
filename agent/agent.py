import asyncio
import logging
import logging.handlers
import os
from datetime import datetime

from dotenv import load_dotenv
from browser_use import Agent, Browser, BrowserProfile
from browser_use.llm.anthropic.chat import ChatAnthropic

load_dotenv()

os.makedirs("agent/logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        "agent/logs/production.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(file_handler)

logger.propagate = False

PANEL_URL = os.getenv("ADMIN_PANEL_URL", "http://localhost:5000")

SYSTEM_PROMPT = f"""You are an IT administrator agent. You control a real browser to complete IT support tasks on the admin panel at {PANEL_URL}.

PAGES:
- {PANEL_URL}/users — create users, reset passwords, toggle account status
- {PANEL_URL}/licenses — assign licenses to users
- {PANEL_URL}/audit — view action history

HOW TO COMPLETE EVERY TASK:
1. Navigate to the correct page by clicking the navbar link.
2. Find the correct form section by reading the heading.
3. Fill each field using the visible label text to identify it.
4. Click the submit button — confirm it says the right action before clicking.
5. Read the flash message at the top of the page (green = success, red = error).
6. Report exactly what the flash message said.

CONDITIONAL TASKS:
- "check if user exists then..." -> go to /users, scan the All Users table for that email.
- If found: proceed to the next action.
- If not found: create the user first, confirm creation flash, then do the follow-up action.
- Always confirm each step before moving to the next.

STRICT RULES:
- Never submit forms via direct URL — always use the visible form UI.
- Never assume success — always read and report the flash message.
- If you see an error flash, report it exactly and stop.
- Complete every step of multi-step tasks sequentially.
"""


async def run_it_task(task: str) -> dict:
    """Execute a natural-language IT task using browser automation."""
    logger.info("=== TASK START ===")
    logger.info(f"Task: {task}")
    start = datetime.now()

    browser = None
    try:
        browser = Browser(
            browser_profile=BrowserProfile(
                headless=False,
                disable_security=True,
            )
        )
        logger.info("Browser initialized")

        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0,
            max_tokens=4096,
        )
        logger.info("LLM initialized — Claude 3.5 Sonnet")

        agent = Agent(
            task=f"{SYSTEM_PROMPT}\n\n---\nIT SUPPORT REQUEST: {task}",
            llm=llm,
            browser=browser,
            max_actions_per_step=8,
        )
        logger.info("Agent created — starting browser navigation")

        result = await agent.run(max_steps=20)

        duration = (datetime.now() - start).seconds
        logger.info(f"Task completed successfully in {duration}s")
        logger.info(f"Result: {str(result)[:200]}...")
        logger.info("=== TASK END (SUCCESS) ===\n")

        return {
            "status": "success",
            "result": str(result),
            "task": task,
            "duration_seconds": duration,
        }

    except asyncio.TimeoutError:
        duration = (datetime.now() - start).seconds
        error_msg = "Task timeout — browser navigation took too long"
        logger.error(f"TIMEOUT: {error_msg}")
        logger.error(f"=== TASK END (TIMEOUT after {duration}s) ===\n")
        return {
            "status": "error",
            "result": error_msg,
            "task": task,
            "duration_seconds": duration,
            "error_type": "timeout",
        }

    except Exception as e:
        duration = (datetime.now() - start).seconds
        error_type = type(e).__name__
        error_msg = str(e)
        logger.error(f"EXCEPTION [{error_type}]: {error_msg}", exc_info=True)
        logger.error("=== TASK END (ERROR) ===\n")
        return {
            "status": "error",
            "result": f"{error_type}: {error_msg}",
            "task": task,
            "duration_seconds": duration,
            "error_type": error_type,
        }

    finally:
        if browser:
            try:
                await browser.close()
                logger.info("Browser closed cleanly")
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")


if __name__ == "__main__":
    result = asyncio.run(run_it_task("Reset the password for john@company.com"))
    print(f"\nStatus: {result['status']}")
    print(f"Result: {result['result']}")