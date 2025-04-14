
import sqlite3  
import pandas as pd 


print("Connexion à la base de données...")
conn = sqlite3.connect("ventes_magasin.db")

#Extraction des données de la base de données
# 1. Données complètes des ventes
print("Extraction des données de ventes...")
requete_ventes = """
SELECT 
    v.*, 
    p.nom_produit, p.prix_unitaire, p.stock, 
    c.nom_categorie, 
    cl.nom AS nom_client, cl.prenom AS prenom_client, cl.ville  
FROM Ventes v
JOIN Produits p ON v.id_produit = p.id_produit
JOIN Categories c ON p.id_categorie = c.id_categorie
JOIN Clients cl ON v.id_client = cl.id_client
"""
ventes_df = pd.read_sql_query(requete_ventes, conn)

# 2. Liste complète des produits
print("Extraction de la liste des produits...")
produits_df = pd.read_sql_query("SELECT * FROM Produits", conn)

# 3. Liste complète des clients
print("Extraction de la liste des clients...")
clients_df = pd.read_sql_query("SELECT * FROM Clients", conn)

# 4. Liste des catégories
print("Extraction des catégories...")
categories_df = pd.read_sql_query("SELECT * FROM Categories", conn)

## Étape 3 : Extraction de données complémentaires

# 1. Produits jamais vendus
print("Recherche des produits jamais vendus...")
produits_non_vendus = pd.read_sql_query("""
SELECT p.* 
FROM Produits p
LEFT JOIN Ventes v ON p.id_produit = v.id_produit
WHERE v.id_vente IS NULL
""", conn)

# 2. Ventes par mois
print("Calcul des ventes par mois...")
ventes_par_mois = pd.read_sql_query("""
SELECT 
    strftime('%Y-%m', date_vente) AS mois,
    SUM(montant_total) AS chiffre_affaires,
    COUNT(id_vente) AS nombre_ventes
FROM Ventes
GROUP BY mois
ORDER BY mois
""", conn)

# 3. VENTES PAR ANNÉE (NOUVEAU)
print("Calcul des ventes par année...")
ventes_par_annee = pd.read_sql_query("""
SELECT 
    strftime('%Y', date_vente) AS annee,
    SUM(montant_total) AS chiffre_affaires,
    COUNT(id_vente) AS nombre_ventes,
    SUM(quantite) AS total_articles_vendus
FROM Ventes
GROUP BY annee
ORDER BY annee
""", conn)

## Étape 4 : Vérification des données
print("\nVérification des données extraites...")
print("- Nombre de ventes :", len(ventes_df))
print("- Nombre de produits :", len(produits_df))
print("- Nombre de clients :", len(clients_df))
print("- Produits jamais vendus :", len(produits_non_vendus))
print("- Années analysées :", ventes_par_annee['annee'].tolist())


print("\nSauvegarde des données...")
toutes_les_donnees = {
    "ventes": ventes_df,
    "produits": produits_df,
    "clients": clients_df,
    "categories": categories_df,
    "produits_non_vendus": produits_non_vendus,
    "ventes_par_mois": ventes_par_mois,
    "ventes_par_annee": ventes_par_annee 
}




conn.close()
print("\nExtraction terminée avec succès!")
print("DataFrames disponibles :")
print("- ventes_df (toutes les ventes détaillées)")
print("- produits_df, clients_df, categories_df")
print("- produits_non_vendus")
print("- ventes_par_mois")
print("- ventes_par_annee (nouveau)")




# Analyses et calculs avec les DataFrames existants
print("Début de l'analyse statistique...")

print("\n" + "="*50)
print("ANALYSES DE BASE")
print("="*50)

# Chiffre d'affaires total
ca_total = ventes_df['montant_total'].sum()
print(f"\n1. Chiffre d'affaires total : {ca_total:,.2f} FCFA")

# Panier moyen
panier_moyen = ventes_df['montant_total'].mean()
print(f"2. Panier moyen : {panier_moyen:.2f} FCFA")

# Nombre moyen d'articles par vente
moyenne_articles = ventes_df['quantite'].mean()
print(f"3. Nombre moyen d'articles par vente : {moyenne_articles:.1f}")

#Analyse réalisée sur les produits 
print("\n" + "="*50)
print("ANALYSE PAR PRODUIT")
print("="*50)

# Top 5 produits par quantité vendue
top_produits_quantite = ventes_df.groupby('nom_produit')['quantite'].sum().nlargest(5)
print("\n4. Top 5 produits (quantité vendue):")
print(top_produits_quantite.to_string())

# Top 5 produits par chiffre d'affaires
top_produits_ca = ventes_df.groupby('nom_produit')['montant_total'].sum().nlargest(5)
print("\n5. Top 5 produits (chiffre d'affaires):")
print(top_produits_ca.to_string())

# Produits jamais vendus
print("\n6. Produits jamais vendus :", len(produits_non_vendus))

# Marge par produit (si prix_unitaire et montant_total disponibles)
ventes_df['marge'] = ventes_df['montant_total'] - (ventes_df['prix_unitaire'] * ventes_df['quantite'])
marge_par_produit = ventes_df.groupby('nom_produit')['marge'].sum().nlargest(5)
print("\n7. Top 5 produits par marge:")
print(marge_par_produit.to_string())


print("\n" + "="*50)
print("ANALYSE TEMPORELLE")
print("="*50)

# Ventes par année
print("\n8. Chiffre d'affaires par année:")
print(ventes_par_annee.to_string(index=False))

# Calcul de l'évolution annuelle
ventes_par_annee['evolution_pct'] = ventes_par_annee['chiffre_affaires'].pct_change() * 100
print("\n9. Évolution annuelle (%):")
print(ventes_par_annee[['annee', 'chiffre_affaires', 'evolution_pct']].to_string(index=False))

# Meilleur mois
meilleur_mois = ventes_par_mois.loc[ventes_par_mois['chiffre_affaires'].idxmax()]
print(f"\n10. Meilleur mois : {meilleur_mois['mois']} (CA: {meilleur_mois['chiffre_affaires']:,.2f} FCFA)")

# Analyse clients
print("\n" + "="*50)
print("ANALYSE CLIENTS")
print("="*50)

# Clients les plus actifs
top_clients_achats = ventes_df.groupby(['nom_client', 'prenom_client'])['id_vente'].count().nlargest(5)
print("\n11. Top 5 clients (nombre d'achats):")
print(top_clients_achats.to_string())

# Clients les plus dépensiers
top_clients_ca = ventes_df.groupby(['nom_client', 'prenom_client'])['montant_total'].sum().nlargest(5)
print("\n12. Top 5 clients (chiffre d'affaires):")
print(top_clients_ca.to_string())

# Analyse par catégorie 
print("\n" + "="*50)
print("ANALYSE PAR CATÉGORIE")
print("="*50)

# CA par catégorie
ca_categories = ventes_df.groupby('nom_categorie')['montant_total'].sum().sort_values(ascending=False)
print("\n13. Chiffre d'affaires par catégorie:")
print(ca_categories.to_string())

# Produits les plus vendus par catégorie
top_par_categorie = ventes_df.groupby(['nom_categorie', 'nom_produit'])['quantite'].sum().groupby('nom_categorie', group_keys=False).nlargest(3)
print("\n14. Top 3 produits par catégorie:")
print(top_par_categorie.to_string())

## 6. Statistiques descriptives -----------------------------------------------
print("\n" + "="*50)
print("STATISTIQUES DESCRIPTIVES")
print("="*50)

print("\n15. Statistiques des ventes:")
print(ventes_df['montant_total'].describe().to_string())

print("\n16. Statistiques des quantités vendues:")
print(ventes_df['quantite'].describe().to_string())

#nouvelles lignes 


# Calcul du panier moyen mensuel et annuel
ventes_par_mois['panier_moyen'] = ventes_par_mois['chiffre_affaires'] / ventes_par_mois['nombre_ventes']
ventes_par_annee['panier_moyen'] = ventes_par_annee['chiffre_affaires'] / ventes_par_annee['nombre_ventes']



# Création d'un dictionnaire avec tous les résultats
resultats_analyse = {
    'ca_total': ca_total,
    'panier_moyen': panier_moyen,
    'top_produits_quantite': top_produits_quantite,
    'top_produits_ca': top_produits_ca,
    'marge_par_produit': marge_par_produit,
    'ventes_par_annee': ventes_par_annee,
    'ventes_par_mois': ventes_par_mois,
    'top_clients_achats': top_clients_achats,
    'top_clients_ca': top_clients_ca,
    'ca_categories': ca_categories,
    'top_par_categorie': top_par_categorie
}

print("\nAnalyse terminée avec succès!")
print("Tous les résultats sont disponibles dans le dictionnaire 'resultats_analyse'.")