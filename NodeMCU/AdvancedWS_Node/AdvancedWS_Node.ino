#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <PubSubClient.h> 

#define TAMANHO_STRING_SERIAL      ((4*8) + 7 + 1)  //8 canais (de 4 bytes de informação cada, em ASCII) e 7 separadores (;) e terminador de string (\0)
 
#define ONE_WIRE_BUS1 D1
OneWire oneWire1(ONE_WIRE_BUS1);
DallasTemperature sensor0(&oneWire1);

#define DHTTYPE DHT11
uint8_t DHTPin = D2;
DHT dht(DHTPin, DHTTYPE);
 
#define NTP_OFFSET   60 * 60      // In seconds
#define NTP_INTERVAL 60 * 1000    // In miliseconds
#define NTP_ADDRESS  "a.st1.ntp.br"
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, NTP_ADDRESS, NTP_OFFSET, NTP_INTERVAL);

const char *host   = "192.168.0.106";
const int httpPort = 5000;
const int   led    = D7;

int estacao   = 1;
String versao = "1.2";
String token  = "";

int ldrPin   = A0;
int tmp      = 80;
int ldrValor = 0;

String data = "";
String str  = "";

float  t, h, l, c;
float  tempC1, temp0, altit, pres0;

WiFiClient espClient;
PubSubClient MQTT(espClient);
char StringLeiturasADC[TAMANHO_STRING_SERIAL];

void initWiFi(void);
void reconectWiFi(void); 
bool VerificaSerial(void);
void EnviaInformacoes(void);

void initWiFi() {
    delay(10);
    reconectWiFi();
}

void reconectWiFi() {
  const char *ssid     = "Katena's House";
  const char *password = "aruazI_sirC@13";
  WiFi.begin(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(led, HIGH);
    delay(100);
    digitalWrite(led, LOW);
    Serial.print( "." );
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

bool VerificaSerial() {
  char c;
  int  i;
   
  if (Serial.available() <= 0)
    return false;

  //há dados sendo recebidos. Limpa buffer de recepção:
  memset(StringLeiturasADC, 0, TAMANHO_STRING_SERIAL);
  
  i = 0;
  do {
    c = Serial.read();
    if (c != '\0') {
      StringLeiturasADC[i] = c;
      i++;
    }
  } while (c != '\0');
  Serial.println("");
  return true;  
}
 
void EnviaInformacoes(void) {
  Serial.println(StringLeiturasADC);
  String thisString1 = String(StringLeiturasADC);
  EncontraValor(thisString1, "Pressao", "pressao",   thisString1.indexOf("Pressao", 0), thisString1.indexOf("Pressao", 0)+7, 10000);
  EncontraValor(thisString1, "Solo",    "umid_solo", thisString1.indexOf("Solo",   23), thisString1.indexOf("Solo",   23)+4, 0);
  EncontraValor(thisString1, "Chuva",   "chuva",     thisString1.indexOf("Chuva",  37), thisString1.indexOf("Chuva",  37)+5, 0);
  EncontraValor(thisString1, "Som",     "som",       thisString1.indexOf("Som",    52), thisString1.indexOf("Som",    52)+3, 0);
}

void EncontraValor(String str1, String str2, String str3, int inicio, int fim, int limite) {
  int pos = 0;
  String temp = "";
  if (str2 == "Pressao") {
    pos = str1.indexOf("Pressao", 0);
    Serial.println(pos);
    if (pos > 0) {
      str1 = str1.substring(pos);
      Serial.println(str1);
    }
    else if (pos == 0) {
      temp = str1.substring(1);
      pos  = temp.indexOf("Pressao", 0);
      if (pos > 0) {
        Serial.println(pos);
        str1 = temp.substring(pos);
      }
    }
    Serial.println(str1);
  }

  if (str1.substring(inicio, fim) == str2) {
    Serial.print(str2);
    str2 = str1.substring(fim+2, fim+8);
    Serial.print(": ");
    if (str2.toFloat() > limite)
      EnviaDados(str2.toFloat(), str3, estacao);
  }
  else {
    Serial.print(str2);
    Serial.println(": ");
    Serial.print("NÃO Achou Substring ");
    Serial.println(str1.substring(inicio, fim));
  }
}

void EnviaDados(float valor, String tipo, int estacao) {
  WiFiClient client;
  timeClient.update();
  
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
      
  String formattedTime    = timeClient.getFormattedTime();
  unsigned long epcohTime = timeClient.getEpochTime();
  
  data  = "{\"valor\": " + String(valor) + ", \"datahora\": " + String(epcohTime) + "}";
/*  
  json=
  {
    "valor": 304.00, 
    "datahora": 1607109786
  },
  headers=
  {
    "Authorization": "jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDcxOTI0NzUsImlhdCI6MTYwNzEwNjA3NSwibmJmIjoxNjA3MTA2MDc1LCJpZGVudGl0eSI6MX0.gpFQ_KaX0DFd3ps8VHK7E5ly5L0doueUSbaYptgQVHI"
  }
*/
  client.println("POST /api/v" + versao + "/sensor/" + String(estacao) + "/" + tipo + " HTTP/1.1");
  client.print("Host: ");
  client.println(host);
  client.println("Accept: */*");
  client.println("Content-Type: application/json");
  client.print("Authorization: ");
  client.println(token);
  client.print("Content-Length: ");
  client.println(data.length());
  
  client.println();
  client.print(data);
  
  Serial.println(token);
  Serial.println(data);

  delay(20); // Can be changed
  if (client.connected()) { 
    client.stop();  // DISCONNECT FROM THE SERVER
  }
  delay(20);
}

String RecebeToken() {
  WiFiClient client;
  String line, token2;
  
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return "Erro ao conectar";
  }
  
  data = "{\"email\": \"admin@gmail.com\", \"password\": \"12345678\"}";

  client.println("POST /token HTTP/1.1");
  client.print("Host: ");
  client.println(host);
  client.println("Accept: */*");
  client.println("Content-Type: application/json");
  client.print("Content-Length: ");
  client.println(data.length());
  client.println();
  client.print(data);

  delay(20); // Can be changed
  while (client.connected()) {
    if (client.available()) {
      line = client.readStringUntil('\n');
      if (line.indexOf("HTTP", 0) > 0) {
        Serial.print("[Response:]");
        Serial.println(line.substring(0, 15));
      }
      if (line.indexOf("access_token", 0) > 0) 
        token2 = "\"jwt " + line.substring(line.indexOf("access_token", 0)+16);
    }
  }
  delay(20);
  return token2;
}

void setup() {
  Serial.begin(115200);
  
  initWiFi();
  
  sensor0.begin();
  if (sensor0.getDeviceCount() == 0)
    Serial.println("Sensor temperatura da água não encontrado");
  
  timeClient.begin();
  
  pinMode(led,    OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(DHTPin, INPUT);

  dht.begin();
  
  token = RecebeToken();
  Serial.print("Token: ");
  Serial.println(token);
  
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
  delay(100);
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
  delay(100);
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
}

void loop() {
  VerificaSerial();
  EnviaInformacoes();
 
  sensor0.requestTemperatures();
  tempC1 = sensor0.getTempCByIndex(0);

  ldrValor = analogRead(ldrPin);
  l = 1024 - ldrValor;

  t = dht.readTemperature();
  h = dht.readHumidity();

  digitalWrite(led, HIGH);
  delay(10);
  digitalWrite(led, LOW);
  delay(10);

  Serial.print("Temperatura Amb.: ");
  EnviaDados(t, "temp_ambiente", estacao);
  Serial.print("Temperatura Água: ");
  EnviaDados(tempC1, "temp_agua", estacao);
  Serial.print("Umidade Relativa: ");
  EnviaDados(h, "umid_relativa", estacao);
  Serial.print("Luminosidade:     ");
  EnviaDados(l, "luminosidade", estacao);
}
