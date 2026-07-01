"""Configuração do cliente Supabase, lido a partir das variáveis de ambiente."""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL e SUPABASE_KEY precisam estar definidas no arquivo .env "
        "(veja o .env.example)."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Nome da tabela onde as leituras são gravadas.
TABELA_LEITURAS = "leituras"
