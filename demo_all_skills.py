"""Demo: Using all 3 skills for Terraform, GitHub, and Deployment."""
import asyncio, os, sys, json

sys.path.insert(0, r"C:\Users\mk220\Documents\skills\terraform-infrastructure")
import skill; TerraformSkill = skill.TerraformSkill; del skill; del sys.modules["skill"]; sys.path.pop(0)

sys.path.insert(0, r"C:\Users\mk220\Documents\skills\github-integration")
import skill; GitHubSkill = skill.GitHubSkill; del skill; del sys.modules["skill"]; sys.path.pop(0)

sys.path.insert(0, r"C:\Users\mk220\Documents\skills\github-actions-deployment")
import skill; DeploymentSkill = skill.DeploymentSkill; del skill; del sys.modules["skill"]; sys.path.pop(0)

TOKEN = os.environ["GITHUB_TOKEN"]
OWNER = "dr-r-manikandan"
REPO  = "task-tracker-app"
TF_DIR = r"C:\Users\mk220\Downloads\task-tracker-app\infrastructure"

async def run(name, skill_cls, op, params=None, auth=None, config=None):
    payload = {
        "operation": op,
        "params": params or {},
        "auth": auth or {},
        "config": config or {"request_id": f"demo-{name}"},
    }
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    result = await skill_cls(payload).execute()
    print(json.dumps(result, indent=2))
    return result

async def main():
    print("\n>>> DEMO: 3 SKILLS FOR TERRAFORM, GITHUB & DEPLOYMENT\n")

    # ─── SKILL 1: Terraform Infrastructure ───────────────────────
    await run("Terraform: validate scripts", TerraformSkill, "validate",
              {"check_format": True}, config={"working_directory": TF_DIR})

    await run("Terraform: format check", TerraformSkill, "format",
              {}, config={"working_directory": TF_DIR})

    r = await run("Terraform: generate plan", TerraformSkill, "plan",
                  {"working_directory": TF_DIR},
                  config={"working_directory": TF_DIR, "variables": {"location": "eastus"}})

    plan_id = r["data"]["plan_id"] if r["success"] else None

    if plan_id:
        await run("Terraform: analyze plan", TerraformSkill, "analyze_plan",
                  {"plan_id": plan_id, "working_directory": TF_DIR})

    await run("Terraform: read state", TerraformSkill, "state_read",
              {"working_directory": TF_DIR})

    await run("Terraform: verify infra", TerraformSkill, "verify_infrastructure",
              {"working_directory": TF_DIR})

    # ─── SKILL 2: GitHub Integration ────────────────────────────
    auth = {"token": TOKEN}
    gh_params = {"owner": OWNER, "repo": REPO}

    await run("GitHub: get repo info", GitHubSkill, "get_repository",
              gh_params, auth=auth)

    await run("GitHub: detect changes on main", GitHubSkill, "detect_changes",
              {**gh_params, "ref": "main"}, auth=auth)

    # ─── SKILL 3: GitHub Actions Deployment ─────────────────────
    r = await run("Deploy: trigger workflow", DeploymentSkill, "trigger_deployment",
                  {**gh_params, "workflow_filename": "deploy.yml", "ref": "main"},
                  auth=auth)

    run_id = r["data"]["run_id"] if r["success"] else None
    if run_id:
        print(f"\n  >> Deploy triggered — run #{run_id}")

        await run("Deploy: workflow status", DeploymentSkill, "workflow_status",
                  {**gh_params, "run_id": run_id}, auth=auth)

        await run("Deploy: monitor workflow", DeploymentSkill, "monitor_workflow",
                  {**gh_params, "run_id": run_id}, auth=auth)

        await run("Deploy: deployment summary", DeploymentSkill, "deployment_summary",
                  {**gh_params, "run_id": run_id}, auth=auth)

    print(f"\n{'='*60}")
    print("  DEMO COMPLETE — all 3 skills demonstrated")
    print(f"{'='*60}")

asyncio.run(main())
