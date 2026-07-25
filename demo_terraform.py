"""Skill 1: Terraform Infrastructure — validate, plan, analyze, verify"""
import asyncio, sys, json
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\terraform-infrastructure")
from skill import TerraformSkill

TF_DIR = r"C:\Users\mk220\Downloads\task-tracker-app\infrastructure"

async def run(op, params=None, config=None, label=""):
    payload = {
        "operation": op, "params": params or {},
        "config": config or {"working_directory": TF_DIR, "request_id": f"demo-{op}"}
    }
    r = await TerraformSkill(payload).execute()
    print(f"\n{'='*50}\n  {label or op}\n{'='*50}")
    print(json.dumps(r, indent=2))
    return r

async def main():
    print("\n*** SKILL 1: TERRAFORM INFRASTRUCTURE ***\n")

    # validate Terraform scripts
    await run("validate", {"check_format": True}, label="1a. Validate Terraform scripts")

    # fmt check
    await run("format", {}, label="1b. Format check")

    # generate a plan (read-only)
    r = await run("plan", {"working_directory": TF_DIR},
                  {"working_directory": TF_DIR, "variables": {"location": "eastus"}},
                  label="1c. Generate Terraform plan")

    if r.get("success"):
        pid = r["data"]["plan_id"]
        # analyze the plan
        await run("analyze_plan", {"plan_id": pid, "working_directory": TF_DIR}, label="1d. Analyze plan")
        # read state
        await run("state_read", {"working_directory": TF_DIR}, label="1e. Read Terraform state")
        # verify no drift
        await run("verify_infrastructure", {"working_directory": TF_DIR}, label="1f. Verify infrastructure")

    print(f"\n{'='*50}\n  TERRAFORM DEMO COMPLETE\n{'='*50}")

asyncio.run(main())
