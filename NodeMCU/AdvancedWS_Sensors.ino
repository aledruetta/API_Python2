#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <DHT.h>
//#include <OneWire.h>
//#include <DallasTemperature.h>

#define DHTTYPE DHT11 // DHT11
//#define DHTPin 4 // GPIo4 ou porta D2 do NodeMCU
uint8_t DHTPin = D2;
DHT dht(DHTPin, DHTTYPE);
 
//#define ONE_WIRE_BUS 16 //GPI016 ou porta D0 do NodeMCU
//OneWire oneWire(ONE_WIRE_BUS);
//DallasTemperature sensors(&oneWire);
#define NTP_OFFSET   60 * 60      // In seconds
#define NTP_INTERVAL 60 * 1000    // In miliseconds
#define NTP_ADDRESS  "europe.pool.ntp.org"
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, NTP_ADDRESS, NTP_OFFSET, NTP_INTERVAL);

const char *ssid     = "Katena's House";
const char *password = "aruazI_sirC@13";
const char *host     = "192.168.0.109";
const int   led      = D7;

int    estacao  = 1;
int    ldrPin   = A0;
int    tmp      = 80;
int    ldrValor = 0;
String data     = "";
float  t, h;

void setup() {
  timeClient.begin();
  
  pinMode(led,    OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(DHTPin, INPUT);
  
  Serial.begin(115200);
  delay(100);

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(led, HIGH); // acende o LED
    delay(200);
    digitalWrite(led, LOW); // acende o LED
    delay(200);
    Serial.print( "." );
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  dht.begin();
}

void loop() {
  ldrValor = 1024 - analogRead(ldrPin);
  Serial.print("Leitura: ");
  Serial.println(ldrValor);
  
  t = dht.readTemperature();
  h = dht.readHumidity();
//  sensors.requestTemperatures();
  
  timeClient.update();
    
  envia_dados(t, "temperatura", estacao);
  envia_dados(h, "umidade", estacao);
}

void envia_dados(float valor, String tipo, int estacao) {
  WiFiClient client;
  const int httpPort = 5000;
  
  String formattedTime    = timeClient.getFormattedTime();
  unsigned long epcohTime = timeClient.getEpochTime();
  
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  else
    Serial.println("connected");

  Serial.print("formattedTime: ");
  Serial.println(formattedTime);
  Serial.print("epcohTime: ");
  Serial.println(epcohTime);
  
  data = "{\"valor\": " + String(valor) + ", \"datahora\": " + String(epcohTime) + "}";
  Serial.println("Requesting POST: ");
  // Send request to the server:
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

  delay(250); // Can be changed
  if (client.connected()) { 
    client.stop();  // DISCONNECT FROM THE SERVER
  }
  Serial.println("closing connection");
  delay(250);
}
