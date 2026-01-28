import os
from typing import Optional
from pydantic import model_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configuration de Pydantic pour lire le fichier .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Chemins
    train_data_dir: str
    test_data_dir: str
    chroma_db_dir: str

    # Modèle Global
    model_provider: str = "openai"  # Valeur par défaut

    # Ollama Settings
    ollama_url: str = "http://localhost:11434"
    ollama_chat_model_name: str = "mistral-nemo:latest"
    ollama_embedding_model_name: str = "mistral-nemo:latest"

    # OpenAI Settings
    openai_url: str = "https://api.openai.com/v1"
    openai_chat_model_name: str = "gpt-3.5-turbo"
    openai_embedding_model_name: str = "text-embedding-ada-002"
    openai_api_key: Optional[str] = None

    # LangSmith
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_api_key: Optional[str] = None
    langsmith_tracing: bool = False

    app_name: str = "QualiBat"
    debug_mode: bool = False

    # Logique de validation
    @model_validator(mode='after')
    def verify_models(self) -> 'Settings':
        if self.model_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY must be set when provider is 'openai'")
        elif self.model_provider == "ollama":
            if not self.ollama_chat_model_name or not self.ollama_embedding_model_name:
                raise ValueError("Ollama model names must be set")
        else:
            raise ValueError(f"Unknown model_provider: {self.model_provider}")
        return self

    @property
    def chat_model_name(self) -> str:
        return self.openai_chat_model_name if self.model_provider == "openai" else self.ollama_chat_model_name

    @property
    def embedding_model_name(self) -> str:
        return self.openai_embedding_model_name if self.model_provider == "openai" else self.ollama_embedding_model_name

# Instanciation unique
settings = Settings()