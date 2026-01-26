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
    # Models Configuration
    model_provider: str = os.getenv("MODEL_PROVIDER", "ollama")

    # Ollama Settings
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_chat_model_name: str = os.getenv("OLLAMA_CHAT_MODEL_NAME", "mistral-nemo:latest")
    ollama_embedding_model_name: str = os.getenv("OLLAMA_EMBEDDING_MODEL_NAME", "mistral-nemo:latest")

    # OpenAI Settings
    openai_url: str = os.getenv("OPENAI_URL", "https://api.openai.com/v1")
    openai_chat_model_name: str = os.getenv("OPENAI_CHAT_MODEL_NAME", "gpt-3.5-turbo")
    openai_embedding_model_name: str = os.getenv("OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-ada-002")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    @property
    def chat_model_name(self) -> str:
        if self.model_provider == "openai":
            return self.openai_chat_model_name
        return self.ollama_chat_model_name

    @property
    def embedding_model_name(self) -> str:
        if self.model_provider == "openai":
            return self.openai_embedding_model_name
        return self.ollama_embedding_model_name

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