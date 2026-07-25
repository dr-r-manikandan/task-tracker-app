"""pipeline_infra.py — Step 3: Validate and plan Terraform"""
import asyncio, sys, json
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\terraform-infrastructure")
import skill

TF_DIR = sys.argv[1]

async def main():
    v = await skill.TerraformSkill({
        "operation": "validate", "params": {"check_format": True},
        "config": {"working_directory": TF_DIR, "request_id": "pipe-val"}
    }).execute()
    print("VALIDATE:", json.dumps(v))

    p = await skill.TerraformSkill({
        "operation": "plan", "params": {"working_directory": TF_DIR},
        "config": {"working_directory": TF_DIR, "request_id": "pipe-plan"}
    }).execute()
    print("PLAN:", json.dumps(p))

asyncio.run(main())
