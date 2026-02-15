# CHANGELOG

<!-- version list -->

## v1.1.0 (2026-02-15)

### Bug Fixes

- **IPCheck**: IPCheck and tests
  ([`f6de7d6`](https://github.com/m-xim/aiogram-webhook/commit/f6de7d6712ae560dd61a090300a8257ca7a83f6a))

- **security**: Check to SecurityCheck
  ([`8952893`](https://github.com/m-xim/aiogram-webhook/commit/89528937bb690847198efb4bf1034c18a83ab3d6))

- **webhook**: Only set secret_token param if not None
  ([`7dbe835`](https://github.com/m-xim/aiogram-webhook/commit/7dbe835c2b63927a34f8246f8db3334fce07d798))

### Chores

- **build**: Remove packages field from pyproject.toml
  ([`12cc4dd`](https://github.com/m-xim/aiogram-webhook/commit/12cc4ddb4e5a4b65a2f1410ff9108974f5dfac1e))

- **build**: Switch to uv_build backend and migrate ruff config to ruff.toml
  ([`25dcc43`](https://github.com/m-xim/aiogram-webhook/commit/25dcc432fe55f17801f819af343e772b2633087f))

- **pyproject**: Add support for Python 3.14
  ([`cb5e710`](https://github.com/m-xim/aiogram-webhook/commit/cb5e7106dace85d00ebcffb78d495fbcdf4a221f))

### Documentation

- **core**: Add and improve docstrings for adapters, routing, security, and checks
  ([`fee7007`](https://github.com/m-xim/aiogram-webhook/commit/fee70078491824607e85aaffc5ce258756c9f083))

### Features

- **secret_token**: Add secret token format validation and update tests
  ([`fb46f4d`](https://github.com/m-xim/aiogram-webhook/commit/fb46f4d4fc3def30f79cc293916b645a468bf233))

- **webhook_config**: Add WebhookConfig for default webhook parameters and update engine interfaces
  ([`1b319e1`](https://github.com/m-xim/aiogram-webhook/commit/1b319e1bd2d0a340162acaa871cfaf7b43ae3fe6))

### Refactoring

- **ip**: Unify IPAddress and IPNetwork types, update adapters and checks
  ([`8c26d7e`](https://github.com/m-xim/aiogram-webhook/commit/8c26d7e8f3f28c8a1b5dc0cc5b2d1929d1128688))

- **security**: Rename Check protocol to SecurityCheck
  ([`f95ad95`](https://github.com/m-xim/aiogram-webhook/commit/f95ad955fd503c78168c60b68f01be374b0f1865))


## v1.0.0 (2026-02-13)

### Bug Fixes

- **query routing**: Replace extend_query with update_query for parameter override
  ([`e2da44b`](https://github.com/m-xim/aiogram-webhook/commit/e2da44bd0b035901aa9c8dd38a147c2149d5280d))

- **readme**: Update web adapter for aiohttp
  ([`4eac869`](https://github.com/m-xim/aiogram-webhook/commit/4eac8696e1094997493eedcf951f1adedace566a))

- **token**: Update on_startup method to use keyword-only arguments
  ([`9633886`](https://github.com/m-xim/aiogram-webhook/commit/9633886971923268c23e6ecdb366ff88de6448f4))

- **webhook**: Implement set_webhook method in base
  ([`94bd9dc`](https://github.com/m-xim/aiogram-webhook/commit/94bd9dcceed3ba216b2e8ef692d872a8ce206791))

### Chores

- **ci**: Update actions/checkout and astral-sh/setup-uv versions in workflows
  ([`1e1468b`](https://github.com/m-xim/aiogram-webhook/commit/1e1468be0eaa5cf4eda12024fefb7e3c4a8a21c0))

- **pyproject**: Remove allow_zero_version setting
  ([`1ba993d`](https://github.com/m-xim/aiogram-webhook/commit/1ba993d1955d4a7a370b05177711f4a5a553768a))

### Documentation

- **CONTRIBUTING**: Add contributing guidelines
  ([`a0171c2`](https://github.com/m-xim/aiogram-webhook/commit/a0171c29730f7e3af9ff0d6277e97168ebee782a))

- **example**: Add startup function to register webhook on bot initialization
  ([`d010e67`](https://github.com/m-xim/aiogram-webhook/commit/d010e67a4c3c4ace94aeb9b80465053646804bcf))

- **README**: Correct
  ([`c3e8465`](https://github.com/m-xim/aiogram-webhook/commit/c3e8465fa509ff5e28a1336ab16908f9c0dfbe27))

### Features

- **ip**: Add support for X-Forwarded-For header
  ([`3c80341`](https://github.com/m-xim/aiogram-webhook/commit/3c80341eb088b06414a201af2826324d0097ce8a))

- **routing**: Add default parameter name for PathRouting and QueryRouting
  ([`22b5379`](https://github.com/m-xim/aiogram-webhook/commit/22b5379e6be2aa6386433b8d8851706eb3b47f10))

- **routing**: Introduce TokenRouting and StaticRouting, refactor PathRouting and QueryRouting to
  inherit from TokenRouting
  ([`3a02200`](https://github.com/m-xim/aiogram-webhook/commit/3a022003d9b2cb228e03bd73344a308b876775f7))

- **tests**: Add Python 3.15
  ([`322859b`](https://github.com/m-xim/aiogram-webhook/commit/322859b6e7dd409b479f4d9ce446d9f1c04f394a))

- **tests**: Add StaticRouting tests and refactor PathRouting and QueryRouting tests
  ([`f45bb99`](https://github.com/m-xim/aiogram-webhook/commit/f45bb992597b5eca745fee1f6b5bd924ff4abd99))

- **tests**: Add tests
  ([`edb4cec`](https://github.com/m-xim/aiogram-webhook/commit/edb4cec773a1592b5fd0f0ce80faaab4bdff58e2))

- **tests**: Add tests for IPCheck with X-Forwarded-For header
  ([`a4b9517`](https://github.com/m-xim/aiogram-webhook/commit/a4b9517baf8fdd80cfcb4eca0ef309baf66dc678))

### Refactoring

- **bot**: Rename resolve_bot_from_request to _get_bot_from_request and update related methods
  ([`f31bd8c`](https://github.com/m-xim/aiogram-webhook/commit/f31bd8c1042affcd9cb4dc155226f95b4d5d765b))

- **docs**: Add about new routing
  ([`8c62ad9`](https://github.com/m-xim/aiogram-webhook/commit/8c62ad97a93da4a7e4bb6cb5507d097262822b39))

- **ip**: Unify IP retrieval methods and enhance X-Forwarded-For extraction
  ([`9e84588`](https://github.com/m-xim/aiogram-webhook/commit/9e845881726895b03eed2a1aa8fcf06078c2d4d8))

- **routing**: Enhance URL handling and token extraction in routing classes
  ([`bc6f656`](https://github.com/m-xim/aiogram-webhook/commit/bc6f6566bdf7d03988d091e07538eabe7e015164))

- **routing**: Improve initialization and token handling in routing classes
  ([`84491ca`](https://github.com/m-xim/aiogram-webhook/commit/84491ca21e0571a8f657c1c830d5a6a7bdcb8b5a))

- **security**: Simplify security parameter handling in constructors
  ([`f134fd0`](https://github.com/m-xim/aiogram-webhook/commit/f134fd071b613a4661656d78594d9940bc517301))

- **startup**: Update on_startup and on_shutdown methods to accept app argument
  ([`a4e624b`](https://github.com/m-xim/aiogram-webhook/commit/a4e624bed8f0aadd76e3266b7cd2f051a7748c95))

- **webhook**: Simplify signature of on_startup and on_shutdown methods; add _build_workflow_data
  helper
  ([`a3ef6b6`](https://github.com/m-xim/aiogram-webhook/commit/a3ef6b6cfba127ac7c46e98f508559e937ff1c40))

- **webhook**: Streamline payload building and enhance file handling in webhook response
  ([`900ec00`](https://github.com/m-xim/aiogram-webhook/commit/900ec0079f56896e8ad86624dc82b13daca137f9))


## v0.2.0 (2026-01-31)

### Chores

- **pyproject**: Relax aiogram and yarl version requirements
  ([`b8eb941`](https://github.com/m-xim/aiogram-webhook/commit/b8eb9415bd154672b11a65183c42177087cc1618))

### Code Style

- **simple, token**: Condense dispatcher event calls to single lines
  ([`55e997b`](https://github.com/m-xim/aiogram-webhook/commit/55e997b95564bfc76ffca43a92d2aab5481a3782))

### Features

- **aiohttp, docs**: Add aiohttp optional dependency, update adapter import, and expand README with
  aiohttp usage and engine details
  ([`fbd7247`](https://github.com/m-xim/aiogram-webhook/commit/fbd72478d64df8171107222ced7c087c59875ae8))


## v0.1.0 (2026-01-15)

### Chores

- **pyproject**: Add per-file ignores for ruff linting in tests and create package init file
  ([`9b7dc1a`](https://github.com/m-xim/aiogram-webhook/commit/9b7dc1ac1c34e319f880a1aed8e5afb5da3b6775))

### Documentation

- **readme**: Update
  ([`ee6731f`](https://github.com/m-xim/aiogram-webhook/commit/ee6731fe94f5aa65f7d8afe7c82ce411d38f2fc4))

### Features

- **aiohttp**: Add aiohttp integration
  ([`da2dd02`](https://github.com/m-xim/aiogram-webhook/commit/da2dd02f3aecc96351ac72edf9b1026ffed95f9a))

### Testing

- **security, routing**: Add tests for security checks and routing logic with dummy adapter
  ([`5c3a449`](https://github.com/m-xim/aiogram-webhook/commit/5c3a44992572e94afb215c7db7862f2d87b5b66b))


## v0.0.3 (2025-12-28)


## v0.0.2 (2025-12-27)


## v0.0.1 (2025-12-27)

- Initial Release
