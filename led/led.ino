#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "NomDuWiFi";       // Nom de ton réseau WiFi
const char* password = "MotDePasse"; // Mot de passe WiFi
const char* server = "http://192.168.1.100:5000/controle_led";  // Adresse Flask

const int ledPin = 2;  // GPIO pour la LED (par exemple GPIO 2 sur l'ESP8266)

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  pinMode(ledPin, OUTPUT);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion WiFi...");
  }
  Serial.println("Connecté au WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(server);
    http.addHeader("Content-Type", "application/json");

    // Exemple : Température extérieure
    String payload = "{\"temperature_exterieure\": 28.5}";
    int httpCode = http.POST(payload);

    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);

      // Décider d'allumer ou d'éteindre la LED
      if (response.indexOf("allumer") != -1) {
        digitalWrite(ledPin, HIGH);  // Allume la LED
      } else {
        digitalWrite(ledPin, LOW);   // Éteint la LED
      }
    } else {
      Serial.println("Erreur de connexion au serveur");
    }

    http.end();
  }
  delay(60000);  // Envoie la requête toutes les 60 secondes
}
