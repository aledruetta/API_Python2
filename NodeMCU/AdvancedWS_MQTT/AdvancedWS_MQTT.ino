#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <PubSubClient.h> // Importa a Biblioteca PubSubClien
 
//defines:
//defines de id mqtt e tópicos para publicação e subscribe
#define TOPICO_PUBLISH   "MQTTNodeMCUAnalogicoEnvia"    //tópico MQTT de envio de informações para Broker
                                                        //IMPORTANTE: recomendamos fortemente alterar os nomes
                                                        //            desses tópicos. Caso contrário, há grandes
                                                        //            chances de você controlar e monitorar o NodeMCU
                                                        //            de outra pessoa.
#define ID_MQTT  "NodeMCUAnalogico"     //id mqtt (para identificação de sessão)
                                        //IMPORTANTE: este deve ser único no broker (ou seja, 
                                        //            se um client MQTT tentar entrar com o mesmo 
                                        //            id de outro já conectado ao broker, o broker 
                                        //            irá fechar a conexão de um deles).
 
#define TAMANHO_STRING_SERIAL      ((4*8) + 7 + 1)  //8 canais (de 4 bytes de informação cada, em ASCII) e 7 separadores (;) e terminador de string (\0)
 
#define ONE_WIRE_BUS1 D1
OneWire oneWire1(ONE_WIRE_BUS1);
DallasTemperature sensor0(&oneWire1);

#define DHTTYPE DHT11 // DHT11
uint8_t DHTPin = D2;
DHT dht(DHTPin, DHTTYPE);
 
#define NTP_OFFSET   60 * 60      // In seconds
#define NTP_INTERVAL 60 * 1000    // In miliseconds
#define NTP_ADDRESS  "a.st1.ntp.br"
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, NTP_ADDRESS, NTP_OFFSET, NTP_INTERVAL);

const char *host = "192.168.0.113";
const int   led  = D7;

int estacao  = 1;
int ldrPin   = A0;
int tmp      = 80;
int ldrValor = 0;

String data = "";
String str  = "";

float  t, h, l, c;
float  tempC1, temp0, altit, pres0;

char EstadoSaida = '0';  //variável que armazena o estado atual da saída

const char* BROKER_MQTT = "iot.eclipse.org"; //URL do broker MQTT que se deseja utilizar
int BROKER_PORT = 1883; // Porta do Broker MQTT

WiFiClient espClient; // Cria o objeto espClient
PubSubClient MQTT(espClient); // Instancia o Cliente MQTT passando o objeto espClient
char StringLeiturasADC[TAMANHO_STRING_SERIAL];

void initWiFi(void);
void initMQTT(void);
void reconectWiFi(void); 
//void mqtt_callback(char* topic, byte* payload, unsigned int length);
//void VerificaConexoesWiFIEMQTT(void);
bool VerificaSeHaInformacaoNaSerial(void);
//void EnviaInformacoesMQTT(void);

void initWiFi() {
    delay(10);
    reconectWiFi();
}

void reconectWiFi() {
  const char *ssid     = "Katena's House";
  const char *password = "aruazI_sirC@13";
  WiFi.begin(ssid, password);

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(led, HIGH); // acende o LED
    delay(100);
    digitalWrite(led, LOW); // acende o LED
    Serial.print( "." );
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void initMQTT() {
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);   //informa qual broker e porta deve ser conectado
}
 
void reconnectMQTT() {
  if (!MQTT.connected()) 
  {
    if (MQTT.connect(ID_MQTT)) 
      Serial.println("Conectado ao MQTT");
    else
    {
      Serial.println("NÃO conectado ao MQTT");
      //aguarda 2 segundos e tenta se conectar novamente.
      delay(200);
    }
  }
  else
    Serial.println("Conectado ao MQTT");
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String msg;

  //obtem a string do payload recebido
  for (int i = 0; i < length; i++) {
     char c = (char)payload[i];
     msg += c;
  }
 
  if (msg.equals("L")) {
    digitalWrite(D0, LOW);
    EstadoSaida = '1';
  }

  //verifica se deve colocar nivel alto de tensão na saída D0:
  if (msg.equals("D")) {
    digitalWrite(D0, HIGH);
    EstadoSaida = '0';
  }
}

void VerificaConexoesWiFIEMQTT(void) {
  if (!MQTT.connected()) {
    reconnectMQTT(); //se não há conexão com o Broker, a conexão é refeita
    Serial.println("NÃO conectado ao MQTT");
  }
  else
    Serial.println("Conectado ao MQTT");
}
 
bool VerificaSeHaInformacaoNaSerial() {
  char c;
  int  i;
   
  if (Serial.available() <= 0)
    return false;
 
  //há dados sendo recebidos. Limpa buffer de recepção:
  memset(StringLeiturasADC, 0, TAMANHO_STRING_SERIAL);  
  //pega a string toda (até \0).
  
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
 
void EnviaInformacoesMQTT(void) {
  //MQTT.publish(TOPICO_PUBLISH, StringLeiturasADC);
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
    if (pos > 0)
      str1 = str1.substring(pos-3);
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
  const int httpPort = 5000;
  timeClient.update();
  
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
      
  String formattedTime    = timeClient.getFormattedTime();
  unsigned long epcohTime = timeClient.getEpochTime();
  
  data = "{\"valor\": " + String(valor) + ", \"datahora\": " + String(epcohTime) + "}";
  
  client.println("POST /api/v1.1/sensor/" + String(estacao) + "/" + tipo + " HTTP/1.1");
  client.print("Host: ");
  client.println(host);
  client.println("Accept: */*");
  client.println("Content-Type: application/json");
  client.print("Content-Length: ");
  client.println(data.length());
  client.println();
  client.print(data);
  Serial.println(data);

  delay(20); // Can be changed
  if (client.connected()) { 
    client.stop();  // DISCONNECT FROM THE SERVER
  }
  delay(20);
}

void setup() {
  Serial.begin(115200);
  
  // We start by connecting to a WiFi network
  initWiFi();
  
  initMQTT();
  
  sensor0.begin();
  //Serial.print(sensor0.getDeviceCount(), DEC);
  if (sensor0.getDeviceCount() == 0)
    Serial.println("Sensor temperatura da água não encontrado");
  
  timeClient.begin();
  
  pinMode(led,    OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(DHTPin, INPUT);

  dht.begin();
  
  digitalWrite(led, HIGH); // acende o LED
  delay(100);
  digitalWrite(led, LOW); // acende o LED
  delay(100);
  digitalWrite(led, HIGH); // acende o LED
  delay(100);
  digitalWrite(led, LOW); // acende o LED
  delay(100);
  digitalWrite(led, HIGH); // acende o LED
  delay(100);
  digitalWrite(led, LOW); // acende o LED
}

void loop() {
//    VerificaConexoesWiFIEMQTT();
  
  //se recebeu informações pela serial, as envia por MQTT
  VerificaSeHaInformacaoNaSerial();
  EnviaInformacoesMQTT();
 
  //keep=alive do MQTT
//  MQTT.loop();  
  
  sensor0.requestTemperatures();
  tempC1 = sensor0.getTempCByIndex(0);

  ldrValor = analogRead(ldrPin);
  l = 1024 - ldrValor;

  t = dht.readTemperature();
  h = dht.readHumidity();

  digitalWrite(led, HIGH); // acende o LED
  delay(10);
  digitalWrite(led, LOW); // acende o LED
  delay(10);

  Serial.print("Temperatura Amb.: ");
  EnviaDados(t, "temp_ambiente", estacao);
  Serial.print("Temperatura Água: ");
  EnviaDados(tempC1, "temp_agua", estacao);
  Serial.print("Umidade Relativa: ");
  EnviaDados(h, "umid_relativa", estacao);
  Serial.print("Luminosidade:     ");
  EnviaDados(l, "luminosidade", estacao);
  
  //ESP.reset();
}
