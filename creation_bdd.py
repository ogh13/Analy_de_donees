import sqlite3
import random
from datetime import datetime, timedelta
import numpy as np

# Création et connexion à la base de données
conn = sqlite3.connect('ventes_magasin.db')
cursor = conn.cursor()

# Suppression des tables existantes (pour pouvoir relancer le script si le besoin est nécessaire)
cursor.execute("DROP TABLE IF EXISTS Ventes;")
cursor.execute("DROP TABLE IF EXISTS Produits;")
cursor.execute("DROP TABLE IF EXISTS Clients;")
cursor.execute("DROP TABLE IF EXISTS Categories;")

# Création des tables
cursor.execute("""
CREATE TABLE Categories (
    id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_categorie TEXT NOT NULL,
    description TEXT
);
""")

cursor.execute("""
CREATE TABLE Produits (
    id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_produit TEXT NOT NULL,
    id_categorie INTEGER,
    prix_unitaire REAL NOT NULL,
    stock INTEGER,
    description TEXT,
    FOREIGN KEY (id_categorie) REFERENCES Categories(id_categorie)
);
""")

cursor.execute("""
CREATE TABLE Clients (
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT,
    telephone TEXT,
    ville TEXT,
    date_inscription TEXT,
    frequence_achat TEXT
);
""")

cursor.execute("""
CREATE TABLE Ventes (
    id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produit INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    date_vente TEXT NOT NULL,
    quantite INTEGER NOT NULL,
    montant_total REAL NOT NULL,
    mode_paiement TEXT,
    FOREIGN KEY (id_produit) REFERENCES Produits(id_produit),
    FOREIGN KEY (id_client) REFERENCES Clients(id_client)
);
""")

# Insertion des catégories (plus détaillées)
categories = [
    ('Électronique', 'Appareils électroniques et gadgets'),
    ('Vêtements Homme', 'Vêtements pour hommes'),
    ('Vêtements Femme', 'Vêtements pour femmes'),
    ('Vêtements Enfant', 'Vêtements pour enfants'),
    ('Alimentation', 'Produits alimentaires et boissons'),
    ('Maison', 'Meubles et articles pour la maison'),
    ('Jardin', 'Articles de jardinage'),
    ('Loisirs', 'Livres, jeux et articles de sport'),
    ('Beauté', 'Produits de beauté et cosmétiques'),
    ('Bricolage', 'Outils et matériel de bricolage')
]
cursor.executemany("INSERT INTO Categories (nom_categorie, description) VALUES (?, ?);", categories)

# Insertion des produits (100 produits)
produits = []
marques_electronique = ['Sony', 'Samsung', 'Apple', 'LG', 'Philips', 'Dell', 'HP', 'Canon', 'Bose', 'JBL']
marques_vetements = ['Nike', 'Adidas', 'Zara', 'H&M', 'Levi\'s', 'Lacoste', 'Puma', 'Uniqlo', 'Tommy Hilfiger', 'Calvin Klein']
types_alimentaires = ['Bio', 'Sans gluten', 'Vegan', 'Local', 'Artisanal', 'Premium', 'Classique']

for i in range(1, 101):  # 100 produits
    categorie = random.randint(1, 10)
    
    if categorie == 1:  # Électronique
        nom = f"{random.choice(marques_electronique)} {random.choice(['Télévision', 'Smartphone', 'Casque audio', 'Ordinateur portable', 'Appareil photo', 'Enceinte Bluetooth', 'Tablette', 'Montre connectée'])} {i}"
        prix = round(random.uniform(5000, 1200000), 2)
    elif 2 <= categorie <= 4:  # Vêtements
        type_vetement = random.choice(['T-shirt', 'Pantalon', 'Robe', 'Veste', 'Pull', 'Chemise', 'Short', 'Jupe'])
        nom = f"{random.choice(marques_vetements)} {type_vetement} {random.choice(['Classique', 'Sport', 'Décontracté', 'Élégant', 'Été', 'Hiver'])}"
        prix = round(random.uniform(1500, 300000), 2)
    elif categorie == 5:  # Alimentation
        type_produit = random.choice(['Pâtes', 'Riz', 'Céréales', 'Biscuits', 'Chocolat', 'Café', 'Thé', 'Jus', 'Eau', 'Vin'])
        nom = f"{type_produit} {random.choice(types_alimentaires)} {i}"
        prix = round(random.uniform(150, 25000), 2)
    elif categorie == 6:  # Maison
        nom = f"{random.choice(['Canapé', 'Table', 'Chaise', 'Armoire', 'Lit', 'Lampadaire', 'Tapis', 'Rideaux'])} {random.choice(['Moderne', 'Classique', 'Scandinave', 'Industriel'])}"
        prix = round(random.uniform(3000, 150000), 2)
    elif categorie == 7:  # Jardin
        nom = f"{random.choice(['Tondeuse', 'Barbecue', 'Table jardin', 'Chaise jardin', 'Parasol', 'Piscine', 'Outillage', 'Plante'])} {i}"
        prix = round(random.uniform(2000, 800000), 2)
    elif categorie == 8:  # Loisirs
        nom = f"{random.choice(['Livre', 'Jeu vidéo', 'Ballon', 'Raquette', 'Vélo', 'Puzzle', 'Figurine', 'Instrument'])} {random.choice(['Premium', 'Standard', 'Édition limitée'])}"
        prix = round(random.uniform(1000, 50000), 2)
    elif categorie == 9:  # Beauté
        nom = f"{random.choice(['Crème', 'Parfum', 'Maquillage', 'Shampoing', 'Gel douche', 'Soin visage', 'Masque'])} {random.choice(['Luxe', 'Naturel', 'Bio', 'Sensible'])}"
        prix = round(random.uniform(500, 20000), 2)
    elif categorie == 10:  # Bricolage
        nom = f"{random.choice(['Perceuse', 'Marteau', 'Scie', 'Tournevis', 'Pince', 'Échelle', 'Peinture', 'Clou'])} {random.choice(['Professionnel', 'Débutant', 'Haute qualité'])}"
        prix = round(random.uniform(800, 40000), 2)
    
    produits.append((
        nom, 
        categorie, 
        prix, 
        random.randint(5, 500),
        f"Description du produit {nom}"
    ))

cursor.executemany(
    "INSERT INTO Produits (nom_produit, id_categorie, prix_unitaire, stock, description) VALUES (?, ?, ?, ?, ?);", 
    produits
)

# Insertion des clients (150 clients pour plus de variété)
noms = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau', 
        'Laurent', 'Simon', 'Michel', 'Lefebvre', 'Lemoine', 'Roux', 'David', 'Bertrand', 'Morel', 'Fournier']
prenoms_h = ['Jean', 'Pierre', 'Paul', 'Jacques', 'Michel', 'André', 'Nicolas', 'François', 'David', 'Thomas',
             'Alexandre', 'Julien', 'Christophe', 'Stéphane', 'Philippe', 'Patrick', 'Sébastien', 'Éric', 'Olivier', 'Guillaume']
prenoms_f = ['Marie', 'Jeanne', 'Anne', 'Sophie', 'Isabelle', 'Nathalie', 'Valérie', 'Christine', 'Françoise', 'Monique',
             'Sandrine', 'Céline', 'Élodie', 'Caroline', 'Virginie', 'Stéphanie', 'Aurélie', 'Émilie', 'Camille', 'Julie']
villes = [
    'Abidjan', 'Dakar', 'Bamako', 'Ouagadougou', 'Lomé', 'Cotonou', 'Accra', 'Conakry', 'Niamey', 'Banjul',
    'Freetown', 'Monrovia', 'Nouakchott', 'Ziguinchor', 'Koulikoro', 'Kumasi', 'Parakou', 'Kankan', 'Bouaké', 'San Pedro'
]

clients = []
for i in range(1, 151):  # 150 clients
    nom = random.choice(noms)
    if random.random() < 0.5:
        prenom = random.choice(prenoms_h)
    else:
        prenom = random.choice(prenoms_f)
    
    email = f"{prenom.lower()}.{nom.lower()}{random.randint(1,99)}@example.com"
    telephone = f"0{random.randint(1,9)}{''.join([str(random.randint(0,9)) for _ in range(8)])}"
    ville = random.choice(villes)
    
    # Date d'inscription aléatoire dans les 3 dernières années
    date_inscription = (datetime.now() - timedelta(days=random.randint(1, 1095))).strftime('%Y-%m-%d')
    
    frequence = random.choice(['Occasionnel', 'Régulier', 'Fidèle', 'VIP'])
    
    clients.append((
        nom, 
        prenom, 
        email, 
        telephone, 
        ville, 
        date_inscription, 
        frequence
    ))

cursor.executemany(
    "INSERT INTO Clients (nom, prenom, email, telephone, ville, date_inscription, frequence_achat) VALUES (?, ?, ?, ?, ?, ?, ?);", 
    clients
)

# Insertion des ventes (800 ventes pour couvrir les 100 produits)
modes_paiement = ['Carte', 'Espèces', 'Chèque', 'Tmoney', 'Flooz']
ventes = []

# On crée des ventes sur une période de 2 ans pour plus de données temporelles
start_date = datetime.now() - timedelta(days=730)
end_date = datetime.now()

for i in range(1, 801):  # 800 ventes
    # Date aléatoire dans la période
    random_date = start_date + (end_date - start_date) * random.random()
    date_vente = random_date.strftime('%Y-%m-%d')
    
    id_produit = random.randint(1, 100)
    id_client = random.randint(1, 150)
    
    # On récupère le prix du produit
    cursor.execute("SELECT prix_unitaire FROM Produits WHERE id_produit = ?;", (id_produit,))
    prix_unitaire = cursor.fetchone()[0]
    
    # On veut juste favoriser les petites quantités
    # On utilise une distribution exponentielle pour simuler la quantité achetée
    quantite = int(np.random.exponential(scale=1.5)) + 1
    if quantite > 15:  # On limite la quantité à 15
        quantite = 15
    
    # Montant total avec possibilité de petite réduction aléatoire
    reduction = random.uniform(0.9, 1.0) if random.random() < 0.3 else 1.0  # 30% de chance d'avoir une réduction
    montant = round(prix_unitaire * quantite * reduction, 2)
    
    mode = random.choice(modes_paiement)
    
    ventes.append((
        id_produit, 
        id_client, 
        date_vente, 
        quantite, 
        montant, 
        mode
    ))

cursor.executemany(
    "INSERT INTO Ventes (id_produit, id_client, date_vente, quantite, montant_total, mode_paiement) VALUES (?, ?, ?, ?, ?, ?);", 
    ventes
)


conn.commit()
conn.close()

print("Base de données créée avec succès avec:")
print("- 10 catégories")
print("- 100 produits")
print("- 150 clients")
print("- 800 ventes")