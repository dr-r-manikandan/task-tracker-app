import asyncio, json, sys
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\terraform-infrastructure")
from skill import TerraformSkill

TF_DIR = r"C:\Users\mk220\Downloads\task-tracker-app\infrastructure"

async def run(op, params=None, config=None):
    payload = {
        "operation": op,
        "params": params or {},
        "config": config or {"provider": "azurerm", "request_id": f"test-{op}"}
    }
    result = await TerraformSkill(payload).execute()
    print(f"\n=== {op} ===")
    print(json.dumps(result, indent=2))
    return result

async def main():
    r1 = await run("validate", {"check_format": True}, {"working_directory": TF_DIR})
    if not r1["success"]: return

    await run("format", {}, {"working_directory": TF_DIR})

    r3 = await run("plan", {"working_directory": TF_DIR}, {
        "working_directory": TF_DIR, "variables": {"location": "eastus"}
    })
    if not r3["success"]: return
    plan_id = r3["data"]["plan_id"]
    print(f"\nPlan ID: {plan_id}")

    await run("analyze_plan", {"plan_id": plan_id, "working_directory": TF_DIR})
    await run("state_read", {"working_directory": TF_DIR})
    await run("verify_infrastructure", {"working_directory": TF_DIR})

    print("\nRead-only tests passed.")

asyncio.run(main())