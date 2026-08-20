# Contributing to ACE-Step
Hopefully this will provide a simple, easy to understand guide to making 
safe contributions to the project, happy coding!


## ACE-Step SCM Contribution Scope

ACE-Step SCM is a maintained fork of the original ACE-Step project created
specifically to support **The Muser SCM**.

Contributions to this repository should therefore be evaluated primarily in
the context of compatibility, integration, environment management, and
maintenance required by The Muser SCM.

The broader ACE-Step project supports platforms, environments, and workflows
that are not validated by The Shadow Collective. Where possible, SCM-specific
changes should remain isolated and avoid altering unrelated upstream behavior.

For contributions to the original ACE-Step project itself, including broader
platform support and upstream features, contributors should refer to the
original ACE-Step repository:

https://github.com/ace-step/ACE-Step-1.5


## SCM Development Environment

ACE-Step SCM development should use the dedicated SCM environment provided by
this repository.

The validated SCM environment currently uses:

- Python 3.14
- PyTorch 2.13.0 + CUDA 13.0
- The repository's dedicated `.venv-scm` environment

From the ACE-Step SCM repository root, prepare the development environment with:

```bat
scripts\scm\bootstrap_scm_environment.bat
```

Contributors working on SCM-specific compatibility or integration changes
should use this environment when reproducing issues and validating changes.

Do not assume that the original ACE-Step development environment and the
ACE-Step SCM environment are interchangeable. The SCM dependency stack
contains compatibility work maintained specifically for The Muser SCM.

Changes that affect dependency versions, environment bootstrap, model loading,
hardware detection, or API behavior should also be validated through
The Muser SCM integration whenever practical.


### Upstream Development Instructions

The development instructions below originate from the original ACE-Step
project and are retained for reference when working with inherited upstream
code and workflows.

They are **not the validated setup procedure for ACE-Step SCM**.

For SCM-specific development, compatibility work, and The Muser SCM
integration, use the `.venv-scm` environment and SCM bootstrap procedure
described above.

Commands, Python versions, dependency versions, and platform-specific
instructions in the upstream sections may differ from the environment
validated by The Shadow Collective.


## Why This Matters

The original ACE-Step project supports **many hardware and runtime combinations**.
A change that works perfectly on one setup can unintentionally break another if 
scope is not tightly controlled.

The original ACE-Step project has kind of gone viral, and has thousands 
of users, amateur, semi professional and professional, technical and 
none technical, it is important that Ace-Step has reliable builds to 
maintain user trust and engagement.

Recent PR patterns have shown avoidable regressions, for example:

- Fixes that changed behaviour outside the intended target path
- Hardware-specific assumptions leaking into general code paths
- String / status handling changes that broke downstream logic
- Missing or weak review before merge

The goal here is **not blame**.
The goal is **predictable, low-risk contributions** that maintainers can trust and merge with confidence.

---

## Core Principles for Contributors

### Solve One Problem at a Time
- Keep each PR focused on **a single bug or feature**.
- Do **not** mix refactors, formatting, and behaviour changes unless absolutely required.

### Minimize Blast Radius
- Touch **only** the files and functions required for the fix.
- Avoid “drive-by improvements” in unrelated code.

### Preserve Non-Target Platforms
- If fixing **CUDA behaviour**, do not change **CPU / MPS / XPU** paths unless needed.
- Explicitly state **“non-target platforms unchanged”** in the PR notes — and verify it.

### Prove the Change
- Add or run **targeted checks** for the affected path.
- Include a short **regression checklist** in the PR description.

### Be Explicit About Risk
- Call out edge cases and trade-offs up front.
- If uncertain, say so and ask maintainers or experienced contributors for preferred direction.

Clarity beats confidence.

---
## AI Prompt Guardrails for Multi-Platform Projects

Tell your coding agent explicitly:

- Ask for a proposal and plan before making code changes.
- Make only the **minimum required changes** for the target issue.
- Do **not** refactor unrelated code.
- Do **not** alter non-target hardware/runtime paths unless required.
- If a cross-platform change is necessary, **isolate and justify it explicitly**.
- Preserve existing behaviour and interfaces unless the bug fix requires change.

These guardrails dramatically reduce accidental regressions from broad AI edits.

---

## Recommended AI-Assisted Workflow (Copilot / CodePilot / Codex)

### Step 1: Commit-Scoped Review (First Pass)
Once you feel work is complete, and whatever manual or automated testing passes, commit your work to your local project. Note the commit number, or ask your agent to provide the number for your latest commit.

**Use a different agent to review your work than was used to produce the work**

If you use Claud or OpenAI codex, use your free Copilot tokens in VScode to get a Copilot review. If in doubt, ask your main agent to formulate a prompt for the review agent. It will 'know' what it has worked on and can suggest appropriate focus areas for the review agent.

Ask the agent to review **only your commit diff**, not the whole repo.

Prompt example:

Review commit <sha> only.
Focus on regressions, behaviour changes, and missing tests.
Ignore pre-existing issues outside changed hunks.
Output findings by severity with file/line references.

Fix the issues raised by the review, rerun the review process until only non-breaking trivial issues exist. This may need to be repeated a number of times until the commit is clean, but watch that this does not incorrectly blow scope out beyond what is required for the primary fix.
---

### Step 2: Validate Findings

Classify each finding as:

- **Accept** — real issue introduced or exposed by your change
- **Rebut** — incorrect or out-of-scope concern
- **Pre-existing** — not introduced by this PR (note separately)

---

### Step 3: Apply Minimal Fixes
- Fix **accepted** issues with the **smallest possible patch**.
- Do **not** broaden scope or refactor opportunistically.

---

### Step 4: PR-Scoped Review (Second Pass)

Run review on the **entire PR diff**, but only what changed.

Prompt example:

Review PR diff only (base <base>, head <head>), 
(or alternatively, "treat commit a/b/c... as a whole.")
Prioritize regression risk across hardware paths.
Verify unchanged behaviour on non-target platforms.
Flag only issues in changed code.

---

### Step 5: Write Reviewer Responses

For each reviewer comment:

- Quote the concern
- Respond in one line
- Mark disposition clearly
- Link to fix if applicable

---

## Review / Accept / Rebut / Fix Cycle (Practical Template)

Use this structure in your notes:

Comment: <reviewer concern>
Disposition: Accepted | Rebutted | Pre-existing
Response: <one-line rationale>
Action: <commit / file / line> or No code change

This keeps discussion **objective, fast, and easy to follow**.

---

## PR Description Template (Recommended)

### Summary
- What bug or feature is addressed
- Why this change is needed

### Scope
- Files changed
- What is explicitly **out of scope**

### Risk and Compatibility
- Target platform / path
- Confirmation that **non-target paths are unchanged**
  (or describe exactly what changed and why)

### Regression Checks
- Checks run (manual and/or automated)
- Key scenarios validated

### Reviewer Notes
- Known pre-existing issues not addressed
- Follow-up items (if any)

For an example of a carefully documented pull request, see this
[upstream ACE-Step PR](https://github.com/ace-step/ACE-Step-1.5/pull/309),
which demonstrates the care and rigor encouraged by the original ACE-Step
maintainers before submitting a PR.

If automated reviewers such as CodeRabbit or Copilot identify significant
issues, address those findings and repeat the review process before considering
the contribution ready for submission.

---

Maintainers are balancing **correctness, stability, and review bandwidth**.

PRs that are:
- tightly scoped
- clearly explained
- minimally risky
- easy to reason about

are **much more likely to be reviewed and merged quickly**.

Thanks for helping keep the project stable and enjoyable to work on.
