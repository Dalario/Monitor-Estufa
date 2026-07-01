"""API de monitoramento da estufa.

Recebe leituras dos sensores (temperatura, umidade e luz) enviadas pelo ESP32
e as armazena no Supabase. Também permite consultar o histórico.
"""

import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, status

from database import TABELA_LEITURAS, supabase
from schemas import Leitura, LeituraInput

load_dotenv()

API_KEY = os.environ.get("API_KEY")

app = FastAPI(
    title="Monitor Estufa API",
    description="Recebe e armazena as leituras dos sensores da estufa.",
    version="1.0.0",
)


def verificar_api_key(x_api_key: str = Header(..., description="Chave de acesso da API")):
    """Confere a chave enviada pelo ESP32 no header 'X-API-Key'."""
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API inválida.",
        )


@app.get("/", tags=["Status"])
def raiz():
    """Verifica rapidamente se a API está no ar."""
    return {"status": "ok", "servico": "Monitor Estufa API"}


@app.post(
    "/leituras",
    response_model=Leitura,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verificar_api_key)],
    tags=["Leituras"],
)
def criar_leitura(leitura: LeituraInput):
    """Registra uma nova leitura dos sensores no banco."""
    try:
        resposta = (
            supabase.table(TABELA_LEITURAS)
            .insert(leitura.model_dump())
            .execute()
        )
    except Exception as erro:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao gravar no Supabase: {erro}",
        )

    if not resposta.data:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Supabase não retornou o registro criado.",
        )

    return resposta.data[0]


@app.get("/leituras", response_model=list[Leitura], tags=["Leituras"])
def listar_leituras(limite: int = 50):
    """Retorna as leituras mais recentes (padrão: 50)."""
    limite = max(1, min(limite, 500))
    try:
        resposta = (
            supabase.table(TABELA_LEITURAS)
            .select("*")
            .order("criado_em", desc=True)
            .limit(limite)
            .execute()
        )
    except Exception as erro:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao consultar o Supabase: {erro}",
        )

    return resposta.data or []
