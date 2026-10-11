from pydantic import BaseModel, Field, SecretStr


class DatabaseSettings(BaseModel):
    url: str = Field(default="")
    secret_key: SecretStr | None = Field(default=None)
