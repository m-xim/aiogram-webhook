# Contributing to aiogram-webhook

## Setup
```bash
git clone https://github.com/m-xim/aiogram-webhook.git
cd aiogram-webhook
uv sync --all-extras --upgrade
```

## Before Commit
```bash
uv run ruff format
uv run ruff check --fix

uv run ty check

uv run pytest
```

## Commit Message Format
We use [Conventional Commits](https://www.conventionalcommits.org/) for clear commit history.

Format: `type(scope): description`

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation changes
- `test` — Test additions/changes
- `refactor` — Code refactoring
- `perf` — Performance improvements
- `chore` — Other changes (dependencies, config)

**Scope (optional):** Module or component affected
- `routing`
- `security`
- `adapters`
- `engines`

**Good commit messages:**
- Clear and descriptive
- Start with lowercase (after type)
- No period at the end
- Imperative mood (add, fix, update, not adds, fixed, updating)

## Project Structure
```
src/aiogram_webhook/
├── adapters/          # Web framework adapters
├── engines/           # Core webhook engine
├── routing/           # Routing strategies
└── security/          # Security checks
```

---

For more details:
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Issues](https://github.com/m-xim/aiogram-webhook/issues)
- [GitHub Pull Requests](https://github.com/m-xim/aiogram-webhook/pulls)
- [GitHub Discussions](https://github.com/m-xim/aiogram-webhook/discussions)
















