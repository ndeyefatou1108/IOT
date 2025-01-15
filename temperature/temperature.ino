#include <ESP8266WiFi.h>
#include <DHT.h>

#define DHTPIN D3
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Configuration Wi-Fi
const char* ssid = "iPhone de Ndeye Fatou";
const char* password = "123456780";

// Adresse du serveur Flask
const char* serverUrl = "http://172.20.10.3:5000/api/mesures";

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connexion au Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connexion Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnecté au Wi-Fi !");
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Erreur de lecture du capteur DHT !");
    return;
  }

  Serial.print("Température: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidité: ");
  Serial.print(humidity);
  Serial.println(" %");

  WiFiClient client;
  if (client.connect("172.20.10.3", 5000)) {
    String postData = "temperature=" + String(temperature) + "&humidity=" + String(humidity);
    client.println("POST /api/mesures HTTP/1.1");
    client.println("Host: 172.20.10.3");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Content-Length: " + String(postData.length()));
    client.println();
    client.print(postData);

    while (client.connected() || client.available()) {
      if (client.available()) {
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
    }
    client.stop();
  } else {
    Serial.println("Erreur de connexion au serveur !");
  }

  delay(15000);
}
/*
WiFiClient client;
if (client.connect("172.20.10.3", 5000)) {
    String postData = "temperature=25.9&humidity=42&id_capteur=3";

    client.println("POST /api/mesures HTTP/1.1");
    client.println("Host: 172.20.10.3");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Content-Length: " + String(postData.length()));
    client.println();
    client.print(postData);

    // Lire la réponse du serveur
    while (client.connected() || client.available()) {
        if (client.available()) {
            String line = client.readStringUntil('\n');
            Serial.println(line);
        }
    }
    client.stop();
} else {
    Serial.println("Erreur de connexion au serveur !");
}}*/
