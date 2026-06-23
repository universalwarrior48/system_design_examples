"""
Configuration settings for all services.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Service Settings
    service_name: str = "ecommerce-service"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ecommerce"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 300  # 5 minutes
    
    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    token_expire_minutes: int = 30
    
    # Prometheus
    metrics_enabled: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
