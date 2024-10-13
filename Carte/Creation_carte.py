import folium as f
import pandas as pd

# Position [latitude, longitude] sur laquelle est centrée la carte
location = [47, 1]

#Niveau de zoom initial : 
#3-4 pour un continent, 5-6 pour un pays, 11-12 pour une ville
zoom = 6

#Style de la carte
tiles = 'cartodbpositron'

# Initialisation de la carte
Carte = f.Map(location = location,
                   zoom_start = zoom,
                   tiles = tiles)

# Importation des données sur les installation de la centrale nucléaire
dataset = pd.read_csv("Data/NUC_PROD_INST.csv", 
            sep=",",
            header=0)

# Vérification du succès de l'opération
print(dataset[["nominstallation", "commune"]].head(n=5))
# Commentaire :
## comme on peut voir ici, on a accès au communes des installations nucléaires
## le but va être donc de créer une carte en localisant ces différentes installations
## il faut donc récupérer la latitude et longitude des communes en questions
## en plus, chaque centrale possède une ou plusieurs tranches ce qui amène à plusieurs installations sur une même commune

# Sauvegarde de la carte en HTML
Carte.save("index.html")