# Monitor Estufa — API

FastAPI que recebe as leituras dos sensores da estufa (temperatura, umidade e luz)
enviadas pelo ESP32 e as armazena no **Supabase**.

Arquitetura: `ESP32 → FastAPI → Supabase`.

## 1. Criar a tabela no Supabase

1. Crie um projeto em [supabase.com](https://supabase.com).
2. No painel, vá em **SQL Editor → New query**, cole o conteúdo de
   [`supabase_schema.sql`](supabase_schema.sql) e clique em **Run**.

## 2. Configurar as variáveis de ambiente

1. Copie o exemplo:

   ```powershell
   copy .env.example .env
   ```

2. Preencha o `.env`:
   - `SUPABASE_URL` e `SUPABASE_KEY` → em **Project Settings → API**
     (use a chave **`service_role`**, a secreta).
   - `API_KEY` → invente uma chave secreta; o ESP32 vai enviá-la para se autenticar.

## 3. Instalar e rodar

```powershell
cd api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- Documentação interativa (Swagger): http://localhost:8000/docs
- `--host 0.0.0.0` deixa a API acessível para o ESP32 na mesma rede Wi-Fi.

## 4. Testar rápido

```powershell
curl.exe -X POST http://localhost:8000/leituras `
  -H "Content-Type: application/json" `
  -H "X-API-Key: SUA_API_KEY" `
  -d '{"temperatura": 24.5, "umidade": 60, "luz": 80}'
```

## Endpoints

| Método | Rota         | Descrição                          | Autenticação    |
|--------|--------------|------------------------------------|-----------------|
| GET    | `/`          | Status da API                      | —               |
| POST   | `/leituras`  | Registra uma leitura dos sensores  | Header `X-API-Key` |
| GET    | `/leituras`  | Lista as leituras mais recentes    | —               |

## Descobrir o IP do PC (para configurar no ESP32)

```powershell
ipconfig
```

Use o **IPv4 Address** da sua rede Wi-Fi (algo como `192.168.x.x`) no firmware.
