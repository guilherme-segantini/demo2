# CLAUDE.md

## ⚠️ CRITICAL: SCAFFOLDING FIRST

**Before working on ANY task, check if Issue #15 (Scaffolding) is complete.**

```bash
gh issue view 15
```

- If #15 is **OPEN**: You are the Scaffolding Agent. Work on #15 first.
- If #15 is **CLOSED**: Scaffolding is complete. Proceed to your assigned issue.

**All issues #1-#14 are BLOCKED until #15 is merged to main.**

---

## Quick Reference

| File | Use When... |
|------|-------------|
| `skills/sapui5.md` | Developing SAPUI5/UI5 applications |
| `PRD.md` | Understanding product requirements |
| `PLAN.md` | Reviewing execution plan |

## Project Setup

**Tech Stack:** SAPUI5 1.120+, JavaScript (ES6+), FastAPI, SQLite, LiteLLM

```bash
# Frontend
npm install        # Install dependencies
npm start          # Start dev server (localhost:8080)
npm run build      # Build for production
npm run lint       # Run UI5 linter

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # Start API (localhost:8000)
pytest             # Run tests
```

## For litellm setup with generative AI Hub

- Refer to installation guide at https://docs.litellm.ai/docs/providers/sap

## Code Rules

- Use `sap.ui.define` for all modules—no globals
- Use async loading (`data-sap-ui-async="true"`)
- Use i18n for all user-facing text
- No deprecated APIs (`jQuery.sap.*`, sync loading)
- XML views only

---

## Multi-Agent Development (9 Agents)

This project uses **9 parallel Claude agents** working on isolated branches via Git worktrees.

### ⚠️ Scaffolding Agent Runs First

The Scaffolding Agent (#15) must complete and merge before any other agent starts work.

### Worktree Structure

| Directory | Branch | Agent | Issue(s) |
|-----------|--------|-------|----------|
| `demo2-scaffold/` | `feature/scaffolding` | **Scaffolding** | #15 (FIRST) |
| `demo2/` | `main` | Orchestrator | #13 |
| `demo2-fe1/` | `feature/frontend-dev-1` | Frontend Dev 1 | #1, #7 |
| `demo2-fe2/` | `feature/frontend-dev-2` | Frontend Dev 2 | #2, #8 |
| `demo2-be1/` | `feature/backend-dev-1` | Backend Dev 1 | #3, #9 |
| `demo2-be2/` | `feature/backend-dev-2` | Backend Dev 2 | #4, #10 |
| `demo2-prompt/` | `feature/prompt-engineer` | Prompt Engineer | #5, #11 |
| `demo2-qa/` | `feature/problem-finder` | Problem Finder | #6, #12 |
| `demo2-devops/` | `feature/devops` | DevOps | #14 |

### Execution Order

```
Phase 0: Scaffolding Agent completes #15 and merges to main
    ↓
Phase 1: All 8 agents rebase on main and start their first issue (#1-#6, #13, #14)
    ↓
Phase 2: Agents complete second issues (#7-#12) after first issues merge
```

### Starting an Agent Session

```bash
# STEP 1: Scaffolding Agent (MUST RUN FIRST)
cd /Users/I769068/projects/scaling-productivity/demo2-scaffold && claude
> Work on issue #15

# STEP 2: After #15 is merged, start remaining agents
cd /Users/I769068/projects/scaling-productivity/demo2 && claude          # Orchestrator
cd /Users/I769068/projects/scaling-productivity/demo2-fe1 && claude      # Frontend Dev 1
cd /Users/I769068/projects/scaling-productivity/demo2-fe2 && claude      # Frontend Dev 2
cd /Users/I769068/projects/scaling-productivity/demo2-be1 && claude      # Backend Dev 1
cd /Users/I769068/projects/scaling-productivity/demo2-be2 && claude      # Backend Dev 2
cd /Users/I769068/projects/scaling-productivity/demo2-prompt && claude   # Prompt Engineer
cd /Users/I769068/projects/scaling-productivity/demo2-qa && claude       # Problem Finder
cd /Users/I769068/projects/scaling-productivity/demo2-devops && claude   # DevOps
```

---

## Agent Startup Checklist

When starting a new session:

1. **Check if scaffolding is complete:**
   ```bash
   gh issue view 15
   ```
   - If OPEN and you're in `demo2-scaffold/`: Work on #15
   - If OPEN and you're elsewhere: STOP - wait for #15 to complete
   - If CLOSED: Continue to step 2

2. **Check GitHub auth:** `gh auth status`

3. **Sync with main:**
   ```bash
   git fetch origin main
   git rebase origin/main
   ```

4. **View your issues:**
   ```bash
   gh issue list --label "track-a"     # Frontend agents
   gh issue list --label "track-b"     # Backend agents
   gh issue list --label "track-c"     # Prompt Engineer
   gh issue list --label "qa"          # Problem Finder
   gh issue list --label "integration" # Orchestrator, DevOps
   ```

5. **Pick ONE issue** and add `in-progress` label:
   ```bash
   gh issue edit <number> --add-label "in-progress"
   ```

6. **Do the work** - implement, test, document

7. **Complete the full cycle** (see below)

---

## Task & Issue Tracking

**GitHub Issues is the single source of truth for all task management.**

### ONE TASK AT A TIME RULE

Complete the full cycle for one issue before starting another. Do not work on multiple issues simultaneously.

### Complete Workflow (must follow in order)

1. **Code** - Implement the changes for the issue
2. **Test** - Run verification checklist:
   - [ ] App runs without console errors (`npm start`)
   - [ ] `npm run lint` passes with 0 errors
   - [ ] Backend tests pass (`cd backend && pytest`)
   - [ ] Manual testing of the feature/fix
   - [ ] i18n used for all text
   - [ ] No hardcoded URLs or secrets
3. **Document** - Update CHANGELOG.md with your changes
4. **Commit** - `git commit -m "feat: description. Closes #<number>"`
5. **Push** - `git push origin <branch-name>`
6. **PR** - `gh pr create --base main --title "Description" --body "Closes #<number>"`
7. **Merge** - `gh pr merge <number> --squash`
8. **Next** - Only now pick the next issue

**Do not skip testing.** If tests fail, fix them before committing.

---

## Git Workflow

### Branch Naming
- Branch from up-to-date main
- Format: `<type>/<issue-number>-<short-description>`
- Types: `feature/`, `bugfix/`, `hotfix/`, `chore/`, `docs/`, `refactor/`

### Commit Format
- Format: `<type>: <short description>` (50 chars max)
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Reference issues: `Closes #123`, `Fixes #57`, `Part of #42`

### Syncing with Main

```bash
git fetch origin main
git rebase origin/main
git push origin <branch> --force-with-lease
```

### Creating and Merging PRs

```bash
gh pr create --base main --title "Description" --body "Closes #<number>"
gh pr merge <number> --squash
```

---

## Changelog Management

Maintain `CHANGELOG.md` as a **first-class artifact**.

### When to Update
- After completing a feature or fix
- When deferring or rejecting an approach (document why)
- Before ending a work session

### Format

```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Deferred
- Feature X - Rationale: reason
```

---

## Verification Checklist

Before marking work complete:
- [ ] App runs without console errors
- [ ] `npm run lint` passes with 0 errors
- [ ] Backend `pytest` passes
- [ ] Navigation works correctly
- [ ] i18n used for all text
- [ ] No hardcoded URLs or secrets
- [ ] CHANGELOG.md updated

---

## Issue Dependencies

| Issue | Agent | Blocked By |
|-------|-------|------------|
| #15 | Scaffolding | None (START FIRST) |
| #1 | Frontend Dev 1 | #15 |
| #2 | Frontend Dev 2 | #15 |
| #3 | Backend Dev 1 | #15 |
| #4 | Backend Dev 2 | #15 |
| #5 | Prompt Engineer | #15 |
| #6 | Problem Finder | #15 |
| #7 | Frontend Dev 1 | #15, #1 |
| #8 | Frontend Dev 2 | #15, #2 |
| #9 | Backend Dev 1 | #15, #3, #5 |
| #10 | Backend Dev 2 | #15, #4 |
| #11 | Prompt Engineer | #15, #5 |
| #12 | Problem Finder | #15, #6 |
| #13 | Orchestrator | #15 |
| #14 | DevOps | #15 |

---

## Useful Commands

```bash
git worktree list                    # See all worktrees
gh issue list                        # All open issues
gh issue view <number>               # Issue details
gh pr list                           # Open PRs
gh pr view <number>                  # PR details
gh pr merge <number> --squash        # Merge PR
```

---

## Decisions Made
- 9-agent parallel development with git worktrees
- Scaffolding must complete before other work begins
- One task at a time per agent
- Squash merge for all PRs

## Known Issues
- [Track problems or limitations as discovered]
