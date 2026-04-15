"""
IT-Agent Demo Suite — Production Readiness Validation
Runs 5 comprehensive scenarios to validate the agent is production-ready
Usage: python run_demo.py
Requires: Flask panel on :5000 AND FastAPI server on :8000
"""
import requests
import time
import sys

BASE = "http://localhost:8000"
PANEL = "http://localhost:5000"

G = "\033[92m"; R = "\033[91m"; Y = "\033[93m"
B = "\033[94m"; BOLD = "\033[1m"; X = "\033[0m"

TASKS = [
    {
        "label": "Simple — password reset",
        "task": "Reset the password for john@company.com",
        "expect": "success"
    },
    {
        "label": "Simple — create new user",
        "task": "Create a new user named Alex Kim with email alex@company.com and role Developer",
        "expect": "success"
    },
    {
        "label": "Simple — assign license",
        "task": "Assign license L005 to emma@company.com",
        "expect": "success"
    },
    {
        "label": "Simple — deactivate account",
        "task": "Deactivate the account for mike@company.com",
        "expect": "success"
    },
    {
        "label": "BONUS — conditional multi-step (check → create → assign)",
        "task": "Check if newuser@company.com exists. If they do not exist, create them with name New User and role Analyst. Then assign license L006 to newuser@company.com.",
        "expect": "success"
    }
]


def check_services() -> bool:
    print(f"\n{B}{BOLD}Checking services...{X}")
    ok = True
    for name, url in [("FastAPI agent server :8000", f"{BASE}/health"),
                       ("Flask admin panel  :5000", PANEL)]:
        try:
            requests.get(url, timeout=3)
            print(f"  {G}OK{X}  {name}")
        except:
            print(f"  {R}FAIL{X}  {name} — NOT RUNNING")
            ok = False
    return ok


def run_task(i: int, label: str, task: str) -> str:
    print(f"\n{Y}{BOLD}[{i}] {label}{X}")
    print(f"    Task: {task}")
    try:
        r = requests.post(f"{BASE}/run-task",
                          json={"task": task}, timeout=180)
        data = r.json()
        status = data.get("status", "error")
        result_text = data.get("result", "")[:200]
        duration = data.get("duration_seconds", 0)
        icon = f"{G}PASS{X}" if status == "success" else f"{R}FAIL{X}"
        print(f"    {icon} — {duration}s")
        print(f"    Result: {result_text}")
        return status
    except requests.exceptions.Timeout:
        print(f"    {R}TIMEOUT{X}")
        return "timeout"
    except Exception as e:
        print(f"    {R}ERROR: {e}{X}")
        return "error"


def main():
    print(f"\n{B}{BOLD}{'='*55}")
    print(f"  IT-AGENT TEST SUITE")
    print(f"{'='*55}{X}")

    if not check_services():
        print(f"\n{R}Start both services first:{X}")
        print("  Terminal 1: python admin_panel/app.py")
        print("  Terminal 2: python agent/server.py")
        sys.exit(1)

    print(f"\n{BOLD}Running {len(TASKS)} test scenarios...{X}")
    results = []

    for i, t in enumerate(TASKS, 1):
        status = run_task(i, t["label"], t["task"])
        results.append((t["label"], status))
        if i < len(TASKS):
            print(f"    {Y}Waiting 4s before next task...{X}")
            time.sleep(4)

    print(f"\n{B}{BOLD}{'='*55}")
    print(f"  RESULTS")
    print(f"{'='*55}{X}")
    passed = 0
    for label, status in results:
        ok = status == "success"
        if ok: passed += 1
        icon = f"{G}OK{X}" if ok else f"{R}FAIL{X}"
        print(f"  {icon}  {label}")

    print(f"\n  Score: {G if passed==len(TASKS) else Y}{passed}/{len(TASKS)}{X}")
    if passed == len(TASKS):
        print(f"  {G}{BOLD}All tests passed — ready to submit!{X}\n")
    else:
        print(f"  {Y}Fix failing tasks before submitting.{X}\n")


if __name__ == "__main__":
    main()
