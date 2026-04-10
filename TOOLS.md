# Backend Tooling Baseline

## Core
- Runtime: Node.js service stack in this repository.
- Shell: `bash` for local automation and diagnostics.
- VCS: `git` with small, reviewable commits.
- Work orchestration: Paperclip issue and heartbeat APIs.

## Validation
- Run project tests before finalizing backend changes when tests are available.
- Use targeted smoke checks for touched flows when full test runs are impractical.
