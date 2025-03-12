import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Charger les données
csv_path = "dataset_marketing_dataviz.csv"  # Remplacer par le chemin réel
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("Fichier introuvable. Assurez-vous de fournir le bon chemin.")
    exit()

# Afficher un aperçu des données
print("Aperçu des données avant nettoyage:")
print(df.head())

def nettoyer_donnees(df):
    # Supprimer les doublons
    df = df.drop_duplicates()
    
    # Supprimer les valeurs manquantes
    df = df.dropna(subset=['Impressions', 'Clics', 'Conversions', 'Coût'])
    
    # Remplacement des valeurs aberrantes
    seuil_conversion = df['Conversions'].quantile(0.99)
    df.loc[df['Conversions'] > seuil_conversion, 'Conversions'] = np.nan  # Remplacer les valeurs extrêmes
    
    # Correction des valeurs négatives
    df = df[(df['Clics'] >= 0) & (df['Conversions'] >= 0) & (df['Coût'] >= 0)]
    
    # Remplissage des valeurs manquantes par la médiane
    for col in ['Impressions', 'Clics', 'Conversions', 'Coût']:
        df[col].fillna(df[col].median(), inplace=True)
    
    # Conversion de la colonne Date en format datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    return df

# Nettoyage des données
df = nettoyer_donnees(df)

print("Aperçu des données après nettoyage:")
print(df.head())

# 1. Visualisation des impressions par campagne
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x='Campagne', y='Impressions', estimator=sum, ci=None)
plt.title("Total des impressions par campagne")
plt.xticks(rotation=45)
plt.show()

# 2. Évolution des clics au fil du temps
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x='Date', y='Clics', hue='Campagne')
plt.title("Évolution des clics par campagne")
plt.xticks(rotation=45)
plt.show()

# 3. Relation entre les clics et les conversions
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Clics', y='Conversions', hue='Campagne')
plt.title("Relation entre Clics et Conversions")
plt.show()

# 4. Distribution des coûts des campagnes
plt.figure(figsize=(8, 5))
sns.histplot(df['Coût'], bins=10, kde=True)
plt.title("Distribution des coûts des campagnes")
plt.show()

# 5. Heatmap des corrélations
plt.figure(figsize=(8, 5))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Corrélation entre les variables")
plt.show()
