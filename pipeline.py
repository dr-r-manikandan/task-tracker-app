"""Pipeline: change -> detect -> infra check -> deploy"""
import asyncio, sys, subprocess, json, aiohttp

TOKEN = "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"
OWNER = "dr-r-manikandan"
REPO  = "task-tracker-app"
TF_DIR = r"C:\Users\mk220\Downloads\task-tracker-app\infrastructure"

def run(script, *args):
    cmd = [sys.executable, script, *args]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.stdout:
        print(r.stdout)
    if r.stderr:
        for line in r.stderr.splitlines()[:10]:
            print("  !", line)
    return r

async def main():
    print(f"\n{'='*60}")
    print("  PIPELINE: Code Change -> Detect -> Infra Check -> Deploy")
    print(f"{'='*60}")

    # STEP 1: Get latest commit SHA
    print("  " + "-"*56)
    print("  STEP 1: Get latest commit from GitHub")
    print("  " + "-"*56)
    async with aiohttp.ClientSession() as s:
        async with s.get(f"https://api.github.com/repos/{OWNER}/{REPO}/commits?per_page=1",
                         headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github.v3+json"}) as resp:
            commits = await resp.json()
    sha = commits[0]["sha"] if isinstance(commits, list) and commits else "main"
    msg = commits[0]["commit"]["message"] if sha != "main" else "N/A"
    print(f"  SHA: {sha}")
    print(f"  MSG: {msg}")

    print()
    print("  " + "-"*56)
    print("  STEP 2: Detect changes (github-integration skill)")
    print("  " + "-"*56)
    r = run("pipeline_detect.py", TOKEN, OWNER, REPO, sha)

    categories = set()
    for line in r.stdout.splitlines():
        if line.startswith("CAT:"):
            categories.add(line[4:])
    print(f"  Categories changed: {categories or 'N/A'}")

    print()
    print("  " + "-"*56)
    print("  STEP 3: Infrastructure check (terraform-infrastructure skill)")
    print("  " + "-"*56)
    has_tf = any("terraform" in c.lower() for c in categories)
    if has_tf:
        print("  Terraform files changed -> running validate + plan")
        run("pipeline_infra.py", TF_DIR)
    else:
        print("  No Terraform changes -> skipping Step 3")

    print()
    print("  " + "-"*56)
    print("  STEP 4: Deploy (github-actions-deployment skill)")
    print("  " + "-"*56)
    r = run("pipeline_deploy.py", TOKEN, OWNER, REPO)
    result = {}
    for line in r.stdout.splitlines():
        try:
            result = json.loads(line)
        except json.JSONDecodeError:
            pass
    ok = "[OK]" if result.get("success") else "[FAIL]"
    print(f"  {ok} Deployment triggered")
    print(f"  Result: {json.dumps(result, indent=2)}")

    # ─── Done ───────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  PIPELINE COMPLETE")
    print(f"  Steps: Get commit -> Detect -> {'Infra -> ' if has_tf else 'Skip Infra -> '}Deploy")
    print(f"  View: https://github.com/{OWNER}/{REPO}/actions")
    print(f"{'='*60}")

asyncio.run(main())
