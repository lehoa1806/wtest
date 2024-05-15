from __future__ import annotations

import os


class Env:
    @classmethod
    def get_environment_variable(
        cls,
        env: str,
        default=None,
        require=False,
    ) -> str:
        val = os.getenv(env) or default
        if val is None and require:
            raise Exception(f'Environment variable [{env}] not available')
        return val

    # Global configuration
    @property
    def app_domain(self) -> str | None:
        return self.get_environment_variable('APP_DOMAIN')

    @property
    def debug(self) -> str | None:
        return self.get_environment_variable('DEBUG')
