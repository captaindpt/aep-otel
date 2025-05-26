TASK: bootstrap logbook and repo skeleton
ETA: <15 min
DEPENDENCIES: zero-to-one.md, local git repo
OPEN QUESTIONS: Will GitHub remote be created manually or via automation?

TASK: scaffold multi-language SDK directories (python/, node/, go/)
ETA: 1 hr
DEPENDENCIES: bootstrap task
OPEN QUESTIONS: Which minimum Python/Node/Go versions for CI matrix?

TASK: set up GitHub Actions CI for lint + test across languages
ETA: 2 hrs
DEPENDENCIES: scaffold SDK directories, GitHub repo
OPEN QUESTIONS: Preferred test frameworks?

TASK: implement minimal Python OpenAI wrapper emitting AEP span
ETA: 2 hrs
DEPENDENCIES: python SDK directory
OPEN QUESTIONS: Which OTEL exporter default (stdout vs collector URL)?

TASK: author OTEL collector sample config + docker-compose
ETA: 45 min
DEPENDENCIES: minimal wrapper task
OPEN QUESTIONS: Should we embed collector binary or require user install?

TASK: draft README with quick-start and architecture diagram link
ETA: <30 min
DEPENDENCIES: collector sample config, wrapper impl
OPEN QUESTIONS: Where to host diagram images?

TASK: publish PyPI pre-alpha (0.0.1a0) via GitHub Action release-please
ETA: 1 hr
DEPENDENCIES: CI setup, wrapper impl
OPEN QUESTIONS: Package name `aep-otel` ok?

TASK: capture demo trace screenshot and embed in README
ETA: 15 min
DEPENDENCIES: wrapper impl, collector config
OPEN QUESTIONS: Acceptable to store PNG in repo?

TASK: Make a `feat:` commit, merge `release-please` PR, and trigger first PyPI publish
ETA: <15 min
DEPENDENCIES: PyPI trusted publishing configured, `release-please.yml`, `pypi-publish.yml`
OPEN QUESTIONS: Confirm PyPI project created successfully after first publish

TASK: Test `semantic-release` setup and trigger first release
ETA: 1 hr
DEPENDENCIES: `semantic-release.yml` workflow, `.releaserc.json`, `package.json` & `package-lock.json` (or `yarn.lock`) committed, `GH_PAT_FOR_SEMANTIC_RELEASE` secret configured
OPEN QUESTIONS: Confirm `pyproject.toml` version bumping strategy (currently manual/placeholder, requires `@semantic-release/exec` for full automation with Poetry)

TASK: Implement automatic `pyproject.toml` version bumping with `semantic-release`
ETA: 1.5 hrs
DEPENDENCIES: Working `semantic-release` setup, Poetry installed in CI environment
OPEN QUESTIONS: Best way to integrate `poetry version ${nextRelease.version}` into the `semantic-release` lifecycle? (`@semantic-release/exec` likely candidate) 