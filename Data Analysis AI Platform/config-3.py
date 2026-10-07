from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Data Analyst Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION_32_BYTES_MIN"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/aidataanalyst"
    REDIS_URL: str = "redis://localhost:6379/0"

    LLM_PROVIDER: str = "openai"  # or anthropic, mock
    LLM_API_KEY: str = "mock-key"

    DEFAULT_ROW_LIMIT: int = 1000
    DEFAULT_QUERY_TIMEOUT: int = 30
    JOIN_THRESHOLD_APPROVAL: int = 3

    class Config:
        env_file = ".env"

settings = Settings()
