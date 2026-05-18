from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Target:
    bot_id: int
    bot_token: str
