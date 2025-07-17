from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "綜合人格特質分析平台"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings() 