#include <Arduino.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>

// ===================== CONFIGURAÇÃO =====================
// Preencha com os dados da sua rede Wi-Fi.
const char* WIFI_SSID     = "NOME_DA_SUA_REDE";
const char* WIFI_PASSWORD = "SENHA_DO_WIFI";

// Endereço da sua API FastAPI (use o IPv4 do PC que roda a API, veja `ipconfig`).
// Exemplo: "http://192.168.0.15:8000/leituras"
const char* API_URL = "http://192.168.0.15:8000/leituras";

// Mesma chave definida em API_KEY no arquivo .env da API.
const char* API_KEY = "troque-esta-chave-secreta";

// Intervalo entre envios (em milissegundos). 30000 = 30 segundos.
const unsigned long INTERVALO_ENVIO = 30000;
// =======================================================

// Definição dos pinos escolhidos
#define DHTPIN 5        // Pino digital D5 para o sensor DHT11
#define LDRPIN 33       // Pino analógico D33 para o sensor de luz (ADC1)

// Definição correta do modelo do sensor
#define DHTTYPE DHT11

// Inicialização do sensor DHT
DHT dht(DHTPIN, DHTTYPE);

void conectarWiFi() {
  Serial.print("A ligar ao Wi-Fi");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Tenta ligar por até ~15 segundos
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 30) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("\nWi-Fi ligado! IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha ao ligar ao Wi-Fi. Vai tentar novamente mais tarde.");
  }
}

// Envia as leituras para a API. Devolve true se recebeu resposta 2xx.
bool enviarLeitura(float temperatura, float humidade, float luz) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Sem Wi-Fi; a tentar reconectar...");
    conectarWiFi();
    if (WiFi.status() != WL_CONNECTED) return false;
  }

  HTTPClient http;
  http.begin(API_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", API_KEY);

  // Monta o corpo JSON manualmente (sem bibliotecas extras).
  char corpo[128];
  snprintf(corpo, sizeof(corpo),
           "{\"temperatura\":%.1f,\"umidade\":%.1f,\"luz\":%.1f}",
           temperatura, humidade, luz);

  int codigo = http.POST((uint8_t*)corpo, strlen(corpo));

  if (codigo > 0) {
    Serial.print("API respondeu: ");
    Serial.println(codigo);
  } else {
    Serial.print("Erro no POST: ");
    Serial.println(http.errorToString(codigo));
  }

  http.end();
  return codigo >= 200 && codigo < 300;
}

void setup() {
  // Inicializa a comunicação serial a 115200 bps
  Serial.begin(115200);
  Serial.println("--- Monitorização da Estufa Iniciada ---");

  // Inicializa o sensor DHT11
  dht.begin();

  // Configura o pino do LDR como entrada
  pinMode(LDRPIN, INPUT);

  // Liga ao Wi-Fi
  conectarWiFi();
}

void loop() {
  // Leitura dos dados do DHT11
  float humidade = dht.readHumidity();
  float temperatura = dht.readTemperature();

  // Validação da leitura do sensor de clima
  if (isnan(humidade) || isnan(temperatura)) {
    Serial.println("Erro crítico: Falha ao ler o sensor DHT11!");
    delay(2000);
    return;
  }

  // Leitura analógica do LDR (retorna um valor entre 0 e 4095)
  int luzBruta = analogRead(LDRPIN);

  // Conversão matemática do valor bruto para uma percentagem estimada (0% a 100%)
  // Nota: Se o comportamento inverter (marcar 100% no escuro), altere para: map(luzBruta, 0, 4095, 0, 100)
  float percentagemLuz = map(luzBruta, 4095, 0, 0, 100);

  // Transmissão dos dados estruturados para o Monitor Serial
  Serial.print("Humidade do Ar: ");
  Serial.print(humidade);
  Serial.print("% | ");

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print("°C | ");

  Serial.print("Incidência de Luz: ");
  Serial.print(percentagemLuz);
  Serial.println("%");

  // Envia os dados para a API/Supabase
  enviarLeitura(temperatura, humidade, percentagemLuz);

  // Aguarda antes da próxima leitura/envio
  delay(INTERVALO_ENVIO);
}
