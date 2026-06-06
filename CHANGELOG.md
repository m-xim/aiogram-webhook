# CHANGELOG

<!-- version list -->

## v1.0.0-rc.1 (2026-06-06)

### Bug Fixes

- Deps
  ([`48f8513`](https://github.com/m-xim/aiogram-webhook/commit/48f85136f27b6a2d45b920d5ac0d18ec36095953))

- Docs
  ([`c1dff56`](https://github.com/m-xim/aiogram-webhook/commit/c1dff567d50c4c5a255d5685bca781c0c9307615))

- Fixed
  ([`fc1e857`](https://github.com/m-xim/aiogram-webhook/commit/fc1e8579ee61d821f6602b5304a3d73ac59902d1))

- Fixed
  ([`a0b1f54`](https://github.com/m-xim/aiogram-webhook/commit/a0b1f5426ecb151924595a1982860c8dfaa907f5))

- Handle ModuleNotFoundError for non-fastapi imports
  ([`313bdd5`](https://github.com/m-xim/aiogram-webhook/commit/313bdd57cd294f8c90cef4c1af4add525a448beb))

- Remove WebAdapter import
  ([`07a6498`](https://github.com/m-xim/aiogram-webhook/commit/07a6498547405b3cf4e29a024be3846b82526ced))

- Version
  ([`9819c82`](https://github.com/m-xim/aiogram-webhook/commit/9819c8201c5263f3f90b3ada76f11b98ccf62d14))

- **action**: Docs
  ([`b77975f`](https://github.com/m-xim/aiogram-webhook/commit/b77975f9bb9779353694c868cd54474572577019))

- **aiohttp**: Client_ip type
  ([`1e5c426`](https://github.com/m-xim/aiogram-webhook/commit/1e5c42664ad69f4b96bba4dfbbb7d4e14810c455))

- **base**: _get_bot_from_request
  ([`d3c776f`](https://github.com/m-xim/aiogram-webhook/commit/d3c776f9f85ca89afc125e462dd61b2dbfa292f0))

- **base**: Add warning for unconfigured security in _verify_security method
  ([`6689cd8`](https://github.com/m-xim/aiogram-webhook/commit/6689cd846ed4410dde609e9a4f0d244dad30b2f9))

- **base**: Update _verify_security call to be async
  ([`10e2aad`](https://github.com/m-xim/aiogram-webhook/commit/10e2aad485df05a44b1d1d4dc36f4c45ff5bf848))

- **base, token**: Handle None token case and correct bot storage reference
  ([`849cee2`](https://github.com/m-xim/aiogram-webhook/commit/849cee2869137847d3208ba0a569dec39462d981))

- **bot**: Avoid creating a new Bot for each request
  ([`95d5367`](https://github.com/m-xim/aiogram-webhook/commit/95d53671c4a4253b9feb385b526e25f2f64b575a))

- **bot**: Bot caching and security verification logic
  ([`8cb0e5d`](https://github.com/m-xim/aiogram-webhook/commit/8cb0e5dee8fa816ffedef039e64c746891b42ac7))

- **bot**: Deprecate get_bot method and introduce caching in bot management
  ([`5fa99cc`](https://github.com/m-xim/aiogram-webhook/commit/5fa99cc369704797af26a93e1e05885cba68e37c))

- **BotConfig**: Replace pydantic BaseModel with dataclass for BotConfig
  ([`e492e31`](https://github.com/m-xim/aiogram-webhook/commit/e492e315a5f42d508d7b119a2fd987d23204aa1c))

- **ci**: Update setup-uv action to version 8.1.0
  ([`c0b9355`](https://github.com/m-xim/aiogram-webhook/commit/c0b93553a4704044b0c97bf74a0a1d1d3f88cb4c))

- **ci**: Update versions
  ([`d62fd09`](https://github.com/m-xim/aiogram-webhook/commit/d62fd091454fbb5f32c6e064dba9057c5e27f49a))

- **dependencies**: Update httpx to httpx2 for fastapi testing
  ([`a6586a6`](https://github.com/m-xim/aiogram-webhook/commit/a6586a648a45c5816cf86266ec9c299573a6aade))

- **docs**: .yfm
  ([`a0235e1`](https://github.com/m-xim/aiogram-webhook/commit/a0235e1d02e07b73ea8ded39cc18bbd668d6cc66))

- **docs**: Action
  ([`b2bc6e3`](https://github.com/m-xim/aiogram-webhook/commit/b2bc6e3b720e8b03a365dac194e430b9851dba33))

- **docs**: Action
  ([`0dbde68`](https://github.com/m-xim/aiogram-webhook/commit/0dbde68e6430c152336a8b9c1cb963b4ada3713e))

- **docs**: Action
  ([`5872a10`](https://github.com/m-xim/aiogram-webhook/commit/5872a10848e8509365e647f52ce2c5b085966012))

- **docs**: Action
  ([`2d8bf15`](https://github.com/m-xim/aiogram-webhook/commit/2d8bf15ec6df691a6fa492a2fad349b6fbfb0617))

- **docs**: Ci
  ([`54e116d`](https://github.com/m-xim/aiogram-webhook/commit/54e116d4d6e0a68828dead7f89c06ceb0738a4a6))

- **docs**: Remove js file
  ([`af8a457`](https://github.com/m-xim/aiogram-webhook/commit/af8a457b9798543f3eaa649a64432fd61dc63607))

- **docs**: Vcs
  ([`b0d195c`](https://github.com/m-xim/aiogram-webhook/commit/b0d195c525e382911d1ded6e4422940bb1500aa4))

- **docs**: Vcs
  ([`b9b3e6e`](https://github.com/m-xim/aiogram-webhook/commit/b9b3e6e2e7f5c9ce4962f5ddaddd0570cd17e204))

- **errors**: Correct typo in error message variable name
  ([`f0b2bb5`](https://github.com/m-xim/aiogram-webhook/commit/f0b2bb5f2cd506bb9a5afd40de0eec1bc4b3adde))

- **errors**: Improve error messages for query and path parameter mismatches
  ([`3c35a17`](https://github.com/m-xim/aiogram-webhook/commit/3c35a176908977a188c48c2583227ec02ffc3a5d))

- **errors**: Update log levels and status codes
  ([`0b7763a`](https://github.com/m-xim/aiogram-webhook/commit/0b7763a9ace4d1afa02144ba0fe43ac90b8b675e))

- **gitignore**: Add node_modules to ignore list
  ([`54f8d08`](https://github.com/m-xim/aiogram-webhook/commit/54f8d087fae35fccd6f5dd7708035142c0326d80))

- **import**: Add dataclass_config_to_kwargs utility function
  ([`86666f8`](https://github.com/m-xim/aiogram-webhook/commit/86666f87e6656d2ed157f75210aab413dafdba4b))

- **IPCheck**: IPCheck and tests
  ([`f6de7d6`](https://github.com/m-xim/aiogram-webhook/commit/f6de7d6712ae560dd61a090300a8257ca7a83f6a))

- **query**: Correct isinstance checks for value types in query normalization
  ([`b5535f6`](https://github.com/m-xim/aiogram-webhook/commit/b5535f67e93e1ef702c324dfc8d34bed3dd4386f))

- **query routing**: Replace extend_query with update_query for parameter override
  ([`e2da44b`](https://github.com/m-xim/aiogram-webhook/commit/e2da44bd0b035901aa9c8dd38a147c2149d5280d))

- **readme**: Update web adapter for aiohttp
  ([`4eac869`](https://github.com/m-xim/aiogram-webhook/commit/4eac8696e1094997493eedcf951f1adedace566a))

- **response**: Update headers in payload_response and improve error messages
  ([`8cd1896`](https://github.com/m-xim/aiogram-webhook/commit/8cd1896c7cb22f17f5ac98e1aca3b6122fb2487c))

- **route**: Update route_params type to Any
  ([`d504772`](https://github.com/m-xim/aiogram-webhook/commit/d504772f05934af1c69a11719ac822c1f3bb57da))

- **security**: Add set `secret_token`
  ([`c18250c`](https://github.com/m-xim/aiogram-webhook/commit/c18250c153270912250c0d129f3cb3263900c1d1))

- **security**: Check to SecurityCheck
  ([`8952893`](https://github.com/m-xim/aiogram-webhook/commit/89528937bb690847198efb4bf1034c18a83ab3d6))

- **security**: Enhance warning message
  ([`9596c89`](https://github.com/m-xim/aiogram-webhook/commit/9596c8936cf71e4141797f86991af1b23b709c86))

- **test**: Ver
  ([`4502da9`](https://github.com/m-xim/aiogram-webhook/commit/4502da9511d0dc83d78697ce2335f132c538e63f))

- **token**: Clear internal bot storage on shutdown
  ([`5b6c783`](https://github.com/m-xim/aiogram-webhook/commit/5b6c78302c74cce71f5622c6a21337f0b9ba00c4))

- **token**: Handle TokenValidationError in bot ID extraction
  ([`4a22cea`](https://github.com/m-xim/aiogram-webhook/commit/4a22cea12b1ef69f1834126c35137feb87e6cc31))

- **token**: Handle TokenValidationError in bot retrieval
  ([`72d3264`](https://github.com/m-xim/aiogram-webhook/commit/72d32640a751adb89d38fd6dc0f340ab4d6be754))

- **token**: Move BotConfig import from TYPE_CHECKING
  ([`82bb210`](https://github.com/m-xim/aiogram-webhook/commit/82bb210df2cf942fffa072b812d9c96f268c4d64))

- **token**: On_shutdown tasks
  ([`5371e89`](https://github.com/m-xim/aiogram-webhook/commit/5371e89ce4184c016ea0fce70ea1a3759a14edd8))

- **token**: Remove redundant bot clearing on shutdown
  ([`968f654`](https://github.com/m-xim/aiogram-webhook/commit/968f6547c5c69a84d54ed80b3facfc205f4eb3ba))

- **token**: Update on_startup method to use keyword-only arguments
  ([`9633886`](https://github.com/m-xim/aiogram-webhook/commit/9633886971923268c23e6ecdb366ff88de6448f4))

- **warnings**: Set stacklevel in security warning
  ([`9b6df43`](https://github.com/m-xim/aiogram-webhook/commit/9b6df4371c29c93ad0b27d5d35b679df5e90b9ad))

- **webhook**: Implement set_webhook method in base
  ([`94bd9dc`](https://github.com/m-xim/aiogram-webhook/commit/94bd9dcceed3ba216b2e8ef692d872a8ce206791))

- **webhook**: Only set secret_token param if not None
  ([`7dbe835`](https://github.com/m-xim/aiogram-webhook/commit/7dbe835c2b63927a34f8246f8db3334fce07d798))

- **webhook**: Remove unused webhook_config parameter from SingleBotEngine.set_webhook methods
  ([`08485c2`](https://github.com/m-xim/aiogram-webhook/commit/08485c296e8584af6be70969f01e07d24853bde2))

- **webhook**: Set default values for omitted parameters
  ([`51e30b8`](https://github.com/m-xim/aiogram-webhook/commit/51e30b8a589f4c0fd6fe06519239ed415efcc276))

### Chores

- Add badge for Codecov
  ([`f1e2056`](https://github.com/m-xim/aiogram-webhook/commit/f1e2056a355a30f4a9dbb26ea47f19e6bb2994c4))

- Simplify installation instructions in README
  ([`4b98ec9`](https://github.com/m-xim/aiogram-webhook/commit/4b98ec913cea9d61a61ca53054a37cd2529eeacf))

- Update
  ([`116164c`](https://github.com/m-xim/aiogram-webhook/commit/116164c14a1676c80fb38487a9435418c8868aef))

- Update security example with StaticSecretToken usage
  ([`230e1dd`](https://github.com/m-xim/aiogram-webhook/commit/230e1dd25e1b8bb24812bf8dc93957051eed38bf))

- **build**: Remove packages field from pyproject.toml
  ([`12cc4dd`](https://github.com/m-xim/aiogram-webhook/commit/12cc4ddb4e5a4b65a2f1410ff9108974f5dfac1e))

- **build**: Switch to uv_build backend and migrate ruff config to ruff.toml
  ([`25dcc43`](https://github.com/m-xim/aiogram-webhook/commit/25dcc432fe55f17801f819af343e772b2633087f))

- **ci**: Update actions/checkout and astral-sh/setup-uv versions in workflows
  ([`1e1468b`](https://github.com/m-xim/aiogram-webhook/commit/1e1468be0eaa5cf4eda12024fefb7e3c4a8a21c0))

- **pyproject**: Add support for Python 3.14
  ([`cb5e710`](https://github.com/m-xim/aiogram-webhook/commit/cb5e7106dace85d00ebcffb78d495fbcdf4a221f))

- **pyproject**: Relax aiogram and yarl version requirements
  ([`b8eb941`](https://github.com/m-xim/aiogram-webhook/commit/b8eb9415bd154672b11a65183c42177087cc1618))

- **pyproject**: Remove allow_zero_version setting
  ([`1ba993d`](https://github.com/m-xim/aiogram-webhook/commit/1ba993d1955d4a7a370b05177711f4a5a553768a))

### Code Style

- **simple, token**: Condense dispatcher event calls to single lines
  ([`55e997b`](https://github.com/m-xim/aiogram-webhook/commit/55e997b95564bfc76ffca43a92d2aab5481a3782))

### Documentation

- **CONTRIBUTING**: Add contributing guidelines
  ([`a0171c2`](https://github.com/m-xim/aiogram-webhook/commit/a0171c29730f7e3af9ff0d6277e97168ebee782a))

- **core**: Add and improve docstrings for adapters, routing, security, and checks
  ([`fee7007`](https://github.com/m-xim/aiogram-webhook/commit/fee70078491824607e85aaffc5ce258756c9f083))

- **example**: Add startup function to register webhook on bot initialization
  ([`d010e67`](https://github.com/m-xim/aiogram-webhook/commit/d010e67a4c3c4ace94aeb9b80465053646804bcf))

- **README**: Add badges for Ruff and Ty
  ([`2e3d882`](https://github.com/m-xim/aiogram-webhook/commit/2e3d882b33c09e7bcb1f5ddfa3d4b504c905b721))

- **README**: Correct
  ([`c3e8465`](https://github.com/m-xim/aiogram-webhook/commit/c3e8465fa509ff5e28a1336ab16908f9c0dfbe27))

- **README**: Update routing section for clarity and consistency
  ([`f2431c0`](https://github.com/m-xim/aiogram-webhook/commit/f2431c09d9bbb1ccc48066f79c2e680cf7f86f27))

### Features

- Docs
  ([`f5a89eb`](https://github.com/m-xim/aiogram-webhook/commit/f5a89eb9ac631f37116a118bfad1e5f01ff4dc82))

- **aiohttp, docs**: Add aiohttp optional dependency, update adapter import, and expand README with
  aiohttp usage and engine details
  ([`fbd7247`](https://github.com/m-xim/aiogram-webhook/commit/fbd72478d64df8171107222ced7c087c59875ae8))

- **base_mapping**: Implement len and iter in mapping interface
  ([`bc50c41`](https://github.com/m-xim/aiogram-webhook/commit/bc50c41e16b3d9bfac604e0867250049735c3a93))

- **ci**: Add type checking step with ty
  ([`c1f41e3`](https://github.com/m-xim/aiogram-webhook/commit/c1f41e3612f15e50087321616ddb18e347a62f1d))

- **docs**: Add 404
  ([`e84fd05`](https://github.com/m-xim/aiogram-webhook/commit/e84fd05a369693a74d8632a9b93ecc7bebf619ca))

- **docs**: New logo
  ([`9cde3a1`](https://github.com/m-xim/aiogram-webhook/commit/9cde3a13145bf72b4761ab65781e01ab627bed2b))

- **docs**: Update
  ([`f536d81`](https://github.com/m-xim/aiogram-webhook/commit/f536d81887e00d377023ed959f63c5c6a6e02e15))

- **docs**: Update diplodoc-cli realisation
  ([`15b14bd`](https://github.com/m-xim/aiogram-webhook/commit/15b14bd652dd56ccf7298174f9e6db3bc16116fb))

- **docs**: Update diplodoc-cli realisation 2
  ([`de0bd74`](https://github.com/m-xim/aiogram-webhook/commit/de0bd7485a3841ab065e68fde4472924c0246f4f))

- **docs**: Update README for improved clarity and feature description
  ([`21a3c3f`](https://github.com/m-xim/aiogram-webhook/commit/21a3c3fa076ca5f7588fea296a0cbba85cd5a5f9))

- **engine**: Big refactor webhook engine
  ([`c33d410`](https://github.com/m-xim/aiogram-webhook/commit/c33d410f8b6457a180e7653eceb1d47208ddabba))

- **engine**: Implement graceful shutdown handling and update startup methods
  ([`e638707`](https://github.com/m-xim/aiogram-webhook/commit/e6387070b6d3051c7374fe4ecb858b01a421c21c))

- **errors**: Add logs and errors
  ([`4648ded`](https://github.com/m-xim/aiogram-webhook/commit/4648ded126a24f118e80dbf8b2dc22d40c22ef88))

- **fastapi**: Implement lifespan management for FastAPI adapter
  ([`7ac6e9e`](https://github.com/m-xim/aiogram-webhook/commit/7ac6e9e69122f0446cd6e922b27f602537089bb3))

- **ip**: Add support for X-Forwarded-For header
  ([`3c80341`](https://github.com/m-xim/aiogram-webhook/commit/3c80341eb088b06414a201af2826324d0097ce8a))

- **route**: Add BotIdParam and BotTokenParam
  ([`e24764b`](https://github.com/m-xim/aiogram-webhook/commit/e24764bf10a1b17a50094eaed8d35cc47e90a8de))

- **route**: Add new one Route
  ([`2b456f0`](https://github.com/m-xim/aiogram-webhook/commit/2b456f070eb4604ae44e0752d6a5b7db1a708426))

- **route**: Add test
  ([`83d3081`](https://github.com/m-xim/aiogram-webhook/commit/83d308147ccd0ce7d521b22eb0f58ae96fa9b1bc))

- **route**: Big refactor
  ([`cc6010a`](https://github.com/m-xim/aiogram-webhook/commit/cc6010a26e4f8d0993d8c14b49a44f5233f2be3c))

- **route**: Enhance query normalization and improve error handling
  ([`78f0bda`](https://github.com/m-xim/aiogram-webhook/commit/78f0bda2ff86b34916024fafd581e579b5adb1a1))

- **routing**: Add default parameter name for PathRouting and QueryRouting
  ([`22b5379`](https://github.com/m-xim/aiogram-webhook/commit/22b5379e6be2aa6386433b8d8851706eb3b47f10))

- **routing**: Introduce TokenRouting and StaticRouting, refactor PathRouting and QueryRouting to
  inherit from TokenRouting
  ([`3a02200`](https://github.com/m-xim/aiogram-webhook/commit/3a022003d9b2cb228e03bd73344a308b876775f7))

- **secret_token**: Add secret token format validation and update tests
  ([`fb46f4d`](https://github.com/m-xim/aiogram-webhook/commit/fb46f4d4fc3def30f79cc293916b645a468bf233))

- **security**: Add test
  ([`fcefadf`](https://github.com/m-xim/aiogram-webhook/commit/fcefadfa1468329eb3dcf425d99f3b14a80c7621))

- **tasks**: Add TaskTracker
  ([`7596d51`](https://github.com/m-xim/aiogram-webhook/commit/7596d51db2d0bdf5232899fbf984e17202f49272))

- **test**: Add test analysis
  ([`05cae9e`](https://github.com/m-xim/aiogram-webhook/commit/05cae9e778a9669b332ef073cd669a97db93e38a))

- **tests**: Add pytest-cov for coverage reporting and integrate Codecov
  ([`6e43ad6`](https://github.com/m-xim/aiogram-webhook/commit/6e43ad66c9ace88a0c18643540afd07c1e65f27f))

- **tests**: Add Python 3.15
  ([`322859b`](https://github.com/m-xim/aiogram-webhook/commit/322859b6e7dd409b479f4d9ce446d9f1c04f394a))

- **tests**: Add StaticRouting tests and refactor PathRouting and QueryRouting tests
  ([`f45bb99`](https://github.com/m-xim/aiogram-webhook/commit/f45bb992597b5eca745fee1f6b5bd924ff4abd99))

- **tests**: Add tests
  ([`edb4cec`](https://github.com/m-xim/aiogram-webhook/commit/edb4cec773a1592b5fd0f0ce80faaab4bdff58e2))

- **tests**: Add tests for IPCheck with X-Forwarded-For header
  ([`a4b9517`](https://github.com/m-xim/aiogram-webhook/commit/a4b9517baf8fdd80cfcb4eca0ef309baf66dc678))

- **tests**: Refactoring and add new tests
  ([`9b86554`](https://github.com/m-xim/aiogram-webhook/commit/9b865546a90554d4724ca8e9264da052a5146b4d))

- **web**: Add support payload_response in fastapi
  ([`e0e80d7`](https://github.com/m-xim/aiogram-webhook/commit/e0e80d7666020c48fc57d9d29e7835a85c77ddc2))

- **webhook**: Add support multipart
  ([`03d0088`](https://github.com/m-xim/aiogram-webhook/commit/03d0088988da006457b00a0988ebcdbe160d1018))

- **webhook_config**: Add WebhookConfig for default webhook parameters and update engine interfaces
  ([`1b319e1`](https://github.com/m-xim/aiogram-webhook/commit/1b319e1bd2d0a340162acaa871cfaf7b43ae3fe6))

### Refactoring

- Move on_startup
  ([`519c7d2`](https://github.com/m-xim/aiogram-webhook/commit/519c7d2f4d7e7c4815bf726436e65c5fb7a204d9))

- Remove WebAdapter from public API exports
  ([`1ef8bbd`](https://github.com/m-xim/aiogram-webhook/commit/1ef8bbd03100191612feccd897a9509c403bc3fe))

- Security
  ([`9d36d2e`](https://github.com/m-xim/aiogram-webhook/commit/9d36d2e2a827171432b9c5f638b5d8092162f182))

- Simplify import statements and enhance lifecycle data structure
  ([`c9c3ad2`](https://github.com/m-xim/aiogram-webhook/commit/c9c3ad2c6e6ad57e1ec0456d8fc849d90020443d))

- Standardize terminology in CONTRIBUTING.md
  ([`5acee70`](https://github.com/m-xim/aiogram-webhook/commit/5acee7058a90ec13a800cee20d7f80cbd16e0a13))

- Standardize terminology in docstrings and update response handling
  ([`8ef42bf`](https://github.com/m-xim/aiogram-webhook/commit/8ef42bfdc05ba16ec31da4b6f32602726e1acd42))

- Tests
  ([`aed1f9d`](https://github.com/m-xim/aiogram-webhook/commit/aed1f9d88dc3ea484b295ec9fe820fab600981db))

- Unify response creation via WebAdapter and update BoundRequest interface
  ([`3f30edc`](https://github.com/m-xim/aiogram-webhook/commit/3f30edc82d3f9e9eaf653c90c99695e3bb5f9e93))

- Web
  ([`1bc6a0f`](https://github.com/m-xim/aiogram-webhook/commit/1bc6a0fb69fa93130b4b08e7ca95eb11389948a7))

- **adapters**: Cache headers and query params mappings in BoundRequest implementations
  ([`72c0216`](https://github.com/m-xim/aiogram-webhook/commit/72c02161a0f4767d233324faabc4c0fb01b30bf9))

- **adapters**: Unify BoundRequest interface and introduce framework-specific mappings
  ([`ca3693c`](https://github.com/m-xim/aiogram-webhook/commit/ca3693c104caab61c7cbc3b101cd611b9a2fbf97))

- **base**: Deprecate _get_bot_from_request and introduce _get_bot_for_request
  ([`4ec2bac`](https://github.com/m-xim/aiogram-webhook/commit/4ec2bac9139f95daf9520409bf910a6ce7e0aa2c))

- **base**: Move warning about security in __init__
  ([`e2a555f`](https://github.com/m-xim/aiogram-webhook/commit/e2a555fb9a12078fda7148853457a4654f80d5ba))

- **bot**: _ensure_bot_cached
  ([`a6647ef`](https://github.com/m-xim/aiogram-webhook/commit/a6647ef6a80aaf1a2c11d9b4c538ebd529f339f0))

- **bot**: Rename resolve_bot_from_request to _get_bot_from_request and update related methods
  ([`f31bd8c`](https://github.com/m-xim/aiogram-webhook/commit/f31bd8c1042affcd9cb4dc155226f95b4d5d765b))

- **BotConfig**: Enable slots in BotConfig
  ([`0374ace`](https://github.com/m-xim/aiogram-webhook/commit/0374aced2c9dd4f2e48a800d82115c9a78af3c39))

- **docs**: Add about new routing
  ([`8c62ad9`](https://github.com/m-xim/aiogram-webhook/commit/8c62ad97a93da4a7e4bb6cb5507d097262822b39))

- **FastAPI**: Rename FastAPI classes to FastApi for consistency
  ([`b890b86`](https://github.com/m-xim/aiogram-webhook/commit/b890b86e28d4dc4689a8e8216f3db36b828f39ac))

- **ip**: Refactoring
  ([`3292a0f`](https://github.com/m-xim/aiogram-webhook/commit/3292a0f2c3b074f5ad22a0d09e889605310a856a))

- **ip**: Unify IP retrieval methods and enhance X-Forwarded-For extraction
  ([`9e84588`](https://github.com/m-xim/aiogram-webhook/commit/9e845881726895b03eed2a1aa8fcf06078c2d4d8))

- **ip**: Unify IPAddress and IPNetwork types, update adapters and checks
  ([`8c26d7e`](https://github.com/m-xim/aiogram-webhook/commit/8c26d7e8f3f28c8a1b5dc0cc5b2d1929d1128688))

- **routing**: Convert methods to async
  ([`dc83170`](https://github.com/m-xim/aiogram-webhook/commit/dc83170a877375e90eb71f521f80a836ef4e601e))

- **routing**: Enhance URL handling and token extraction in routing classes
  ([`bc6f656`](https://github.com/m-xim/aiogram-webhook/commit/bc6f6566bdf7d03988d091e07538eabe7e015164))

- **routing**: Improve initialization and token handling in routing classes
  ([`84491ca`](https://github.com/m-xim/aiogram-webhook/commit/84491ca21e0571a8f657c1c830d5a6a7bdcb8b5a))

- **secret_token**: Change SecretToken from ABC to Protocol
  ([`66ecb5d`](https://github.com/m-xim/aiogram-webhook/commit/66ecb5dd9e10a8074b2727d4cb1252f4c0c2c33c))

- **secret_token**: Convert secret_token method to async
  ([`26f04cd`](https://github.com/m-xim/aiogram-webhook/commit/26f04cd1171837e8974fd5edbf08cd7a72682331))

- **security**: Remove redundant security checks and default to Security instance
  ([`5214a65`](https://github.com/m-xim/aiogram-webhook/commit/5214a657ab01e76e566b728de0c6ce11a23ea995))

- **security**: Rename Check protocol to SecurityCheck
  ([`f95ad95`](https://github.com/m-xim/aiogram-webhook/commit/f95ad955fd503c78168c60b68f01be374b0f1865))

- **security**: Rename token parameter to bot_token for clarity
  ([`8a5302c`](https://github.com/m-xim/aiogram-webhook/commit/8a5302c7415c730662e24bba2c3f15ed0fe7f1a9))

- **security**: Simplify security parameter handling in constructors
  ([`f134fd0`](https://github.com/m-xim/aiogram-webhook/commit/f134fd071b613a4661656d78594d9940bc517301))

- **security**: Update type hints for BoundRequest and clarify SecretToken docstring
  ([`e5a0509`](https://github.com/m-xim/aiogram-webhook/commit/e5a0509a91943aa1fd49bab9523ee817a956de0a))

- **security**: Update verify method to include dispatcher for security system
  ([`f56c164`](https://github.com/m-xim/aiogram-webhook/commit/f56c164cdf8be39105aea343f4351f69562f4bb7))

- **startup**: Update on_startup and on_shutdown methods to accept app argument
  ([`a4e624b`](https://github.com/m-xim/aiogram-webhook/commit/a4e624bed8f0aadd76e3266b7cd2f051a7748c95))

- **tasks**: Improve type annotations and error logging in TaskTracker
  ([`53e5158`](https://github.com/m-xim/aiogram-webhook/commit/53e51589ebba2ef9fa96ae155a23aef4012bc0b4))

- **tests**: Introduce DummyRequest and update DummyBoundRequest
  ([`abba2a0`](https://github.com/m-xim/aiogram-webhook/commit/abba2a09cc132e5d72016d8a2ec5136efe460647))

- **token**: Convert _get_bot_by_token to async
  ([`ad90c33`](https://github.com/m-xim/aiogram-webhook/commit/ad90c3359d800d9de317fb8514e74480edf62dbb))

- **token**: Remove docstring from _ensure_bot_cached method
  ([`68ca610`](https://github.com/m-xim/aiogram-webhook/commit/68ca610337c7ecfbc794124c99c3a2c50deed46b))

- **token**: Replace direct access to _bots with bots property
  ([`0c6dc2d`](https://github.com/m-xim/aiogram-webhook/commit/0c6dc2d4c58f8b3e9a2456e5a50b2588341cef85))

- **token**: Return a read-only bots using MappingProxyType
  ([`8db5918`](https://github.com/m-xim/aiogram-webhook/commit/8db5918ac4a535e1dee76a41444c7a83b5003f26))

- **token**: Use _bots attribute
  ([`70a7ff5`](https://github.com/m-xim/aiogram-webhook/commit/70a7ff53cb96425bd5fe44798a03b52920589834))

- **token**: Use BotConfig instance for bot initialization
  ([`aedd111`](https://github.com/m-xim/aiogram-webhook/commit/aedd111659bab4bdf1bbf6e403df675188c2a8c6))

- **webhook**: Simplify signature of on_startup and on_shutdown methods; add _build_workflow_data
  helper
  ([`a3ef6b6`](https://github.com/m-xim/aiogram-webhook/commit/a3ef6b6cfba127ac7c46e98f508559e937ff1c40))

- **webhook**: Streamline payload building and enhance file handling in webhook response
  ([`900ec00`](https://github.com/m-xim/aiogram-webhook/commit/900ec0079f56896e8ad86624dc82b13daca137f9))

- **WebhookEngine**: Make security optional and update secret token handling
  ([`e0d8fb3`](https://github.com/m-xim/aiogram-webhook/commit/e0d8fb393860a94f872bc9320210af2f4c4bd2ee))

- **WebhookEngine**: Pass parsed update dict instead of BoundRequest to handler methods
  ([`c50af89`](https://github.com/m-xim/aiogram-webhook/commit/c50af890a04b41223221b28edfc52f8177c787ab))

### Testing

- Refactoring
  ([`ba933d3`](https://github.com/m-xim/aiogram-webhook/commit/ba933d3f6ceb4080ff38e1936826bda5b810e235))

- **webhook**: Add tests for building webhook payload
  ([`6ace3e1`](https://github.com/m-xim/aiogram-webhook/commit/6ace3e1bc15b0486734fc4ec9102f7b50043b9ec))


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
