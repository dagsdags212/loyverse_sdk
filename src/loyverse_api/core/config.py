from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Config(BaseSettings):
    loyverse_api_key: str
    db_url: str
    limit: int = 50
    timezone: str = "Asia/Manila"


config = Config()
