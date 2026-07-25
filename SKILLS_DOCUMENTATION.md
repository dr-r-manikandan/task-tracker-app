# Three Reusable Skills — Terraform, GitHub Integration & GitHub Actions Deployment

## Overview

Three generic, reusable Python skills that work together to manage the full lifecycle of a cloud-hosted application:

| Skill | Purpose | Reusable because... |
|-------|---------|-------------------|
| **terraform-infrastructure** | Validate, plan, apply, and verify cloud infrastructure via Terraform | Takes `working_directory`, `provider`, `variables` as params — works with any Terraform project |
| **github-integration** | Read repos, classify commits, manage PRs, trigger workflows via GitHub API | Takes `owner`, `repo`, `token` as params — works with any GitHub repository |
| **github-actions-deployment** | Trigger, monitor, summarize, and rollback deployments via GitHub Actions | Takes `owner`, `repo`, `workflow_filename`, `ref`, `environment` — works with any GitHub Actions workflow |

All three live at `C:\Users\mk220\Documents\skills\` and are independent of each other (except `github-actions-deployment` composes `github-integration` internally).

---

## How the Pipeline Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    pipeline.py (orchestrator)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STEP 1  │  Call GitHub API (public) to get latest commit SHA    │
│          │  e.g. 3352163f614e3704324230dbff3fbb46d1841e39        │
│                                                                  │
│  STEP 2  │  github-integration skill — detect_changes            │
│          │  Classifies every file in the commit:                 │
│          │    - application_code  → src/task-tracker.jsx         │
│          │    - terraform          → infrastructure/main.tf      │
│          │    - other              → *.tfstate backups           │
│                                                                  │
│  STEP 3  │  terraform-infrastructure skill — only if terraform   │
│          │  files changed in step 2:                             │
│          │    - validate: checks syntax + formatting             │
│          │    - plan: generates execution plan, checks for       │
│          │      destructive changes (destroying resources)       │
│          │    - (apply: would deploy infra — requires review)    │
│                                                                  │
│  STEP 4  │  github-actions-deployment skill — trigger deploy     │
│          │  Calls trigger_workflow on deploy.yml which:          │
│          │    - runs npm ci && npm run build                     │
│          │    - builds Docker image, pushes to ACR               │
│          │    - runs az containerapp update → live on Azure      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

Each step runs as a **separate Python subprocess** so the three skills never conflict (they all have the same module name `skill.py`).

### Decision Logic

```
                     ┌─────────────┐
                     │  New commit  │
                     └──────┬──────┘
                            │
                     ┌──────▼──────┐
                     │  Detect     │
                     │  changes    │  ← github-integration
                     └──────┬──────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
     ┌────────▼────────┐        ┌─────────▼────────┐
     │  Terraform      │        │  App code only    │
     │  files changed  │        │  (no infra)       │
     └────────┬────────┘        └─────────┬────────┘
              │                           │
     ┌────────▼────────┐                 │
     │  validate +     │                 │
     │  plan (infra)   │  ← terraform-   │
     │  check for      │    infrastructure│
     │  destruction    │                 │
     └────────┬────────┘                 │
              │                           │
              └──────────┬───────────────┘
                         │
                  ┌──────▼──────┐
                  │  Trigger    │
                  │  deploy.yml │  ← github-actions-deployment
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │  Live on    │
                  │  Azure      │
                  └─────────────┘
```

---

## Applications

### Task Tracker App (demo project)
- **React + Vite** frontend, hosted on **Azure Container Apps**
- URL: https://ca-tasktracker.livelyisland-6f5b3dbf.westeurope.azurecontainerapps.io
- Infra managed via Terraform (`infrastructure/` directory)
- Deployment via `.github/workflows/deploy.yml` (GitHub Actions)

### The skills are NOT tied to this app
Changing 3 variables makes them work for any project:

```python
OWNER = "any-github-org"
REPO  = "any-repo"
TF_DIR = r"path\to\terraform"
```

---

## How to Run

### Prerequisites
- Python 3.12+
- Terraform CLI installed and on PATH
- Azure CLI logged in (for Terraform to authenticate)
- `pip install aiohttp`

### 1. Set your GitHub token
```powershell
$env:GITHUB_TOKEN = "github_pat_..."
```

### 2. Run the full pipeline
```powershell
cd C:\Users\mk220\Downloads\task-tracker-app
python pipeline.py
```

### 3. Run individual skill demos
```powershell
python demo_terraform.py    # Skill 1: validate, plan, state, verify
python demo_github.py       # Skill 2: repo info, list PRs, simulate event
python demo_deploy.py       # Skill 3: trigger workflow on GitHub
```

### 4. Run all tests (proves skills are solid)
```powershell
cd C:\Users\mk220\Documents\skills\github-integration
python -m pytest tests/ -q     # 52 tests

cd C:\Users\mk220\Documents\skills\terraform-infrastructure
python -m pytest tests/ -q     # 20 tests

cd C:\Users\mk220\Documents\skills\github-actions-deployment
python -m pytest tests/ -q     # 19 tests
```

**Total: 91 tests, all passing.**

---

## What Each Skill's Tests Prove

| Skill | Tests | What they verify |
|-------|-------|-----------------|
| **github-integration** | 52 | Auth, repo queries, commit analysis, PR CRUD, workflow trigger/monitor, event normalization, input validation, error handling |
| **terraform-infrastructure** | 20 | Syntax validation, format checking, plan generation, plan analysis, state read, drift detection, safety guardrails (plan-then-apply, destroy confirmation) |
| **github-actions-deployment** | 19 | Deployment trigger, run correlation, polling loop, status checks, log download, rollback dispatch, failure parsing, summary reports |

---

## Architecture of Each Skill

All three follow the same pattern:

```
skill/
├── skill.py              ← Main entry point (one class)
├── operations/           ← One handler per operation
│   ├── validate_op.py
│   ├── plan_op.py
│   └── ...
├── schemas/
│   ├── input.schema.json  ← JSON Schema for input validation
│   └── output.schema.json ← Consistent output structure
├── validation/            ← Input validator
├── log_utils/             ← Structured JSON logging
├── retry/                 ← Retry with exponential backoff
├── tests/                 ← pytest test suite
├── SKILL.md               ← Full documentation
└── metadata.yaml          ← Version, dependencies, category
```

Every operation receives all parameters at runtime in a `payload` dict:

```python
payload = {
    "operation": "detect_changes",      # which operation
    "auth": {"token": "ghp_..."},       # credentials
    "params": {"owner": "...", ...},    # operation-specific inputs
    "config": {"request_id": "..."}     # global settings
}
result = await GitHubSkill(payload).execute()
```

Output is always structured the same way:

```json
{
  "success": true/false,
  "operation": "detect_changes",
  "data": { ... },
  "error": { "code": "...", "message": "..." },
  "meta": { "duration_ms": 1234, ... }
}
```

---

## Key Safety Features

| Skill | Safety |
|-------|--------|
| **terraform-infrastructure** | Plan-then-apply separation. Destroy requires explicit `confirm_destroy: true`. Destructive changes surfaced before apply. State locks never force-unlocked automatically. |
| **github-integration** | Credentials never logged (first 4 + last 4 chars only). Rate limit handling. Full pagination support. |
| **github-actions-deployment** | Rollback never automatic — always caller-initiated. Run correlation via UUID. Polling timeout prevents infinite loops. |
