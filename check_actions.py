"""Check last GitHub Actions run status"""
import asyncio, aiohttp, os, sys
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\github-integration")
import skill

TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = "dr-r-manikandan"
REPO = "task-tracker-app"

async def main():
    # Trigger
    r = await skill.GitHubSkill({
        "operation": "trigger_workflow", "auth": {"token": TOKEN},
        "params": {"owner": OWNER, "repo": REPO, "workflow_filename": "deploy.yml", "ref": "main"},
        "config": {"request_id": "check"}
    }).execute()
    print("Trigger:", r["success"])

    # List runs
    async with aiohttp.ClientSession() as s:
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs?per_page=5&branch=main"
        async with s.get(url, headers={"Authorization": f"Bearer {TOKEN}"}) as resp:
            data = await resp.json()
            for run in data.get("workflow_runs", []):
                print(f"Run #{run['id']}: {run['status']}/{run['conclusion']} — {run['display_title'][:60]}")
            if not data.get("workflow_runs"):
                print("No runs found. API response:", await resp.text()[:300])

asyncio.run(main())
