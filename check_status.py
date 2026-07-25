import asyncio, aiohttp, json, sys
TOKEN = __import__("os").environ.get("GITHUB_TOKEN", "")

async def main():
    async with aiohttp.ClientSession() as s:
        url = "https://api.github.com/repos/dr-r-manikandan/task-tracker-app/actions/runs?per_page=1"
        async with s.get(url, headers={"Authorization": f"Bearer {TOKEN}"}) as r:
            data = await r.json()
            print(json.dumps(data, indent=2)[:500])
            run = data["workflow_runs"][0]
            print(f"Run #{run['id']}: status={run['status']}, conclusion={run['conclusion']}")
            print(f"URL: {run['html_url']}")
        # Get jobs
        jurl = run["jobs_url"]
        async with s.get(jurl, headers={"Authorization": f"Bearer {TOKEN}"}) as jr:
            jobs = await jr.json()
            for job in jobs.get("jobs", []):
                print(f"  Job: {job['name']} — {job['conclusion']}")
                for step in job.get("steps", []):
                    print(f"    Step: {step['name']} — {step['conclusion']}")
asyncio.run(main())
