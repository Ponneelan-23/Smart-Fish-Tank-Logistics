#include <WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

//======================================================
// WiFi Credentials
//======================================================

const char* ssid = "Edge Matrix Corporation";
const char* password = "edgematrix0409";

//======================================================
// MQTT Configuration
//======================================================

const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "tce/ponneelan/temp";

//======================================================
// Pin Definitions
//======================================================

#define TURBIDITY_PIN 34
#define DS18B20_PIN   13

#define TRIG_PIN      26
#define ECHO_PIN      27

//======================================================
// Tank Configuration
//======================================================

// Distance from ultrasonic sensor to tank bottom

const float TANK_HEIGHT_CM = 25.0;

//======================================================
// DS18B20 Setup
//======================================================

OneWire oneWire(DS18B20_PIN);
DallasTemperature tempSensor(&oneWire);

//======================================================
// MQTT Setup
//======================================================

WiFiClient espClient;
PubSubClient client(espClient);

//======================================================

unsigned long previousMillis = 0;
const long publishInterval = 2000;

//======================================================
// WiFi Connection
//======================================================

void connectWiFi()
{
  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

//======================================================
// MQTT Reconnect
//======================================================

void reconnectMQTT()
{
  while (!client.connected())
  {
    Serial.print("Connecting to MQTT...");

    String clientID = "FishTankESP32-";
    clientID += String(random(0xffff), HEX);

    if (client.connect(clientID.c_str()))
    {
      Serial.println("Connected");
    }
    else
    {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 2 seconds");

      delay(2000);
    }
  }
}

//======================================================
// Setup
//======================================================

void setup()
{
  Serial.begin(115200);

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  tempSensor.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  connectWiFi();

  client.setServer(mqtt_server, mqtt_port);

  Serial.println();
  Serial.println("=================================");
  Serial.println("Fish Tank Monitoring Started");
  Serial.println("=================================");
}

//======================================================
// Main Loop
//======================================================

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    connectWiFi();
  }

  if (!client.connected())
  {
    reconnectMQTT();
  }

  client.loop();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= publishInterval)
  {
    previousMillis = currentMillis;

    publishSensorData();
  }
}

//======================================================
// Read Sensors and Publish
//======================================================

void publishSensorData()
{
  //====================================================
  // Temperature
  //====================================================

  tempSensor.requestTemperatures();
  float temperature =
      tempSensor.getTempCByIndex(0);

  //====================================================
  // Turbidity
  //====================================================

  long sum = 0;

  for (int i = 0; i < 20; i++)
  {
    sum += analogRead(TURBIDITY_PIN);
    delay(10);
  }

  int rawValue = sum / 20;

  float voltage =
      rawValue * (3.3 / 4095.0);

  float turbidityNTU =
      map(rawValue, 0, 4095, 1000, 0);

  //====================================================
  // Ultrasonic Sensor
  //====================================================

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  long duration =
      pulseIn(ECHO_PIN, HIGH, 30000);

  float distanceCM =
      duration * 0.0343 / 2.0;

  float waterLevelCM =
      TANK_HEIGHT_CM - distanceCM;

  if (waterLevelCM < 0)
      waterLevelCM = 0;

  if (waterLevelCM > TANK_HEIGHT_CM)
      waterLevelCM = TANK_HEIGHT_CM;

  float waterLevelPercent =
      (waterLevelCM / TANK_HEIGHT_CM) * 100.0;

  //====================================================
  // JSON Payload
  //====================================================

  String payload = "{";

  payload += "\"temperature\":";
  payload += String(temperature, 2);

  payload += ",\"turbidity_raw\":";
  payload += String(rawValue);

  payload += ",\"turbidity_voltage\":";
  payload += String(voltage, 3);

  payload += ",\"turbidity_ntu\":";
  payload += String(turbidityNTU, 2);

  payload += ",\"water_distance_cm\":";
  payload += String(distanceCM, 1);

  payload += ",\"water_level_cm\":";
  payload += String(waterLevelCM, 1);

  payload += ",\"water_level_percent\":";
  payload += String(waterLevelPercent, 1);

  payload += "}";

  //====================================================
  // Serial Monitor
  //====================================================

  Serial.println();
  Serial.println("=================================");

  Serial.print("Temperature : ");
  Serial.print(temperature);
  Serial.println(" C");

  Serial.print("Raw ADC     : ");
  Serial.println(rawValue);

  Serial.print("Voltage     : ");
  Serial.print(voltage, 3);
  Serial.println(" V");

  Serial.print("Turbidity   : ");
  Serial.println(turbidityNTU);

  Serial.print("Distance    : ");
  Serial.print(distanceCM);
  Serial.println(" cm");

  Serial.print("Water Level : ");
  Serial.print(waterLevelCM);
  Serial.println(" cm");

  Serial.print("Level %     : ");
  Serial.print(waterLevelPercent);
  Serial.println("%");

  Serial.println();

  Serial.println("MQTT Payload:");
  Serial.println(payload);

  Serial.println("=================================");

  //====================================================
  // MQTT Publish
  //====================================================

  bool status =
      client.publish(mqtt_topic,
                     payload.c_str());

  if (status)
  {
    Serial.println("MQTT Publish Success");
  }
  else
  {
    Serial.println("MQTT Publish Failed");
  }
}
