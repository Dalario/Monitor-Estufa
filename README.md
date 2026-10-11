<div align="center">

# 🌱 Monitor Estufa

**Monitoramento de estufa em tempo real com ESP32, FastAPI e Supabase**

Sensores de temperatura, umidade e luz enviando leituras para a nuvem a cada 30 segundos.

![ESP32](https://img.shields.io/badge/ESP32-Arduino-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![PlatformIO](https://img.shields.io/badge/PlatformIO-F5822A?style=for-the-badge&logo=platformio&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

</div>

---

## 📖 Sobre o projeto

O **Monitor Estufa** é um sistema IoT ponta a ponta para acompanhar as condições de uma estufa. Um **ESP32** lê os sensores, envia os dados via Wi-Fi para uma **API REST em FastAPI**, que valida, autentica e grava tudo no **Supabase (PostgreSQL)**. O histórico fica disponível para consulta a qualquer momento.

### ✨ Funcionalidades

- 🌡️ **Temperatura** e 💧 **umidade do ar** com sensor DHT11
- ☀️ **Incidência de luz** (0–100%) com sensor LDR
- 📡 Envio automático das leituras a cada **30 segundos**
- 🔁 Reconexão automática ao Wi-Fi em caso de queda
- 🔐 Autenticação do dispositivo via header `X-API-Key`
- ✅ Validação dos dados com Pydantic (faixas de valores aceitas)
- 🗄️ Armazenamento em PostgreSQL (Supabase) com **RLS ativado**
- 📚 Documentação interativa automática (Swagger em `/docs`)
- ☁️ Pronto para deploy no **Railway** (HTTPS) ou execução local (HTTP)

---

## 🏗️ Arquitetura

```
┌──────────────────┐   HTTP(S) POST /leituras   ┌──────────────────┐   insert / select   ┌──────────────────┐
│      ESP32       │ ─────────────────────────▶ │     FastAPI      │ ──────────────────▶ │     Supabase     │
│  DHT11  +  LDR   │   JSON + X-API-Key         │ (Railway / local)│                     │   (PostgreSQL)   │
└──────────────────┘                            └──────────────────┘                     └──────────────────┘
```

---

## 🧰 Tecnologias

| Camada      | Stack                                                                 |
|-------------|-----------------------------------------------------------------------|
| Firmware    | C++ (Arduino framework), PlatformIO, Adafruit DHT sensor library      |
| Backend     | Python 3.12, FastAPI, Uvicorn, Pydantic, python-dotenv                |
| Banco       | Supabase (PostgreSQL) com Row Level Security                          |
| Deploy      | Railway (via `Procfile`)                                              |

---

## 🔌 Hardware

| Componente            | Pino no ESP32 | Observação                         |
|-----------------------|---------------|------------------------------------|
| Sensor DHT11 (dados)  | `GPIO 5`      | Temperatura e umidade              |
| Sensor LDR (analógico)| `GPIO 33`     | Canal ADC1 (compatível com Wi-Fi)  |

> ⚠️ O ESP32 só conecta em redes **2.4 GHz**.

---

## 📁 Estrutura do repositório

```
Monitor-Estufa/
├── src/
│   └── main.cpp              # Firmware do ESP32 (leitura dos sensores + envio)
├── include/
│   └── secrets.example.h     # Modelo de credenciais (Wi-Fi, URL e chave da API)
├── api/
│   ├── main.py               # Rotas da API (FastAPI)
│   ├── schemas.py            # Modelos Pydantic de entrada/saída
│   ├── database.py           # Cliente Supabase
│   ├── supabase_schema.sql   # Script de criação da tabela
│   ├── requirements.txt      # Dependências Python
│   ├── Procfile              # Comando de start no Railway
│   └── .env.example          # Modelo de variáveis de ambiente
├── run.py                    # Atalho para subir a API localmente
└── platformio.ini            # Configuração do PlatformIO (esp32dev)
```

---

## 🚀 Como rodar

### 1. Banco de dados (Supabase)

1. Crie um projeto em [supabase.com](https://supabase.com).
2. Vá em **SQL Editor → New query**, cole o conteúdo de [`api/supabase_schema.sql`](api/supabase_schema.sql) e clique em **Run**.

### 2. API (FastAPI)

```bash
cd api
cp .env.example .env        # no Windows: copy .env.example .env
```

Preencha o `.env`:

| Variável       | Onde encontrar                                                          |
|----------------|-------------------------------------------------------------------------|
| `SUPABASE_URL` | Supabase → Project Settings → API                                       |
| `SUPABASE_KEY` | Chave **`service_role`** (secreta — nunca coloque no ESP32)             |
| `API_KEY`      | Invente uma chave aleatória; o ESP32 vai usá-la para se autenticar      |

Instale e execute:

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> 💡 No Windows, depois de criar o `.venv`, basta rodar `python run.py` na raiz do projeto.

Acesse a documentação em **http://localhost:8000/docs**.

#### Deploy no Railway

Aponte o serviço para a pasta `api/`, defina as variáveis `SUPABASE_URL`, `SUPABASE_KEY` e `API_KEY` e pronto — o `Procfile` cuida do start.

### 3. Firmware (ESP32)

1. Copie `include/secrets.example.h` para `include/secrets.h` e preencha:

   ```cpp
   #define WIFI_SSID     "NOME_DA_SUA_REDE"
   #define WIFI_PASSWORD "SENHA_DO_WIFI"
   #define API_URL       "https://SEU-PROJETO.up.railway.app/leituras"  // ou http://192.168.x.x:8000/leituras
   #define API_KEY       "mesma-chave-do-.env"
   ```

2. Abra o projeto no **VS Code + PlatformIO**, compile e grave no ESP32.
3. Abra o **Serial Monitor** (115200 bps) para acompanhar as leituras e as respostas da API.

> O firmware detecta sozinho se a URL é `http` ou `https` e escolhe o cliente adequado.

---

## 📡 Endpoints

| Método | Rota                     | Descrição                                   | Autenticação       |
|--------|--------------------------|---------------------------------------------|--------------------|
| `GET`  | `/`                      | Status da API                               | —                  |
| `POST` | `/leituras`              | Registra uma nova leitura                   | Header `X-API-Key` |
| `GET`  | `/leituras?limite=50`    | Lista as leituras mais recentes (máx. 500)  | —                  |

**Exemplo de envio:**

```bash
curl -X POST http://localhost:8000/leituras \
  -H "Content-Type: application/json" \
  -H "X-API-Key: SUA_API_KEY" \
  -d '{"temperatura": 24.5, "umidade": 60, "luz": 80}'
```

**Resposta (`201 Created`):**

```json
{
  "id": 1,
  "temperatura": 24.5,
  "umidade": 60.0,
  "luz": 80.0,
  "criado_em": "2026-10-11T19:30:00.000000+00:00"
}
```

**Faixas aceitas:** temperatura de −40 a 100 °C · umidade de 0 a 100% · luz de 0 a 100%.

---

## 🔐 Segurança

- Credenciais do firmware (`secrets.h`) e da API (`.env`) ficam **fora do Git**.
- A chave `service_role` do Supabase existe **apenas no servidor**.
- A tabela `leituras` tem **RLS ativado sem políticas públicas**, então a chave `anon` não lê nem escreve direto no banco.
- O ESP32 se autentica na API com uma chave própria (`X-API-Key`).

---

## 🗺️ Próximos passos

- [ ] Dashboard web com gráficos do histórico
- [ ] Alertas (temperatura/umidade fora da faixa ideal)
- [ ] Validação do certificado TLS no ESP32
- [ ] Proteger também a rota `GET /leituras`
- [ ] Sensor de umidade do solo

---

<div align="center">

Feito com 💚 por **[Dalario](https://github.com/Dalario)**

</div>
