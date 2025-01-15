-- Suppression des tables si elles existent
DROP TABLE IF EXISTS logements;
DROP TABLE IF EXISTS pieces;
DROP TABLE IF EXISTS capteurs;
DROP TABLE IF EXISTS types_capteurs;
DROP TABLE IF EXISTS mesures;
DROP TABLE IF EXISTS factures;

-- Création des tables

-- Table logements
CREATE TABLE logements (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT NOT NULL,
    telephone TEXT NOT NULL,
    ip TEXT NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table pièces
CREATE TABLE pieces (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_piece TEXT NOT NULL,
    coord_x INTEGER NOT NULL,
    coord_y INTEGER NOT NULL,
    coord_z INTEGER NOT NULL,
    id_logement INTEGER NOT NULL,
    FOREIGN KEY(id_logement) REFERENCES logements(id_logement)
);

-- Table types_capteurs
CREATE TABLE types_capteurs (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_type TEXT NOT NULL,
    unite_mesure TEXT NOT NULL,
    plage_precision TEXT
);

-- Table capteurs
CREATE TABLE capteurs (
    id_capteur INTEGER PRIMARY KEY AUTOINCREMENT,
    id_type INTEGER NOT NULL,
    id_piece INTEGER NOT NULL,
    port_comm TEXT NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_type) REFERENCES types_capteurs(id_type),
    FOREIGN KEY(id_piece) REFERENCES pieces(id_piece)
);

-- Table mesures
CREATE TABLE mesures (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    valeur REAL NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_capteur INTEGER NOT NULL,
    FOREIGN KEY(id_capteur) REFERENCES capteurs(id_capteur)
);

-- Table factures
CREATE TABLE factures (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    montant REAL NOT NULL,
    valeur_consommée REAL NOT NULL,
    id_logement INTEGER NOT NULL,
    FOREIGN KEY(id_logement) REFERENCES logements(id_logement)
);


--Q3
-- Insertion d'un logement
INSERT INTO logements (adresse, telephone, ip) 
VALUES ('10 rue Eco', '0102030405', '192.168.1.1');

-- Insertion de pièces associées au logement
INSERT INTO pieces (nom_piece, coord_x, coord_y, coord_z, id_logement) 
VALUES 
    ('Salon', 0, 0, 0, 1),
    ('Cuisine', 1, 0, 0, 1),
    ('Chambre', 0, 1, 0, 1),
    ('Salle de bain', 0, 0, 1, 1);
    
    --Q4
    
    -- Insertion de types de capteurs/actionneurs
INSERT INTO types_capteurs (nom_type, unite_mesure, plage_precision) 
VALUES 
    ('Température', '°C', '0-50'),
    ('Électricité', 'kWh', '0-1000'),
    ('Eau', 'm³', '0-500'),
    ('Gaz', 'm³', '0-300');

--Q5
-- Insertion de capteurs/actionneurs
INSERT INTO capteurs (id_type, id_piece, port_comm) 
VALUES 
    (1, 1, 'COM1'),  -- Capteur de température dans le salon
    (2, 2, 'COM2');  -- Capteur d'électricité dans la cuisine

--Q6

-- Insertion de mesures pour le capteur de température (COM1)
INSERT INTO mesures (id_capteur, valeur) 
VALUES 
    (1, 21.5),  -- Première mesure : 21.5°C
    (1, 22.0);  -- Deuxième mesure : 22.0°C

-- Insertion de mesures pour le capteur d'électricité (COM2)
INSERT INTO mesures (id_capteur, valeur) 
VALUES 
    (2, 1.2),  -- Première mesure : 1.2 kWh
    (2, 1.8);  -- Deuxième mesure : 1.8 kWh
--Q7

-- Insertion de factures pour le logement
INSERT INTO factures (type, date, montant, valeur_consommée, id_logement) 
VALUES 
    ('Eau', '2024-11-01', 42.30, 9.5, 1),       -- Facture d'eau (9.5 m³)
    ('Électricité', '2024-11-01', 85.50, 150.0, 1), -- Facture d'électricité (150 kWh)
    ('Gaz', '2024-11-10', 102.75, 100.0, 1),   -- Facture de gaz (100 m³)
    ('Déchets', '2024-11-15', 15.00, 20.0, 1); -- Gestion des déchets (poids en kg)


