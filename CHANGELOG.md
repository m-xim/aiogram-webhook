# CHANGELOG

<!-- version list -->

## v3.2.0 (2026-10-07)

### Bug Fixes

- Add Route to __all__ exports in __init__.py
  ([`3e971f7`](https://github.com/m-xim/aiogram-webhook/commit/3e971f7072693a9a8b15765508fa7c77e7034d02))

- Allow non-ASCII filenames in content disposition for form-data
  ([`7cef166`](https://github.com/m-xim/aiogram-webhook/commit/7cef1664fa9608196518ece7df97a225b818bfad))

- Enhance shutdown process by allowing optional bot parameter in _on_shutdown method
  ([`0b9da4f`](https://github.com/m-xim/aiogram-webhook/commit/0b9da4f76d92de0c3e7d9e51f8e8c07c70c050c3))

- Ensure proper detachment of bot and tracker in token engine
  ([`5c4abb8`](https://github.com/m-xim/aiogram-webhook/commit/5c4abb80089bf00d9fa35a730f9c58e57939ac7b))

- Improve request handling by validating payload format and ensuring shutdown safety
  ([`fcae097`](https://github.com/m-xim/aiogram-webhook/commit/fcae097eb978a18b028f676b2a3a2b6eac246d18))

- Raise error when handling requests during shutdown in TokenEngine
  ([`b2385ab`](https://github.com/m-xim/aiogram-webhook/commit/b2385ab7f2fd8109638e56daec78726bb936a041))

- Update lifespan function signature to use None
  ([`ab41d78`](https://github.com/m-xim/aiogram-webhook/commit/ab41d786d29533933a53e33ac4ce4204bdb25cba))

- **gate**: Update type hint for enter method to use Generator
  ([`606f8c2`](https://github.com/m-xim/aiogram-webhook/commit/606f8c2cf97a2aab4fdbb128a25040d6e06bf50b))

- **security**: Enhance secret token validation to reject non-ASCII characters
  ([`5de91c9`](https://github.com/m-xim/aiogram-webhook/commit/5de91c99f0561058aeb70c1c769aab65b80fde13))

- **security**: Ensure secret token comparison handles encoding for non-ASCII characters
  ([`742965a`](https://github.com/m-xim/aiogram-webhook/commit/742965a776eb99ed07084c048898a265efc9415b))

- **ty**: Remove type ignore comments from assertions in test files
  ([`18d5daf`](https://github.com/m-xim/aiogram-webhook/commit/18d5daf7303b3bbd1e8aedd60528ce6ab57702e2))

- **web**: Note about lifespan in fastapi
  ([`dba27ce`](https://github.com/m-xim/aiogram-webhook/commit/dba27cec09a8e5fdb0847a700f5fdeeaff01ba74))

### Chores

- Add context7
  ([`7d6b9d6`](https://github.com/m-xim/aiogram-webhook/commit/7d6b9d61bd3264bd0c7945fb3e3edb8584654ac3))

- Reorder imports
  ([`d48c019`](https://github.com/m-xim/aiogram-webhook/commit/d48c0195f21f00b7d9a3b5c9c08e515b3f1bf612))

- Update .gitignore to include profile
  ([`0cf924b`](https://github.com/m-xim/aiogram-webhook/commit/0cf924bac6adb05cb2928870380ab95e07efce98))

- Update dependabot configuration for multiple ecosystems
  ([`a642ae8`](https://github.com/m-xim/aiogram-webhook/commit/a642ae8d592313ae3a120a5493c5f46722267e4b))

- Update dependencies in package-lock.json
  ([`874dcb0`](https://github.com/m-xim/aiogram-webhook/commit/874dcb0e98edf618fbad3ddf691bbfeb914d7f49))

- Update dependencies in package-lock.json
  ([`9ff2283`](https://github.com/m-xim/aiogram-webhook/commit/9ff2283846694e1da764c47a755908a0f26d49db))

- Update GitHub Actions workflows
  ([`2adf54e`](https://github.com/m-xim/aiogram-webhook/commit/2adf54ebe4afc2747f3010a7efe8ce91b1a14ada))

- Update package-lock.json and ruff.toml
  ([`c28c79c`](https://github.com/m-xim/aiogram-webhook/commit/c28c79c5a1f864359f7dd62f788b5387b990edb6))

- Update package-lock.json with dependency version upgrades
  ([`bdb5dc7`](https://github.com/m-xim/aiogram-webhook/commit/bdb5dc7339d56e87fa94a4546852bde3af687512))

- Update release workflow to use trusted publishing for PyPI
  ([`c86588d`](https://github.com/m-xim/aiogram-webhook/commit/c86588da023ab6211ba90e639c55252b3314d98b))

- **ci**: Bump actions/checkout from 6 to 7
  ([`aedd88a`](https://github.com/m-xim/aiogram-webhook/commit/aedd88a951f7ed3d7ad8b93b03d995ad3d7d4a3c))

- **ci**: Bump actions/configure-pages from 5 to 6
  ([`2c0ad93`](https://github.com/m-xim/aiogram-webhook/commit/2c0ad9370c3dd2a8a7370d21194c72a6e92c16b9))

- **ci**: Bump actions/deploy-pages from 4 to 5
  ([`4da8774`](https://github.com/m-xim/aiogram-webhook/commit/4da8774af7251c6ab9f7759bd8ba60a4d1fc4f7d))

- **ci**: Bump actions/setup-node from 4 to 7
  ([`c9eee9f`](https://github.com/m-xim/aiogram-webhook/commit/c9eee9ff8fd4977c8e320c5c27002bac11a3d8bc))

- **ci**: Bump actions/upload-pages-artifact from 3 to 5
  ([`b48b2d8`](https://github.com/m-xim/aiogram-webhook/commit/b48b2d887958742e88611e7b578fe3bc79dab9ed))

- **deps**: Bump sanitize-html
  ([`f172fa1`](https://github.com/m-xim/aiogram-webhook/commit/f172fa1927f6f03bcc82bcf2bf5e08e656815fda))

- **deps**: Bump the npm_and_yarn group across 1 directory with 2 updates
  ([`a0de4dc`](https://github.com/m-xim/aiogram-webhook/commit/a0de4dca6b975d3a62cb1fb29b457eaae60f4829))

- **deps**: Bump the npm_and_yarn group across 1 directory with 5 updates
  ([`1a1e781`](https://github.com/m-xim/aiogram-webhook/commit/1a1e7811839840d12ab2099582eba05e33aa54b6))

- **deps**: Update package-lock.json
  ([`85c91b6`](https://github.com/m-xim/aiogram-webhook/commit/85c91b6ae496961b29c3e9cdd556deeef8777acc))

- **deps-dev**: Update uv-build requirement from <0.12 to <0.13
  ([`9e6d942`](https://github.com/m-xim/aiogram-webhook/commit/9e6d942f92ea37484e3761ac3d663f2a5b942e34))

### Documentation

- Clarify error messages and update example in TokenEngine documentation
  ([`ed4fbc3`](https://github.com/m-xim/aiogram-webhook/commit/ed4fbc341f52503d3d5701669eb3b980e9f68c14))

- Clarify multipart content requirements for payload_response in TelegramMethod handling
  ([`41e3659`](https://github.com/m-xim/aiogram-webhook/commit/41e3659f1dad76c70f6fc2b8c62dd1d49aedc65f))

- Enhance TokenEngine docstring for clarity
  ([`f26a8df`](https://github.com/m-xim/aiogram-webhook/commit/f26a8dfdce26b0dfb1e42af94e5b0a1f67b488fa))

- Fix examples
  ([`17701f2`](https://github.com/m-xim/aiogram-webhook/commit/17701f2b85f4feb319f8c0a2ea11c95af9251274))

- Fix warning about request body size limitations in Starlette
  ([`76cfd09`](https://github.com/m-xim/aiogram-webhook/commit/76cfd09a5119fdb1257ace1a30e83632d7e86caa))

- Format code for better readability in custom-engine.md
  ([`03074cf`](https://github.com/m-xim/aiogram-webhook/commit/03074cfa14c80a009792531acece707da6ce07f9))

- Update custom adapter on payload handling
  ([`b965b83`](https://github.com/m-xim/aiogram-webhook/commit/b965b835020749297e67c5b90b80e439b9074022))

- Update diplodoc
  ([`e8f08b2`](https://github.com/m-xim/aiogram-webhook/commit/e8f08b277fdc496406535b72599cea01d6f64a92))

- Update diplodoc
  ([`d49d527`](https://github.com/m-xim/aiogram-webhook/commit/d49d527cff6022b99074d3e066dc48522c95f6fb))

- **fastapi**: Add warning about request body size limitations
  ([`6ec3636`](https://github.com/m-xim/aiogram-webhook/commit/6ec36361b9360393e4d4af097baabe27dd38bea9))

### Features

- Add debug logging for raw update processing
  ([`a2764a4`](https://github.com/m-xim/aiogram-webhook/commit/a2764a45aa498bedf8c9320035ed6b9dedd313ab))

- **gate**: Implement RequestGate to manage request admission and closure
  ([`342e416`](https://github.com/m-xim/aiogram-webhook/commit/342e4168adee74f6c5e440b430ba49fb201210ef))

- **gate**: Integrate RequestGate for request management during shutdown
  ([`e11eb2e`](https://github.com/m-xim/aiogram-webhook/commit/e11eb2edae627267c468173cf731b42c62f161a5))

- **payload**: Refactor webhook payload handling to support JSON-native values
  ([`fe160b0`](https://github.com/m-xim/aiogram-webhook/commit/fe160b05890a88052e32b7da553d75b49d8acb74))

### Refactoring

- Types, tests, docstring
  ([`9d9b787`](https://github.com/m-xim/aiogram-webhook/commit/9d9b787fb3c727e6c769bc125e3ad8edc3f93bbe))

### Testing

- Add tests for bot removal and shutdown behavior in TokenEngine
  ([`abd475a`](https://github.com/m-xim/aiogram-webhook/commit/abd475aece39df76570b8ba78493f6dec2e43a7c))

- Add tests for handling invalid JSON payloads in webhook engine
  ([`90e523b`](https://github.com/m-xim/aiogram-webhook/commit/90e523b052b579e7f8aae894b7bcab640468810e))

- Remove unnecessary type ignore comments in webhook engine tests
  ([`ee3abc7`](https://github.com/m-xim/aiogram-webhook/commit/ee3abc7e884fcc5d358d02b996d860251ea6a7cf))


## v3.1.0 (2026-06-10)

### Features

- **web**: Add auto lifespan for fastapi, update tests
  ([`13af449`](https://github.com/m-xim/aiogram-webhook/commit/13af449c1b3001aada0802b58a4db475db909820))

- **web**: Add note about lifespan in fastapi
  ([`7d4f375`](https://github.com/m-xim/aiogram-webhook/commit/7d4f37542f8e6665a61d9b510f3973399cec6556))

- **web**: Remove old lifespan
  ([`aa48ba9`](https://github.com/m-xim/aiogram-webhook/commit/aa48ba94102991eefae47fa4b5407a66fa75d9c8))


## v3.0.1 (2026-06-08)

### Bug Fixes

- **engine**: Params
  ([`1ec279f`](https://github.com/m-xim/aiogram-webhook/commit/1ec279ff3a33f0038aa00b58e6f2ba90430bf958))


## v3.0.0 (2026-06-08)

### Bug Fixes

- **docs**: 404 base path for style, scripts etc
  ([`6cb75c7`](https://github.com/m-xim/aiogram-webhook/commit/6cb75c74f8a2b3c06e51dbf331dd77e28e327a03))

- **docs**: Favicon
  ([`127036b`](https://github.com/m-xim/aiogram-webhook/commit/127036b9d67dd1f60a1930f550d62e63a71252e3))

- **docs**: Links
  ([`6d414dc`](https://github.com/m-xim/aiogram-webhook/commit/6d414dc551c6ce53f314c6ad1573f30b3f877fd5))

- **docs**: Remove release badge
  ([`00da2bb`](https://github.com/m-xim/aiogram-webhook/commit/00da2bbd39af701049949e74429700bea6093040))

- **docs**: Remove release badge
  ([`266591a`](https://github.com/m-xim/aiogram-webhook/commit/266591a8b6182c3965df129f652bfc42faf76c82))

- **docs**: Translate
  ([`81f42be`](https://github.com/m-xim/aiogram-webhook/commit/81f42bef5b08d0b5e451b88c621e7a5a61e40f17))

- **docs**: Url
  ([`ab19aca`](https://github.com/m-xim/aiogram-webhook/commit/ab19acac6af1fdb1fe9bdcb8290f51cd55613fb0))

- **engine**: Webhook config
  ([`6937704`](https://github.com/m-xim/aiogram-webhook/commit/6937704850c150f20a847fe825b1adf1fe3c7687))

- **pyproject**: Documentation url
  ([`194ec19`](https://github.com/m-xim/aiogram-webhook/commit/194ec19cda2b0b27ac58fda063728a393f20c1ab))

- **route**: Use lstrip instead of strip for path joining
  ([`5664207`](https://github.com/m-xim/aiogram-webhook/commit/5664207c17e9ed7f400db354a9053f68bbaf629f))

- **token**: _on_shutdown and add timeout in remove_bot
  ([`20736b6`](https://github.com/m-xim/aiogram-webhook/commit/20736b66a9b0b3aee473f9293fcbe12a4bfe9dec))

- **web**: Add lazy headers and query_params
  ([`566f8f9`](https://github.com/m-xim/aiogram-webhook/commit/566f8f9a0ad00470707a0d73bf8fa17c185cc3ed))

- **web**: Content-length for fastapi
  ([`1bd5f11`](https://github.com/m-xim/aiogram-webhook/commit/1bd5f1144317343ff099d4c4ccb31fbcd771aaaa))

### Chores

- Style
  ([`cbf8ba6`](https://github.com/m-xim/aiogram-webhook/commit/cbf8ba6ffb52f728eaf85451582d110f5fd0c408))

### Features

- **ci**: Add environment
  ([`86ab6b8`](https://github.com/m-xim/aiogram-webhook/commit/86ab6b8566d7610010d3c888dedf5ec8497bb9eb))

- **docs**: Add new icons, add new home
  ([`5bfc684`](https://github.com/m-xim/aiogram-webhook/commit/5bfc68476104e0b1b470422ae3be44b8a48eccbd))

- **docs**: Add shutdown_timeout and update dispatch
  ([`aa687bd`](https://github.com/m-xim/aiogram-webhook/commit/aa687bd073175fa0e0379a15e90859588ee0d2c8))

- **docs**: Update mermaid
  ([`e2ac6aa`](https://github.com/m-xim/aiogram-webhook/commit/e2ac6aa680f282579e73250f4d913aa5cd286a86))

- **docs**: Update paths
  ([`b40271f`](https://github.com/m-xim/aiogram-webhook/commit/b40271fcb2f97f2dd22a8275c66c24969d9cf267))

- **engines**: Add configurable shutdown_timeout parameter
  ([`3aed1a4`](https://github.com/m-xim/aiogram-webhook/commit/3aed1a4c3f5814646180e3e6de8f9b39383bbd44))

### Refactoring

- **docs**: Webhook config
  ([`4c39573`](https://github.com/m-xim/aiogram-webhook/commit/4c3957368a93da849965f7fafd5acf9eb01cd0b9))

- **engine**: Webhook config
  ([`965331e`](https://github.com/m-xim/aiogram-webhook/commit/965331edc923935fbef30b5b5b0e1906adcdb146))

- **route**: Build_url
  ([`cb9ee93`](https://github.com/m-xim/aiogram-webhook/commit/cb9ee93c5f87ed7c83e9ec6ad87ef180ef77c808))

- **test**: Use MultiDict directly in DummyRequest
  ([`8175e4d`](https://github.com/m-xim/aiogram-webhook/commit/8175e4d5063cdb436cf49c1ee4e96af7610c0f20))


## v2.0.1 (2026-02-21)

### Bug Fixes

- **BotConfig**: Replace pydantic BaseModel with dataclass for BotConfig
  ([`e492e31`](https://github.com/m-xim/aiogram-webhook/commit/e492e315a5f42d508d7b119a2fd987d23204aa1c))


## v2.0.0 (2026-02-21)

### Bug Fixes

- Remove WebAdapter import
  ([`07a6498`](https://github.com/m-xim/aiogram-webhook/commit/07a6498547405b3cf4e29a024be3846b82526ced))

- **token**: Move BotConfig import from TYPE_CHECKING
  ([`82bb210`](https://github.com/m-xim/aiogram-webhook/commit/82bb210df2cf942fffa072b812d9c96f268c4d64))

### Features

- **base_mapping**: Implement len and iter in mapping interface
  ([`bc50c41`](https://github.com/m-xim/aiogram-webhook/commit/bc50c41e16b3d9bfac604e0867250049735c3a93))

### Refactoring

- Move on_startup
  ([`519c7d2`](https://github.com/m-xim/aiogram-webhook/commit/519c7d2f4d7e7c4815bf726436e65c5fb7a204d9))

- Remove WebAdapter from public API exports
  ([`1ef8bbd`](https://github.com/m-xim/aiogram-webhook/commit/1ef8bbd03100191612feccd897a9509c403bc3fe))

- Unify response creation via WebAdapter and update BoundRequest interface
  ([`3f30edc`](https://github.com/m-xim/aiogram-webhook/commit/3f30edc82d3f9e9eaf653c90c99695e3bb5f9e93))

- **adapters**: Cache headers and query params mappings in BoundRequest implementations
  ([`72c0216`](https://github.com/m-xim/aiogram-webhook/commit/72c02161a0f4767d233324faabc4c0fb01b30bf9))

- **adapters**: Unify BoundRequest interface and introduce framework-specific mappings
  ([`ca3693c`](https://github.com/m-xim/aiogram-webhook/commit/ca3693c104caab61c7cbc3b101cd611b9a2fbf97))

- **ip**: Refactoring
  ([`3292a0f`](https://github.com/m-xim/aiogram-webhook/commit/3292a0f2c3b074f5ad22a0d09e889605310a856a))

- **security**: Remove redundant security checks and default to Security instance
  ([`5214a65`](https://github.com/m-xim/aiogram-webhook/commit/5214a657ab01e76e566b728de0c6ce11a23ea995))

- **security**: Update type hints for BoundRequest and clarify SecretToken docstring
  ([`e5a0509`](https://github.com/m-xim/aiogram-webhook/commit/e5a0509a91943aa1fd49bab9523ee817a956de0a))

- **tests**: Introduce DummyRequest and update DummyBoundRequest
  ([`abba2a0`](https://github.com/m-xim/aiogram-webhook/commit/abba2a09cc132e5d72016d8a2ec5136efe460647))

- **token**: Use BotConfig instance for bot initialization
  ([`aedd111`](https://github.com/m-xim/aiogram-webhook/commit/aedd111659bab4bdf1bbf6e403df675188c2a8c6))

- **WebhookEngine**: Make security optional and update secret token handling
  ([`e0d8fb3`](https://github.com/m-xim/aiogram-webhook/commit/e0d8fb393860a94f872bc9320210af2f4c4bd2ee))

- **WebhookEngine**: Pass parsed update dict instead of BoundRequest to handler methods
  ([`c50af89`](https://github.com/m-xim/aiogram-webhook/commit/c50af890a04b41223221b28edfc52f8177c787ab))


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
