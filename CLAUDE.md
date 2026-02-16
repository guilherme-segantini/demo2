# CLAUDE.md

## Quick Reference

| File | Use When... |
|------|-------------|
| `skills/sapui5.md` | Developing SAPUI5/UI5 applications |

## Project Setup

**Tech Stack:** SAPUI5 1.120+, JavaScript (ES6+), OData V4 / JSON models

```bash
npm start          # Start dev server
npm run build      # Build for production
npm run lint       # Run UI5 linter
npm test           # Run tests
```

See `skills/sapui5.md` for detailed patterns and structure.

## For litellm setup with generative AI Hub

- Refer to installation guide at https://docs.litellm.ai/docs/providers/sap

## Code Rules

- Use `sap.ui.define` for all modules—no globals
- Use async loading (`data-sap-ui-async="true"`)
- Use i18n for all user-facing text
- No deprecated APIs (`jQuery.sap.*`, sync loading)
- XML views only

---

## Task & Issue Tracking

**GitHub Issues is the single source of truth for all task management.**

Use `gh` CLI commands for tracking—never rely on memory or ad-hoc notes.

### Issue Management

Before doing any work:
- Check `gh auth status` and list open issues first
- Ensure an issue exists for the task—create one if it doesn't

**Creating issues:**
- Use a short, descriptive title
- Include acceptance criteria as checkboxes
- Add technical notes, constraints, or dependencies
- Apply labels: `feature`, `bug`, `chore`, `docs`, `spike`, `blocked`, `ready`

**For bugs, include:**
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### Working on Tasks

**When starting:**
1. Verify the issue exists (`gh issue view <number>`)
2. Add `in-progress` label
3. Create a branch linked to the issue (`feature/#123-description`)

**During work:**
- Add progress comments to the issue
- Reference issue numbers in commits (`Part of #123`)
- Update labels if blocked

### Completing Tasks

**ONE TASK AT A TIME RULE:**
Complete the full cycle for one issue before starting another. Do not work on multiple issues simultaneously.

**Complete workflow (must follow in order):**
1. **Code** - Implement the changes for the issue
2. **Test** - Run verification checklist (see below):
   - [ ] App runs without console errors (`npm start`)
   - [ ] `npm run lint` passes with 0 errors
   - [ ] `npm test` passes (all unit tests)
   - [ ] Manual testing of the feature/fix
   - [ ] i18n used for all text
   - [ ] No hardcoded URLs or secrets
3. **Document** - Update CHANGELOG.md with your changes
4. **Commit** - Commit your work with issue reference: `git commit -m "feat: description. Part of #123"`
5. **Push** - Push your branch to remote: `git push origin <branch-name>`
6. **PR** - Create a pull request: `gh pr create --base main --title "Description" --body "Closes #123"`
7. **Merge** - Merge the PR: `gh pr merge <number> --squash`
8. **Verify** - Issue auto-closes when PR is merged
9. **Next** - Only now pick the next issue from your backlog

**Do not skip testing.** If tests fail, fix them before committing.

**Auto-close keywords in commits/PRs:**
- `Closes #123`
- `Fixes #123`
- `Resolves #123`

### Useful Queries

```bash
gh issue list                      # All open issues
gh issue list --assignee @me       # Your assigned issues
gh issue list --label "priority-high"  # High priority
gh issue list --label "ready"      # Ready to work
gh issue list --label "bug"        # Bugs only
gh issue list --search "keyword"   # Search issues
```

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

### Workflow Preferences
- Use rebase for personal branches, merge for shared branches
- Use `--force-with-lease` after rebasing
- Prefer squash merge for features

### PR Description
Include:
- What the PR does and why
- List of changes made
- Related issue numbers
- Type of change (bug fix, feature, breaking change)
- Testing checklist

---

## Changelog Management

Maintain `CHANGELOG.md` as a **first-class artifact**—not a release note afterthought.

### Purpose
- Record **what** was done and **why**
- Track **what was intentionally deferred** and the rationale
- Enable AI to resume work without reintroducing rejected ideas
- Provide humans a curated, readable history

### Format

Based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/):

```markdown
# Changelog

## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Deferred
- Feature X - Rationale: Not needed for PoC scope (YAGNI)

## [1.0.0] - 2025-01-30

### Added
- Initial feature set
```

### Change Types

| Type | Use For |
|------|---------|
| **Added** | New features |
| **Changed** | Changes in existing functionality |
| **Deprecated** | Soon-to-be removed features |
| **Removed** | Now removed features |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |
| **Deferred** | Intentionally postponed or rejected ideas (with rationale) |

### Guidelines

**Do:**
- Keep `[Unreleased]` section at the top
- Use ISO 8601 date format: `YYYY-MM-DD`
- List newest versions first
- Include rationale for significant decisions
- Record deferred items to prevent revisiting rejected ideas
- Update with each meaningful change, not just at release

**Don't:**
- Dump git logs into the changelog
- Use vague descriptions ("fixed stuff", "updates")
- Omit reasoning behind changes
- Wait until release to write entries

### When to Update
- After completing a feature or fix
- When deferring or rejecting an approach (document why)
- When making architectural decisions
- Before ending a work session (capture context for continuity)

---

## Decisions Made
- [Document decisions as you make them]

## Known Issues
- [Track problems or limitations]

---

## Multi-Agent Development (Git Worktrees)

This project uses **3 parallel Claude agents** working on isolated branches via Git worktrees.

### Worktree Structure

| Directory | Branch | Track | Focus |
|-----------|--------|-------|-------|
| `technologies-trend/` | `main` | Orchestrator | Merge PRs, coordination |
| `track-a/` | `feature/track-a` | Track A | Frontend (SAPUI5) |
| `track-b/` | `feature/track-b` | Track B | Backend (FastAPI) |
| `track-c/` | `feature/track-c` | Track C | AI/Prompts |

### Starting an Agent Session

```bash
# Track A - Frontend Developer
cd /Users/I769068/projects/scaling-productivity/track-a && claude

# Track B - Backend Developer
cd /Users/I769068/projects/scaling-productivity/track-b && claude

# Track C - AI/Prompts Developer
cd /Users/I769068/projects/scaling-productivity/track-c && claude
```

### Agent Startup Checklist

When starting a new session as a track agent:

1. **Read this CLAUDE.md** to understand your role and workflow rules
2. **Check GitHub auth:** `gh auth status`
3. **Sync with main:** `git fetch origin main && git rebase origin/main`
4. **View your backlog:** `gh issue list --label "track-X"` (replace X with a, b, or c)
5. **Pick ONE issue** and add `in-progress` label: `gh issue edit <number> --add-label "in-progress"`
6. **Do the work** - stay in your track's directory (`webapp/`, `backend/`, or `prompts/`)
7. **Test everything** - run `npm start`, `npm run lint`, `npm test` and verify manually
8. **Update CHANGELOG.md** with your changes
9. **Commit with issue reference:** `git commit -m "feat: description. Part of #<number>"`
10. **Push to remote:** `git push origin feature/track-X`
11. **Create a PR:** `gh pr create --base main --title "[Track X] Description" --body "Closes #<number>"`
12. **Merge the PR:** `gh pr merge <number> --squash` (or wait for review if required)
13. **Repeat** - Go back to step 4 and pick the next issue

**Work on one issue at a time. Complete the full cycle before starting another.**

### Agent Responsibilities

**Track A Agent (Frontend):**
- GitHub Issues: #5, #8, #9, #10, #11, #12
- Files: `webapp/**`
- Label filter: `gh issue list --label "track-a"`

**Track B Agent (Backend):**
- GitHub Issues: #2, #3, #4, #13, #14, #15
- Files: `backend/**`
- Label filter: `gh issue list --label "track-b"`

**Track C Agent (AI/Prompts):**
- GitHub Issues: #6, #16, #17, #18
- Files: `prompts/**`
- Label filter: `gh issue list --label "track-c"`

### Workflow Rules

**CRITICAL: One Task at a Time**
- Work on exactly ONE issue per cycle
- Complete the full workflow before picking the next issue
- Never have multiple issues "in progress" simultaneously

**Per-Issue Workflow:**
1. **Check issues first:** `gh issue list --label "track-X"`
2. **Claim ONE task:** Add `in-progress` label before starting
3. **Stay in your lane:** Only modify files in your track's directory
4. **Implement:** Write code, reference issue numbers in commits (`Part of #8`)
5. **Test thoroughly:** Run `npm start`, `npm run lint`, `npm test` - all must pass
6. **Update changelog:** Record changes in CHANGELOG.md
7. **Commit & push:** `git commit` → `git push`
8. **Create PR:** Target `main` branch with `gh pr create`
9. **Merge the PR:** Use squash merge with `gh pr merge <number> --squash`
10. **Repeat:** Go back to step 1 for the next issue

### Syncing with Main

```bash
# Pull latest from main (do this before starting new work)
git fetch origin main
git rebase origin/main

# Push your branch
git push origin feature/track-a --force-with-lease
```

### Creating and Merging a PR

```bash
# Create the PR
gh pr create --base main --title "[Track A] Implement RadarView" --body "Closes #9"

# Merge the PR (squash merge)
gh pr merge <number> --squash
```

### Useful Commands

```bash
git worktree list                    # See all worktrees
gh issue list --label "track-a"      # Your backlog
gh pr list                           # Open PRs
gh pr view <number>                  # PR details
```
