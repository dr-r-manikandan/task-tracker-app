"""Skill 2: GitHub Integration — repo info, detect changes"""
import asyncio, sys, json
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\github-integration")
from skill import GitHubSkill

TOKEN = "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"
OWNER = "dr-r-manikandan"
REPO  = "task-tracker-app"

async def run(op, params=None, label=""):
    payload = {
        "operation": op,
        "auth": {"token": TOKEN},
        "params": params or {},
        "config": {"request_id": f"demo-{op}"}
    }
    r = await GitHubSkill(payload).execute()
    print(f"\n{'='*50}\n  {label or op}\n{'='*50}")
    print(json.dumps(r, indent=2))
    return r

async def main():
    print("\n*** SKILL 2: GITHUB INTEGRATION ***\n")
    await run("get_repository", {"owner": OWNER, "repo": REPO}, label="2a. Get repository info")
    await run("list_pull_requests", {"owner": OWNER, "repo": REPO}, label="2b. List open pull requests")
    await run("monitor_event", {"event_type": "push",
                                "payload": {"ref": "refs/heads/main",
                                            "repository": {"full_name": f"{OWNER}/{REPO}"},
                                            "commits": [{"id": "abc123", "message": "demo"}]}},
              label="2c. Simulate push event")

    print(f"\n{'='*50}\n  GITHUB DEMO COMPLETE\n{'='*50}")

asyncio.run(main())
