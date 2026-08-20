# AGENTS.md — ACE-Step SCM

This file provides instructions for AI coding agents working on
**ACE-Step SCM**.

ACE-Step SCM is a maintained fork of the original ACE-Step project created
specifically to support **The Muser SCM**.

The primary goal of work in this repository is to maintain a known, tested,
and reliable ACE-Step backend for The Muser SCM while disturbing unrelated
upstream ACE-Step behavior as little as possible.


## Project Relationship

The relationship between the projects is:

```text
The Muser SCM
    |
    | installs and manages
    v
ACE-Step SCM
    |
    | loads and runs
    v
ACE-Step models

ACE-Step and its models, architecture, research, and original
implementation are upstream work created by the ACE-Step developers and
contributors.

ACE-Step SCM contains compatibility, integration, environment-management,
and maintenance changes required by The Muser SCM.

Agents must not treat ACE-Step SCM as a replacement for the original ACE-Step
project or assume that SCM-specific requirements apply to upstream ACE-Step.


## Primary Agent Rule

When making changes to ACE-Step SCM:
> Make the smallest change necessary to solve the specific SCM problem while
> preserving unrelated upstream behavior.

Do not perform opportunistic refactors, dependency upgrades, formatting
changes, architecture changes, or cleanup outside the scope of the requested
work.

Changes affecting non-target hardware, operating systems, runtime paths, or
upstream functionality must not be made unless they are genuinely required
for the SCM task.


## Validated SCM Environment

The validated ACE-Step SCM development environment currently uses:

- **Operating system:** Windows 11
- **Python:** 3.14
- **PyTorch:** 2.13.0 + CUDA 13.0
- **GPU:** NVIDIA GeForce RTX 5060 Ti
- **VRAM:** 16 GB
- **Environment:** `.venv-scm`

Agents working on SCM-specific changes should use the repository's dedicated
SCM environment rather than creating or substituting an unrelated Python
environment.

The SCM environment is prepared from the repository root with:

```bat
scripts\scm\bootstrap_scm_environment.bat
```

Do not replace the SCM bootstrap procedure with the original upstream
`uv sync` workflow when validating SCM-specific changes.

The original ACE-Step project supports additional operating systems, hardware
backends, Python environments, and development workflows. Those upstream
configurations are outside The Shadow Collective's validated SCM environment
unless explicitly tested as part of the task.

Do not infer that an SCM compatibility change is appropriate for other
upstream platforms merely because it works in the validated SCM environment.
```

## SCM Development Priorities

Work in ACE-Step SCM should primarily support the requirements of
**The Muser SCM**.

Typical SCM work includes:

- Python and dependency compatibility required by the validated SCM stack
- Compatibility fixes for libraries used by ACE-Step SCM
- SCM environment bootstrap and installation reliability
- ACE-Step REST API integration required by The Muser SCM
- GPU detection and hardware-aware configuration
- Model loading and runtime compatibility
- Startup, shutdown, and service-management behavior used by The Muser SCM
- Fixes required to keep the validated SCM generation workflow operational

The following are not automatically SCM development goals:

- General modernization of unrelated upstream ACE-Step code
- Refactoring code solely for style or architectural preference
- Expanding support to hardware or operating systems we cannot validate
- Replacing upstream systems that already function for the SCM workflow
- Changing ACE-Step model architecture or behavior without a demonstrated
  requirement from The Muser SCM
- Adopting new dependency versions simply because newer versions exist

When a problem can be solved either by a narrowly scoped compatibility patch
or by changing a larger portion of the upstream architecture, prefer the
narrowly scoped solution unless there is a demonstrated reason not to.

If a requested change would significantly alter original ACE-Step behavior,
agents should identify that risk before making the change.


## Validation Requirements

A successful import, dependency installation, or API startup does not by
itself prove that an ACE-Step SCM change is valid.

Validation should match the scope of the change.

For SCM-specific changes, agents should use the following progression where
applicable:

1. Verify that the affected code imports or initializes successfully.
2. Verify that the dedicated `.venv-scm` environment remains functional.
3. Verify that the ACE-Step SCM REST API starts successfully when the change
   affects runtime or API behavior.
4. Verify that the affected model or hardware configuration loads correctly.
5. When generation behavior may be affected, complete an actual music
   generation.
6. When The Muser SCM integration may be affected, validate the workflow
   through The Muser SCM rather than testing ACE-Step SCM only in isolation.

Do not describe a change as fully validated when only a lower-level check has
been completed.

For example:

- Successful installation proves installation, not generation.
- Successful import proves import compatibility, not runtime compatibility.
- Successful API startup proves service startup, not successful inference.
- Successful ACE-Step SCM generation does not necessarily prove that
  The Muser SCM integration remains functional.

Report exactly what was tested and what was not tested.

If validation cannot be completed because the required hardware, model,
environment, or integration is unavailable, state that limitation rather
than assuming the change works.


## Change and Review Rules

Agents working on ACE-Step SCM should keep changes narrow, reviewable, and
easy to validate.

### Before Making Changes

- Identify the specific problem being solved.
- Determine which files and runtime paths are actually involved.
- Check whether the affected code is SCM-specific or inherited upstream code.
- Identify any non-target hardware, operating system, or runtime paths that
  could be affected.
- Prefer understanding the existing implementation before replacing it.

### While Making Changes

- Modify only the files and functions required for the task.
- Do not perform unrelated refactoring or formatting cleanup.
- Preserve existing interfaces unless the requested fix requires a change.
- Keep SCM-specific compatibility logic isolated where practical.
- Do not alter CPU, MPS, XPU, ROCm, or other non-target paths merely to make
  the validated NVIDIA SCM path cleaner.
- Do not remove apparently unused upstream functionality without first
  establishing that it is genuinely unnecessary to the inherited project.

### After Making Changes

- Review the complete diff for unintended changes.
- Confirm that the change remained within the requested scope.
- Run validation appropriate to the affected behavior.
- Check for regressions in adjacent code paths where practical.
- Record any known limitations or untested paths.
- Clearly distinguish pre-existing issues from problems introduced by the
  current change.

### Review Discipline

When using multiple AI coding or review agents, a review agent should examine
the actual change or commit diff rather than broadly rewriting unrelated
parts of the repository.

Review findings should be classified as:

- **Accepted** — a valid issue introduced or exposed by the change
- **Rebutted** — an incorrect or out-of-scope finding
- **Pre-existing** — an issue that existed before the current change

Accepted findings should be fixed with the smallest reasonable patch and
validation should be repeated as necessary.


## Upstream Boundary and Attribution

ACE-Step SCM is derived from the original ACE-Step project.

Agents must preserve the distinction between:

- **ACE-Step** — the original upstream project
- **ACE-Step SCM** — The Shadow Collective's maintained compatibility fork
- **The Muser** — the original Muser project
- **The Muser SCM** — The Shadow Collective's maintained Muser fork

Do not describe original ACE-Step models, architecture, research, or
implementation as work created by The Shadow Collective.

Do not rename upstream ACE-Step models or components merely to apply SCM
branding.

When documentation or code comments discuss an SCM-specific modification,
make the scope of that modification clear without implying that the
underlying upstream component was created by The Shadow Collective.

Preserve existing copyright, license, attribution, and third-party notices.

For original ACE-Step development, documentation, and project direction,
refer to the upstream repository:

https://github.com/ace-step/ACE-Step-1.5


## Source of Truth

When information about the ACE-Step SCM environment conflicts, prefer
evidence from the currently validated SCM implementation over assumptions
based on the original upstream environment.

Use the following order when determining intended SCM behavior:

1. The specific requirements of the current task
2. Working ACE-Step SCM code and SCM-specific scripts
3. The validated `.venv-scm` environment
4. The Muser SCM integration that consumes ACE-Step SCM
5. ACE-Step SCM documentation
6. Original upstream ACE-Step documentation for functionality not modified
   by the SCM fork

Do not change a working SCM configuration solely because upstream
documentation describes a different environment.

Likewise, do not modify unrelated upstream behavior solely to make it conform
to SCM-specific assumptions.

When the implementation, documentation, and observed runtime behavior
disagree, investigate the discrepancy before making changes rather than
assuming that any single source is automatically correct.

If uncertainty remains, preserve the existing working behavior and clearly
report the unresolved discrepancy.
