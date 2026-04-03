from app.config import Settings


class TestSettings:
    def test_openai_api_key_alias_is_supported(self):
        settings = Settings(_env_file=None, **{"OPENAI_API_KEY": "alias-key"})
        assert settings.minimax_api_key == "alias-key"

    def test_extra_environment_variables_are_ignored(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "alias-key")
        monkeypatch.setenv("UNRELATED_ENV", "ignored")

        settings = Settings(_env_file=None)

        assert settings.minimax_api_key == "alias-key"
