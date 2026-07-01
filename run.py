"""Inicia a API a partir da pasta principal do projeto.

Uso (de dentro de Monitor_Estufa):
    python run.py

Não precisa ativar o ambiente virtual nem entrar na pasta api: este script
acha o Python do .venv e a pasta certa sozinho.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.join(ROOT, "api")
VENV_PY = os.path.join(API_DIR, ".venv", "Scripts", "python.exe")


def main():
    # Se o ambiente virtual ainda não existe, avisa de forma clara.
    if not os.path.exists(VENV_PY):
        print("[ERRO] Ambiente virtual nao encontrado em api\\.venv")
        print("Crie com:")
        print("  cd api")
        print("  python -m venv .venv")
        print("  .venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        sys.exit(1)

    # Se este script não está rodando com o Python do .venv (ex.: foi chamado
    # com o Python global), re-executa a si mesmo usando o Python do .venv.
    if os.path.normcase(sys.executable) != os.path.normcase(VENV_PY):
        sys.exit(subprocess.call([VENV_PY, os.path.abspath(__file__)]))

    # Daqui em diante estamos no Python do .venv (uvicorn disponível).
    os.chdir(API_DIR)
    sys.path.insert(0, API_DIR)

    import uvicorn

    porta = int(os.environ.get("PORT", 8000))
    print("Iniciando a API... Documentacao: http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=porta, reload=True)


if __name__ == "__main__":
    main()
