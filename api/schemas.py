"""Modelos de dados (Pydantic) para validação de entrada e saída da API."""

from datetime import datetime

from pydantic import BaseModel, Field


class LeituraInput(BaseModel):
    """Dados que o ESP32 envia ao registrar uma leitura."""

    temperatura: float = Field(..., ge=-40, le=100, description="Temperatura em °C")
    umidade: float = Field(..., ge=0, le=100, description="Umidade do ar em %")
    luz: float = Field(..., ge=0, le=100, description="Incidência de luz em %")

    model_config = {
        "json_schema_extra": {
            "example": {"temperatura": 24.5, "umidade": 60.0, "luz": 80.0}
        }
    }


class Leitura(LeituraInput):
    """Leitura completa, como está armazenada no banco."""

    id: int
    criado_em: datetime
