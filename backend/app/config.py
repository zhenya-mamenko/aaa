from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    app_name: str = ""
    database_import_data_dir: str = "db/data/"
    database_path: str = "db/aaa.db"
    database_schema_dir: str = "db/sql/"
    environment: str = ""
    github_link: str = ""
    version: str = ""


settings = Settings()
settings = Settings(_env_file=f".env{'.' + settings.environment if settings.environment else ''}", _env_file_encoding="utf-8")
settings.app_name = "Assets Allocation App"
settings.github_link = "https://github.com/zhenya-mamenko/aaa"

with open("VERSION") as f:
    settings.version = f.read().strip()
