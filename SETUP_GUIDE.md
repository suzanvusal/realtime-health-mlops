# Smart Health MLOps — Free Tier Setup Guide

## Cost: $0.00

This version uses **GitHub Models API** (free with your GitHub account) for AI code generation,
and pre-written templates for bulk commits. No Anthropic account or credit card needed.

---

## How It Works

| Commit type | Source | API cost |
|-------------|--------|----------|
| Key feature files (6/day) | GitHub Models API (gpt-4o-mini) | $0.00 |
| Pre-written MLOps templates | Local templates | $0.00 |
| Task/refactor commits | Plan-driven snippets | $0.00 |
| **Total per day** | **20–30 commits** | **$0.00** |

---

## Step 1 — Create an Empty GitHub Repo

Go to https://github.com/new → name it `smart-health-mlops` → **no README, no .gitignore**.

---

## Step 2 — Bootstrap Locally (one time)

```bash
pip install pyyaml requests

# Replace with your repo URL
python3 scripts/bootstrap_repo.py \
  --repo https://github.com/YOUR_USERNAME/smart-health-mlops.git
```

---

## Step 3 — Enable GitHub Models

GitHub Models is already available on most accounts. Check at:
https://github.com/marketplace/models

If you see a "Join waitlist" button, join it — approval is usually instant.

---

## Step 4 — No Extra Secrets Needed!

The workflow uses the built-in `GITHUB_TOKEN` (automatically available in every Action).
**You do not need to add any secrets.** That's it.

> The workflow file already has `permissions: models: read` which grants access to GitHub Models.

---

## Step 5 — Trigger the First Run

1. Go to your repo → **Actions** tab
2. Click **"Daily MLOps Commit Automation (Free Tier)"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch it run (~8–12 minutes for 25 commits)

After that, it runs automatically every day at **9:00 AM UTC**.

---

## Manual Controls

```bash
# Preview day 5 without committing
python3 scripts/run_day.py --day 5 --dry-run

# Run day 5 locally
python3 scripts/run_day.py --day 5 --commits 25
```

---

## GitHub Models Free Tier Limits

| Model | Requests/day | Tokens/min |
|-------|-------------|------------|
| gpt-4o-mini | ~150 | 8,000 |
| gpt-4o | ~10 | 8,000 |

We use `gpt-4o-mini` and make only **6 calls/day** — well within limits.

---

## Differences vs Paid Version

| Feature | Free | Paid (Anthropic) |
|---------|------|-----------------|
| Cost | $0 | ~$1–2/day |
| Commits/day | 20–30 | 50–100 |
| Code quality | Good (gpt-4o-mini) | Excellent (Claude) |
| Setup complexity | Minimal | Requires Anthropic key |
