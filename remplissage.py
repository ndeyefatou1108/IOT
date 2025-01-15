import sqlite3
from datetime import datetime, timedelta
import random

# Connexion à la base de données
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Génération de dates réalistes pour les factures
def generer_dates_factures(nb_factures, start_date="2024-01-01"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    return [(start + timedelta(days=30 * i)).strftime("%Y-%m-%d") for i in range(nb_factures)]

# Ajout de nouvelles mesures
def ajouter_mesures():
    print("Ajout de nouvelles mesures...")
    mesures = [
        (1, round(random.uniform(20.0, 25.0), 2)),  # Capteur 1 : Température (20-25°C)
        (2, round(random.uniform(0.5, 3.0), 2)),   # Capteur 2 : Électricité (0.5-3 kWh)
    ]
    for id_capteur, valeur in mesures:
        date_insertion = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO mesures (id_capteur, valeur, date_insertion) VALUES (?, ?, ?)", 
                       (id_capteur, valeur, date_insertion))

# Ajout de factures mensuelles réalistes
def ajouter_factures():
    print("Ajout de nouvelles factures mensuelles...")
    types_factures = ['Eau', 'Électricité', 'Gaz', 'Déchets']
    dates = generer_dates_factures(12, start_date="2024-01-01")
    for date in dates:
        for type_facture in types_factures:
            montant = round(random.uniform(40.0, 120.0), 2)
            valeur_consommée = round(random.uniform(5.0, 100.0), 2)
            cursor.execute("INSERT INTO factures (type, date, montant, valeur_consommée, id_logement) VALUES (?, ?, ?, ?, ?)", 
                           (type_facture, date, montant, valeur_consommée, 1))

# Appeler les fonctions pour remplir la base
ajouter_mesures()
ajouter_factures()

# Sauvegarde et fermeture
conn.commit()
conn.close()

print("Base de données mise à jour avec succès !")

