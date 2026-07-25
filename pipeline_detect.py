"""pipeline_detect.py — Step 2: Detect changes in latest commit"""
import asyncio, sys, json
sys.path.insert(0, r"C:\Users\mk220\Documents\skills\github-integration")
import skill

TOKEN = sys.argv[1]; OWNER = sys.argv[2]; REPO = sys.argv[3]; SHA = sys.argv[4]

async def main():
    r = await skill.GitHubSkill({
        "operation": "detect_changes", "auth": {"token": TOKEN},
        "params": {"owner": OWNER, "repo": REPO, "commit_sha": SHA},
        "config": {"request_id": "pipe-detect"}
    }).execute()
    print(json.dumps(r))
    if r.get("success"):
        seen = set()
        for f in r["data"].get("files", []):
            cat = f.get("classification", "other")
            if cat not in seen:
                seen.add(cat)
                print(f"CAT:{cat}")

asyncio.run(main())
