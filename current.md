TASK IN PROGRESS: Automate Python SDK versioning (`pyproject.toml`) within the `semantic-release` process.
BLOCKERS / NOTES:
  - Need to integrate `poetry version` command into the `semantic-release` workflow, likely using `@semantic-release/exec`.
  - Ensure the `semantic-release` commit includes the `pyproject.toml` change before tagging.
NEXT SMALL STEP: Investigate and configure `@semantic-release/exec` in `.releaserc.json` and update `.github/workflows/semantic-release.yml` if necessary to support Poetry. 