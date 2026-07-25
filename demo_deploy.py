"""Skill 3: GitHub Actions Deployment — trigger workflow via GitHub API"""
import asyncio, sys, json
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\github-integration")
import skill as gh

TOKEN = "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"
OWNER = "dr-r-manikandan"
REPO  = "task-tracker-app"

async def main():
    print("\n*** SKILL 3: GITHUB ACTIONS DEPLOYMENT ***\n")

    r = await gh.GitHubSkill({
        "operation": "trigger_workflow", "auth": {"token": TOKEN},
        "params": {"owner": OWNER, "repo": REPO, "workflow_filename": "deploy.yml", "ref": "main"},
        "config": {"request_id": "demo-deploy"}
    }).execute()

    print("3a. Trigger deployment workflow:")
    print(json.dumps(r, indent=2))

    print("""
3b. The github-actions-deployment skill builds on this with:
    - trigger_deployment   (trigger + auto-resolve run_id)
    - workflow_status      (one-shot status check)
    - monitor_workflow     (poll until completion)
    - deployment_summary   (structured report with failures)
    - download_logs        (fetch logs per job)
    - cancel_workflow      (cancel in-progress run)

    Usage: await DeploymentSkill({...}).execute()
    """)
    print(f"  View run at: https://github.com/{OWNER}/{REPO}/actions\n")

asyncio.run(main())
