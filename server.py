from flask import Flask, render_template, jsonify, request, make_response
import sqlite3  # Pour gérer la connexion avec la base de données SQLite
from fpdf import FPDF  # Pour créer et générer des fichiers PDF
import requests  # Pour envoyer des requêtes HTTP, notamment vers des API externes

# Initialisation de l'application Flask
app = Flask(__name__)

# Fonction pour établir une connexion avec la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Connexion à la base de données 'database.db'
    conn.row_factory = sqlite3.Row  # Format des résultats en dictionnaires (clé-valeur)
    return conn  # Retourne l'objet de connexion

# Configuration des variables pour l'API météo (OpenWeather)
API_KEY = '3c33ba4580c24d8177c9a88b32479bfb'  # Clé d'accès à l'API OpenWeather
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'  # URL pour obtenir les prévisions météo

# Routes pour les différentes pages de l'application

# Page d'accueil
@app.route('/')
def accueil():
    return render_template('index.html')  # Charge et affiche le fichier HTML 'index.html'

# Page de consommation
@app.route('/consommation')
def consommation():
    conn = get_db_connection()  # Connexion à la base de données
    # Requête SQL pour récupérer le total des montants par type de facture
    factures = conn.execute(
        'SELECT type, SUM(montant) AS total FROM factures GROUP BY type'
    ).fetchall()
    conn.close()  # Ferme la connexion à la base
    return render_template('consommation.html', factures=factures)  # Envoie les données au template

# Page des capteurs
@app.route('/capteurs')
def capteurs():
    conn = get_db_connection()  # Connexion à la base de données
    # Requête SQL pour récupérer tous les capteurs
    capteurs = conn.execute('SELECT * FROM capteurs').fetchall()
    conn.close()  # Fermeture de la connexion
    return render_template('capteurs.html', capteurs=capteurs)  # Affiche les données dans 'capteurs.html'

# Page des économies
@app.route('/economies')
def economies():
    conn = get_db_connection()  # Connexion à la base de données
    # Requête SQL pour récupérer toutes les factures
    factures = conn.execute('SELECT * FROM factures').fetchall()
    conn.close()  # Fermeture de la connexion
    return render_template('economies.html', factures=factures)  # Envoie les données au template

# Page de configuration
@app.route('/configuration')
def configuration():
    conn = get_db_connection()  # Connexion à la base
    # Requête SQL pour récupérer les informations des capteurs
    capteurs = conn.execute('SELECT * FROM capteurs').fetchall()
    conn.close()  # Fermeture de la connexion
    return render_template('configuration.html', capteurs=capteurs)

# Téléchargement d'un relevé mensuel au format PDF
@app.route('/telecharger_mensuel', methods=['GET'])
def telecharger_mensuel_pdf():
    mois = request.args.get('mois', '2024-11')  # Récupération du mois à partir des paramètres GET
    conn = get_db_connection()  # Connexion à la base
    # Requête SQL pour récupérer les factures du mois spécifié
    factures = conn.execute(
        "SELECT * FROM factures WHERE strftime('%Y-%m', date) = ?", (mois,)
    ).fetchall()
    conn.close()  # Fermeture de la connexion

    pdf = FPDF()  # Initialisation de l'objet PDF
    pdf.add_page()  # Ajout d'une page

    # Ajout des polices personnalisées
    pdf.add_font('FreeSerif', '', './static/fonts/FreeSerif.ttf', uni=True)
    pdf.add_font('FreeSerif', 'B', './static/fonts/FreeSerifBold.ttf', uni=True)

    # Titre du document PDF
    pdf.set_font('FreeSerif', 'B', 16)
    pdf.cell(200, 10, txt=f"Relevé Mensuel - {mois}", ln=True, align='C')
    pdf.ln(10)

    # Informations générales
    pdf.set_font('FreeSerif', '', 12)
    pdf.cell(200, 10, txt="Nom: Votre Nom", ln=True)
    pdf.cell(200, 10, txt="Adresse: Votre Adresse", ln=True)
    pdf.ln(10)

    # En-têtes du tableau
    pdf.set_font('FreeSerif', 'B', 12)
    pdf.cell(50, 10, "Type", 1)
    pdf.cell(50, 10, "Date", 1)
    pdf.cell(50, 10, "Montant (€)", 1)
    pdf.cell(50, 10, "Valeur Consommée", 1)
    pdf.ln()

    # Contenu des factures
    pdf.set_font('FreeSerif', '', 12)
    for facture in factures:
        pdf.cell(50, 10, facture['type'], 1)
        pdf.cell(50, 10, facture['date'], 1)
        pdf.cell(50, 10, f"{facture['montant']:.2f} €", 1)
        pdf.cell(50, 10, f"{facture['valeur_consommée']:.2f}", 1)
        pdf.ln()

    # Génération du PDF
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=releve_mensuel.pdf'
    return response

# Téléchargement des mesures au format PDF
@app.route('/telecharger_mesures', methods=['GET'])
def telecharger_mesures_pdf():
    conn = get_db_connection()  # Connexion à la base
    # Requête SQL pour récupérer toutes les mesures
    mesures = conn.execute(
        '''
        SELECT m.id_mesure, m.valeur, m.date_insertion, c.id_capteur, c.id_type
        FROM mesures m
        JOIN capteurs c ON m.id_capteur = c.id_capteur
        ORDER BY m.date_insertion
        '''
    ).fetchall()
    conn.close()  # Fermeture de la connexion

    pdf = FPDF()  # Initialisation du PDF
    pdf.add_page()  # Ajout d'une page
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(200, 10, txt="Relevé des Mesures des Capteurs", ln=True, align='C')
    pdf.ln(10)

    # En-têtes du tableau
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(50, 10, "ID Mesure", 1)
    pdf.cell(50, 10, "Capteur", 1)
    pdf.cell(50, 10, "Valeur", 1)
    pdf.cell(50, 10, "Date", 1)
    pdf.ln()

    # Contenu des mesures
    pdf.set_font('Helvetica', '', 12)
    for mesure in mesures:
        pdf.cell(50, 10, str(mesure['id_mesure']), 1)
        pdf.cell(50, 10, str(mesure['id_capteur']), 1)
        pdf.cell(50, 10, f"{mesure['valeur']:.2f}", 1)
        pdf.cell(50, 10, mesure['date_insertion'], 1)
        pdf.ln()

    # Génération du PDF
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=releve_mesures.pdf'
    return response

# API pour récupérer les mesures des capteurs existants
@app.route('/api/mesures', methods=['GET'])
def get_mesures_existants():
    conn = get_db_connection()  # Connexion à la base
    mesures = conn.execute(
        '''
        SELECT id_mesure, valeur, id_capteur, date_insertion
        FROM mesures
        WHERE id_capteur != 3
        ORDER BY date_insertion DESC
        '''
    ).fetchall()
    conn.close()
    return jsonify([dict(mesure) for mesure in mesures])  # Retourne les données en format JSON

# API pour récupérer les mesures du capteur ESP
@app.route('/api/mesures_esp', methods=['GET'])
def get_mesures():
    conn = get_db_connection()  # Connexion à la base
    mesures = conn.execute(
        '''
        SELECT id_mesure, valeur AS temperature, humidity, date_insertion, id_capteur
        FROM mesures
        ORDER BY date_insertion DESC
        '''
    ).fetchall()
    conn.close()

    # Construction des résultats sous forme de liste de dictionnaires
    results = []
    for mesure in mesures:
        results.append({
            'id_mesure': mesure['id_mesure'],
            'id_capteur': mesure['id_capteur'],
            'temperature': mesure['temperature'],
            'humidity': mesure['humidity'] if mesure['humidity'] is not None else 'N/A',
            'date_insertion': mesure['date_insertion']
        })
    return jsonify(results)  # Retourne les données en JSON

# Route pour afficher les pièces
@app.route('/pieces')
def afficher_pieces():
    conn = get_db_connection()  # Connexion à la base
    pieces = conn.execute('SELECT * FROM pieces').fetchall()  # Requête SQL pour récupérer toutes les pièces
    conn.close()
    return render_template('pieces.html', pieces=pieces)  # Affiche les données dans 'pieces.html'

# Route pour afficher les détails d'une pièce spécifique
@app.route('/pieces/<int:piece_id>')
def afficher_details_piece(piece_id):
    conn = get_db_connection()  # Connexion à la base
    # Requête SQL pour récupérer les détails d'une pièce donnée
    piece = conn.execute('SELECT * FROM pieces WHERE id_piece = ?', (piece_id,)).fetchone()
    # Requête SQL pour récupérer les capteurs associés à la pièce
    capteurs = conn.execute(
        '''
        SELECT c.id_capteur, t.nom_type, c.port_comm, m.valeur, m.date_insertion 
        FROM capteurs c
        JOIN types_capteurs t ON c.id_type = t.id_type
        LEFT JOIN mesures m ON m.id_capteur = c.id_capteur
        WHERE c.id_piece = ?
        ORDER BY m.date_insertion DESC
        ''', 
        (piece_id,)
    ).fetchall()
    conn.close()
    return render_template('details_piece.html', piece=piece, capteurs=capteurs)  # Affiche les détails dans 'details_piece.html'

# Route pour afficher les prévisions météo
@app.route('/meteo_page', methods=['GET'])
def meteo_page():
    ville = request.args.get('ville', 'Paris')  # Récupère la ville depuis la requête GET (par défaut : Paris)
    url = f"{BASE_URL}?q={ville}&units=metric&appid={API_KEY}"  # Construit l'URL pour l'API météo
    
    try:
        response = requests.get(url)  # Envoie une requête GET à l'API
        data = response.json()  # Récupère les données en format JSON
        
        # Vérifie si la requête a échoué ou si les données manquent
        if response.status_code != 200 or 'list' not in data:
            return render_template('meteo.html', ville=ville, previsions=None, error="Erreur : Impossible de récupérer les données météo.")

        # Formate les prévisions pour les 5 prochains jours
        previsions = [
            {
                'date': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description']
            }
            for item in data['list'][:5]
        ]
        return render_template('meteo.html', ville=ville, previsions=previsions, error=None)
    
    except Exception as e:
        # En cas d'erreur, affiche une page avec un message d'erreur
        return render_template('meteo.html', ville=ville, previsions=None, error=f"Erreur : {str(e)}")

# Lancement du serveur Flask en mode debug
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

