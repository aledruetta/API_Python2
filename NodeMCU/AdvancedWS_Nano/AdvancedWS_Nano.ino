#include <IRremote.h>                       // Biblioteca IRemote
#include <Adafruit_BMP085.h>
//#include <DallasTemperature.h>
//#include <Wire.h>

#define som_analog   A1
#define solo_analog  A6
#define chuva_analog A7

Adafruit_BMP085 bmp180;

int RECV_PIN = A0;                          // Arduino pino D11 conectado no Receptor IR
IRrecv irrecv(RECV_PIN);                    // criando a instância
decode_results results;                     // declarando os resultados

int cr_cor;
float tempC1, temp0, altit, pres0;
float valor_solo, valor_chuva, valor_som;

//Defines
#define TAMANHO_STRING_SERIAL      ((4*8) + 7 + 1)  //8 canais (de 4 bytes de informação cada, em ASCII) e 7 separadores (;) e 1 terminador de string (\0)
 
//Variáveis globais
int LeiturasADC[8]; //armazenará as leituras dos canais de ADC
 
//protótipops
void FazLeituraCanaisADC(void);
void TransmiteLeiturasADC(void);
 
/*
 * Implementações
 */
 
//Função: faz a leitura dos canais de ADC
//Parâmetros: nenhum
//Retorno: nenhum
void FazLeituraCanaisADC(void)
{
  char i;
 
  for (i = 0; i < 8; i++) {
    LeiturasADC[i] = analogRead(i);
  }
}
 
//Função: Transmite via serial, na forma textual/string, as leituras de ADC obtidas
//Parâmetros: nenhum
//Retorno: nenhum
void TransmiteLeiturasADC(void)
{
   char InfoCanaisADC[TAMANHO_STRING_SERIAL];
 
   //limpa string
   memset(InfoCanaisADC,0,TAMANHO_STRING_SERIAL);
 
   //coloca as leituras numa string
   sprintf(InfoCanaisADC,"%04d;%04d;%04d;%04d;%04d;%04d;%04d;%04d", LeiturasADC[0], 
                                                                    LeiturasADC[1], 
                                                                    LeiturasADC[2], 
                                                                    LeiturasADC[3], 
                                                                    LeiturasADC[4], 
                                                                    LeiturasADC[5],
                                                                    LeiturasADC[6],
                                                                    LeiturasADC[7]);
   //Transmite a string pela serial
   Serial.write(InfoCanaisADC, TAMANHO_STRING_SERIAL);                                                                     
}
  
void setup() 
{
  pinMode(som_analog,   INPUT);
  pinMode(solo_analog,  INPUT);
  pinMode(chuva_analog, INPUT);

  memset(LeiturasADC, 0, sizeof(LeiturasADC));
   
  //configura o baudrate da comunicação serial em 19200
  Serial.begin(115200);   
  irrecv.enableIRIn();                      // Inicializa a recepção de códigos

  bmp180.begin();
}
 
void loop() {
  Serial.print("Pressao: ");
  pres0 = bmp180.readPressure();
  if (pres0 < 100000)
    Serial.print(" ");
  Serial.print(pres0);
  Serial.println(" Pa");
  
  valor_solo = analogRead(solo_analog);
  Serial.print("Solo: ");
  if (valor_solo >= 1000)
    valor_solo = 999;
  Serial.println(valor_solo);  
  
  valor_chuva = analogRead(chuva_analog);
  Serial.print("Chuva: ");
  if (valor_chuva >= 1000)
    valor_chuva = 999;
  Serial.println(valor_chuva);  
  
  valor_som = analogRead(som_analog);
  Serial.print("Som: ");
  Serial.println(valor_som);  
  
  if (irrecv.decode(&results))              // se algum código for recebido
  {
    Serial.print("InfraRed: ");
    cr_cor = (int)results.value;
    Serial.println(cr_cor);     // imprime o Cor em inteiro
    irrecv.resume();
  }
  else
    Serial.println("");     // imprime o Cor em inteiro

  FazLeituraCanaisADC();  
  TransmiteLeiturasADC();
  delay(3000);
}
