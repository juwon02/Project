"""환경변수를 한 곳에서 로드해 나머지 코드가 os.getenv를 직접 쓰지 않게 한다."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    openai_api_key: str = ""
    cors_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        # uvicorn을 backend/ 에서 실행하는 것을 기준으로, 프로젝트 루트의 .env를 가리킨다.
        env_file="../.env",
        env_file_encoding="utf-8",
    )


settings = Settings()
