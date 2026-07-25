"""pipeline_deploy.py — Step 4: Trigger deployment workflow"""
import asyncio, sys, json
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\github-integration")
import skill

TOKEN = sys.argv[1]; OWNER = sys.argv[2]; REPO = sys.argv[3]

async def main():
    r = await skill.GitHubSkill({
        "operation": "trigger_workflow", "auth": {"token": TOKEN},
        "params": {"owner": OWNER, "repo": REPO, "workflow_filename": "deploy.yml", "ref": "main"},
        "config": {"request_id": "pipe-deploy"}
    }).execute()
    print(json.dumps(r))

asyncio.run(main())
