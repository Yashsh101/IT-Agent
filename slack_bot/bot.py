import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])
AGENT_URL = os.getenv("AGENT_URL", "http://localhost:8000")


@app.message("it-agent")
def handle_it_request(message, say):
    task = message["text"].replace("it-agent", "").strip()
    if not task:
        say("Please provide a task. Example: `it-agent reset password for john@company.com`")
        return

    say(f":robot_face: Running task: _{task}_\n_This may take 30-60 seconds..._")

    try:
        response = requests.post(f"{AGENT_URL}/run-task", json={"task": task}, timeout=120)
        result = response.json()

        if result["status"] == "success":
            say(f":white_check_mark: *Task completed*\n{result['result']}")
        else:
            say(f":x: *Task failed*\n{result['result']}")
    except Exception as e:
        say(f":warning: Could not reach the agent: {str(e)}")


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
