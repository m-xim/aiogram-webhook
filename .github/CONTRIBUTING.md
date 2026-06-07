# Contributing to aiogram-webhook

Thank you for your interest in contributing!
This guide covers everything you need to get started — from setting up the environment to opening a pull request.

## Development setup

```bash
git clone https://github.com/m-xim/aiogram-webhook.git
cd aiogram-webhook
uv sync --all-extras --upgrade
```

## Before committing

Run the full check suite before every commit:

```bash
uv run ruff format
uv run ruff check --fix
uv run ty check
uv run pytest
```

All checks must pass. PRs with failing CI will not be reviewed.

## Branch naming

Use the same type prefix as your commit message:

```
feat/add-custom-adapter
fix/route-path-strip
docs/update-security-page
test/token-engine-edge-cases
```

## Commit message format

We follow [Conventional Commits](https://www.conventionalcommits.org/).

Format: `type(scope): description`

**Types:**
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation changes
- `test` — test additions or changes
- `refactor` — code refactoring without behavior change
- `perf` — performance improvements
- `chore` — dependencies, config, tooling

**Scopes (optional):** `route`, `security`, `web`, `engines`

**Rules:**
- Lowercase after the type prefix
- Imperative mood: `add`, `fix`, `update` — not `added`, `fixed`, `updating`
- No period at the end
- Keep the subject line under 72 characters

**Examples:**
```
feat(security): add IP allowlist check
fix(route): use lstrip instead of strip for path joining
docs(web): add aiohttp lifecycle example
test(engines): cover token resolution edge cases
```

## Pull requests

1. Fork the repo and create a branch from `develop` (not `main`).
2. Keep PRs focused — one feature or fix per PR.
3. Add or update tests for every behavior change.
4. Update documentation if the public API or behavior changes.
5. Fill in the PR description: what changed and why.

## Reporting issues

Before opening an issue, search [existing issues](https://github.com/m-xim/aiogram-webhook/issues) to avoid duplicates.

Include:
- Python version and OS
- `aiogram-webhook` version
- Minimal reproducible example
- Full traceback if applicable

## Documentation

The docs live in `docs/` and are built with [Diplodoc]( https://diplodoc.com/) (YFM — Yandex Flavored Markdown).

### Preview locally

```bash
npm install
npm run docs      # build + serve at http://localhost:8080
```

Or separately:

```bash
npm run build     # outputs to docs-html/
npm run web       # serve docs-html/ with http-server
```

### Structure

```
docs/
├── pages/            # Markdown source pages
│   ├── learn/        # Getting started
│   ├── web/          # Web adapter guides
│   ├── engines/      # Engine guides
│   ├── route/        # Route guides
│   ├── security/     # Security guides
│   ├── recipes/      # End-to-end examples
│   └── other/        # API reference, errors, config
├── _assets/          # Images, icons, CSS, JS
├── _includes/        # Reusable Markdown snippets
├── toc.yaml          # Navigation tree (sidebar)
├── index.yaml        # Landing page blocks
├── theme.yaml        # Color theme overrides
└── .yfm              # Diplodoc build config
```

### Adding a page

1. Create a `.md` file under `docs/pages/<section>/`.
2. Add an entry in `docs/toc.yaml` under the right section.
3. Run `npm run docs` to verify rendering and navigation.

### YFM format

Pages use standard Markdown. Some Diplodoc-specific features available:
- `{% note %}...{% endnote %}` — callout blocks (`info`, `warning`, `tip`, `alert`)
- `{% cut "title" %}...{% endcut %}` — collapsible sections
- `#|...|#` — tables with extended syntax

See the [Diplodoc syntax reference](https://diplodoc.com/docs/en/syntax/) for the full list.

### What counts as a docs change

Use the `docs` commit type for any change inside `docs/`. If you add a public API or change behavior, update the relevant docs page in the same PR.

## Project structure

```
src/aiogram_webhook/
├── web/        # Web framework adapters (FastAPI, aiohttp)
├── engines/    # Webhook engine implementations
├── route/      # Route and URL building
└── security/   # Request validation and security checks
```

---

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Discussions](https://github.com/m-xim/aiogram-webhook/discussions)
