import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from extraction_analyse import resultats_analyse

# Configuration du style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

# Création du dossier de sortie
output_dir = "visualisations"
os.makedirs(output_dir, exist_ok=True)

def save_plot(fig, filename):
    """Sauvegarde la figure dans le dossier de sortie"""
    path = os.path.join(output_dir, filename)
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"Graphique sauvegardé : {path}")

# 1. Évolution temporelle des ventes
def plot_evolution_temporelle():
    # Préparation des données
    ventes_par_mois = resultats_analyse['ventes_par_mois'].copy()
    ventes_par_mois['mois'] = pd.to_datetime(ventes_par_mois['mois'])
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(data=ventes_par_mois, x='mois', y='chiffre_affaires', 
                 marker='o', color='royalblue', linewidth=2.5, ax=ax)
    
    # Personnalisation
    ax.set_title("Évolution du chiffre d'affaires mensuel", pad=20, fontsize=16, fontweight='bold')
    ax.set_xlabel("Mois", labelpad=10)
    ax.set_ylabel("Chiffre d'affaires (FCFA)", labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Formatage de l'axe Y pour afficher les grands nombres
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # Rotation des dates pour meilleure lisibilité
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    save_plot(fig, "evolution_ca_mensuel.png")

# 2. Répartition des ventes par produit
def plot_repartition_ventes():
    top_produits = resultats_analyse['top_produits_ca'].head(10)
    autres = resultats_analyse['top_produits_ca'][10:].sum()
    
    
    data = top_produits.to_frame('montant_total').reset_index()
    data.loc[len(data)] = ['Autres produits', autres]
    
    # Création du graphique
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Camembert
    wedges, texts, autotexts = ax1.pie(
        data['montant_total'], 
        labels=data['nom_produit'], 
        autopct='%1.1f%%',
        startangle=90,
        counterclock=False,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 10}
    )
    ax1.set_title("Répartition du CA par produit (Top 10)", pad=20, fontsize=14)
    
    # Bar plot horizontal
    sns.barplot(
        data=data.sort_values('montant_total', ascending=True), 
        y='nom_produit', 
        x='montant_total',
        palette='Blues_r',
        ax=ax2
    )
    ax2.set_title("Top produits par chiffre d'affaires", pad=20, fontsize=14)
    ax2.set_xlabel("Chiffre d'affaires (FCFA)")
    ax2.set_ylabel("")
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    plt.tight_layout()
    save_plot(fig, "repartition_ventes_produits.png")

# 3. Analyse par catégorie
def plot_analyse_categories():
    data = resultats_analyse['ca_categories'].to_frame('chiffre_affaires').reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(
        data=data, 
        y='nom_categorie', 
        x='chiffre_affaires',
        palette='viridis',
        ax=ax
    )
    
    ax.set_title("Chiffre d'affaires par catégorie", pad=20, fontsize=16, fontweight='bold')
    ax.set_xlabel("Chiffre d'affaires (FCFA)", labelpad=10)
    ax.set_ylabel("Catégorie", labelpad=10)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # Ajout des valeurs sur les barres
    for p in ax.patches:
        width = p.get_width()
        ax.text(width + max(data['chiffre_affaires'])*0.02, 
                p.get_y() + p.get_height()/2, 
                '{:,.0f}'.format(width), 
                ha='left', va='center')
    
    plt.tight_layout()
    save_plot(fig, "ca_par_categorie.png")

# 4. Évolution annuelle
def plot_evolution_annuelle():
    data = resultats_analyse['ventes_par_annee'].copy()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=data, 
        x='annee', 
        y='chiffre_affaires',
        marker='o',
        markersize=10,
        linewidth=2.5,
        color='darkgreen',
        ax=ax
    )
    
    ax.set_title("Évolution annuelle du chiffre d'affaires", pad=20, fontsize=16, fontweight='bold')
    ax.set_xlabel("Année", labelpad=10)
    ax.set_ylabel("Chiffre d'affaires (FCFA)", labelpad=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # Ajout des valeurs sur les points
    for i, row in data.iterrows():
        ax.text(row['annee'], row['chiffre_affaires'] + max(data['chiffre_affaires'])*0.03, 
                '{:,.0f}'.format(row['chiffre_affaires']), 
                ha='center')
    
    plt.tight_layout()
    save_plot(fig, "evolution_annuelle_ca.png")

# 5. Top clients
def plot_top_clients():
    data = resultats_analyse['top_clients_ca'].head(10).to_frame('chiffre_affaires').reset_index()
    data['client'] = data['prenom_client'] + ' ' + data['nom_client']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=data, 
        y='client', 
        x='chiffre_affaires',
        palette='rocket_r',
        ax=ax
    )
    
    ax.set_title("Top 10 clients par chiffre d'affaires", pad=20, fontsize=16, fontweight='bold')
    ax.set_xlabel("Chiffre d'affaires (FCFA)", labelpad=10)
    ax.set_ylabel("Client", labelpad=10)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    plt.tight_layout()
    save_plot(fig, "top_clients_ca.png")

#nouvelles lignes

def plot_panier_moyen():
    """Évolution du panier moyen sur la période"""
    data = resultats_analyse['ventes_par_mois'].copy()
    data['mois'] = pd.to_datetime(data['mois'])
    
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(
        data=data,
        x='mois',
        y='panier_moyen',
        marker='o',
        color='darkorange',
        linewidth=2.5
    )
    
    ax.set_title("Évolution du panier moyen mensuel", fontsize=16, fontweight='bold')
    ax.set_xlabel("Mois", fontsize=12)
    ax.set_ylabel("Panier moyen (FCFA)", fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.0f}".format(x)))
    
    save_plot(fig, "evolution_panier_moyen.png")

def plot_quantites_annuelles():
    """Quantités totales vendues par année"""
    data = resultats_analyse['ventes_par_annee']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(
        data=data,
        x='annee',
        y='total_articles_vendus',
        palette='mako'
    )
    
    ax.set_title("Quantités totales vendues par année", fontsize=16, fontweight='bold')
    ax.set_xlabel("Année", fontsize=12)
    ax.set_ylabel("Nombre d'articles vendus", fontsize=12)
    
    # Ajout des étiquettes de valeur
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height()):,}", 
                    (p.get_x() + p.get_width()/2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points')
    
    save_plot(fig, "quantites_annuelles.png")

def plot_top_produits_quantite():
    """Graphique des produits les plus vendus par quantité"""
    data = resultats_analyse['top_produits_quantite'].head(10)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(
        x=data.values,
        y=data.index,
        palette='viridis',
        ax=ax
    )
    
    ax.set_title("Top 10 des produits les plus vendus (quantité)", fontsize=16, fontweight='bold')
    ax.set_xlabel("Quantité totale vendue", fontsize=12)
    ax.set_ylabel("Produit", fontsize=12)
    
    # Ajout des étiquettes de valeur
    for i, v in enumerate(data.values):
        ax.text(v + 5, i, str(v), color='black', va='center')
    
    save_plot(fig, "top_produits_quantite.png")



# Exécution de toutes les visualisations
if __name__ == "__main__":
    print("Début de la création des visualisations...")
    plot_evolution_temporelle()
    plot_repartition_ventes()
    plot_analyse_categories()
    plot_evolution_annuelle()
    plot_top_clients()

    plot_panier_moyen()
    plot_quantites_annuelles()
    plot_top_produits_quantite()
    
    print("Création des visualisations terminée.")
    print("\nToutes les visualisations ont été créées avec succès!")