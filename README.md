![Aiogram Webhook](docs/_assets/brand/banner.png)

# aiogram-webhook
[![PyPI version](https://img.shields.io/pypi/v/aiogram-webhook?color=blue)](https://pypi.org/project/aiogram-webhook)
[![codecov](https://codecov.io/github/m-xim/aiogram-webhook/graph/badge.svg?token=H21MX17Y7D)](https://codecov.io/github/m-xim/aiogram-webhook)
[![Tests Status](https://github.com/m-xim/aiogram-webhook/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-webhook/actions)
[![License](https://img.shields.io/github/license/m-xim/aiogram-webhook.svg)](/LICENSE)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/m-xim/aiogram-webhook)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

Handles the webhook layer for aiogram bots. Registers the endpoint, calls Telegram `setWebhook`, verifies incoming requests, and manages engine lifecycle. Works with FastAPI and aiohttp.

## Install

```bash
pip install aiogram-webhook
pip install "aiogram-webhook[fastapi]"
pip install "aiogram-webhook[aiohttp]"
```

## Documentation

The full documentation is at [aiogram-webhook.m-xim.ru](https://aiogram-webhook.m-xim.ru). It covers installation, setup, routing, security, lifecycle behavior, and the public API.

## Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for development setup, branch naming, commit conventions, and PR guidelines.
