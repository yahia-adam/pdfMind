import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    # On récupère les valeurs brutes du .env d'abord
    root_dir: str = os.getenv("ROOT_DIR")
    train_data_name: str = os.getenv("TRAIN_DATA_DIR")
    test_data_name: str = os.getenv("TEST_DATA_DIR")
    chroma_db_name: str = os.getenv("CHROMA_DB_DIR")

    # Models
    chat_model_name: str = os.getenv("CHAT_MODEL_NAME")
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME")

    # LangSmith
    langsmith_endpoint: str = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY")
    langsmith_tracing: bool = os.getenv("LANGSMITH_TRACING", False)

    app_name: str = os.getenv("APP_NAME", "QualiBot")
    debug_mode: bool = os.getenv("DEBUG_MODE", False)

    @property
    def train_data_dir(self) -> str:
        return os.path.join(self.root_dir, self.train_data_name)

    @property
    def test_data_dir(self) -> str:
        return os.path.join(self.root_dir, self.test_data_name)

    @property
    def chroma_db_dir(self) -> str:
        return os.path.join(self.root_dir, self.chroma_db_name)

settings = Settings()