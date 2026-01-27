import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    # On récupère les valeurs brutes du .env d'abord
    train_data_dir: str = os.getenv("TRAIN_DATA_DIR")
    test_data_dir: str = os.getenv("TEST_DATA_DIR")
    chroma_db_dir: str = os.getenv("CHROMA_DB_DIR")

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

    # verify models
    if (self.model_provider == "openai"):
        if (self.openai_api_key == ""):
            raise ValueError("OPENAI_API_KEY is not set")
        if (self.openai_url == ""):
            raise ValueError("OPENAI_URL is not set")
        if (self.openai_chat_model_name == ""):
            raise ValueError("OPENAI_CHAT_MODEL_NAME is not set")
        if (self.openai_embedding_model_name == ""):
            raise ValueError("OPENAI_EMBEDDING_MODEL_NAME is not set")
    elif (self.model_provider == "ollama"):
        if (self.ollama_chat_model_name == ""):
            raise ValueError("OLLAMA_CHAT_MODEL_NAME is not set")
        if (self.ollama_embedding_model_name == ""):
            raise ValueError("OLLAMA_EMBEDDING_MODEL_NAME is not set")
    else:
        raise ValueError("MODEL_PROVIDER is not set")

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

    app_name: str = os.getenv("APP_NAME", "QualiBat")
    debug_mode: bool = os.getenv("DEBUG_MODE", False)

settings = Settings()