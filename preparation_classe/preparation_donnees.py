###############################################-
# Auteur : Julien RENOULT
# SUJET : compréhension + préparation des données
# Sujet 1 : création de classes sur les installations électriques
# Sujet 2 : exportation simplifiée d'un fichier CSV sur la mise en service de ces installations
# Sujet 3 : analyse exploratoire + analyse prédictive (Solaire, Thermique, Générale)
###############################################-

# ---- Importation des librairies -----
import pandas as pd
######################################-

# ---- Lire le fichier de données -----
dataset = pd.read_csv("./Data/registre-national-installation-production-stockage-electricite-agrege-311222.csv", 
                      header=0, encoding="iso-8859-1", sep="\t", engine="python")

# Vérification du succès de l'opération
#print(dataset["codegestionnaire"].head(n=5))
######################################-

# ---- Compréhension des données ----
# Regarder le nom des colonnes
print("Les colonnes présents dans ce dataframe : ")
print(dataset.columns)

# Regarder la taille des données
print("\nLa dimension du dataframe : ")
print(dataset.size, dataset.shape)
####################################-

# ---- Sélection des colonnes d'intérêts ----
data = dataset[["nominstallation", "codeeicresourceobject", "codeiris", "commune", "epci", 
                "departement", "region", "dateraccordement", "datemiseenservice", 
                "datedebutversion", "postesource", "tensionraccordement", "moderaccordement",
                "filiere", "combustible", "combustiblessecondaires", "technologie", "typestockage", "puismaxinstallee",
                "puismaxraccharge", "puismaxcharge", "puismaxrac", "puismaxinstalleedischarge", "nbgroupes", "regime",
                "energiestockable", "capacitereservoir", "productible", "debitmaximal", "gestionnaire", "hauteurchute"]]

print("\nExtrait du dataframe après sélection des colonnes : ")
print(data.head(n=5))

# Mettre en majuscule + supprimer les accents (lien : https://stackoverflow.com/questions/37926248/how-to-remove-accents-from-values-in-columns) 
# combustible, combustiblessecondaires et technologie
# Application sur chacune des séries
data[["technologie", "combustible", "combustiblessecondaires"]] = data[["technologie", "combustible", "combustiblessecondaires"]].apply(lambda x : x.str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

print(data[["technologie", "combustible", "combustiblessecondaires"]][~(data["combustible"].isnull())])
############################################-

# ---- Ne garder que les installations individuelles ----
installations_elec = data[~(data["codeeicresourceobject"].isnull())]
print("\nExtrait des installations électriques : ")
print(installations_elec.head(n=10))
print(installations_elec.tail(n=10))
print("\nLa dimension du dataframe d'installations électriques : ")
print(installations_elec.size, installations_elec.shape)
###################################################################-

# ---- Préparation des données pour les installations électriques (1/2) ----

print("\nExtrait des installations électriques : ")
print(installations_elec.head(n=10))
print(installations_elec.tail(n=10))
print("\nLa dimension du dataframe des installations électriques : ")
print(installations_elec.size, installations_elec.shape)
print(installations_elec.columns)

# Regardons les différentes filières dans les installations électriques
print("Les différentes filières : ")
print(installations_elec.groupby(["filiere", "technologie", "combustible"]).count())

# Création de la fonction pour créer les différents dataframes correspondant à plusieurs fillières
def dataframe_filiere(dataframe, filiere, cols_drop=[]):
    
    if type(cols_drop) == list and cols_drop != []:
        nouv_dataframe = dataframe[dataframe["filiere"] == filiere].drop(cols_drop, axis=1)
    else :
        nouv_dataframe = dataframe[dataframe["filiere"] == filiere]

    # Montrer un extrait du dataframe
    print("\nExtrait des installations électriques concernant la filière '"+ filiere +"' : ")
    print(nouv_dataframe.head(n=10))
    print(nouv_dataframe.tail(n=10))
    print("\nLa dimension du dataframe des installations électriques concernant la filière '"+ filiere +"' : ")
    print(nouv_dataframe.size, nouv_dataframe.shape)

    return nouv_dataframe

# Création du dataframe concernant les hydrauliques
installations_hyd = dataframe_filiere(dataframe=installations_elec, filiere="Hydraulique")

# Création du dataframe concernant la Bioénergie
installations_bio = dataframe_filiere(dataframe=installations_elec, filiere="Bioénergies", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant l'Eolien
installations_eol = dataframe_filiere(dataframe=installations_elec, filiere="Eolien", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant le Solaire
installations_sol = dataframe_filiere(dataframe=installations_elec, filiere="Solaire", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant le Thermique non renouvelable
installations_tnr = dataframe_filiere(dataframe=installations_elec, filiere="Thermique non renouvelable", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant autres filières
installations_aut = dataframe_filiere(dataframe=installations_elec, filiere="Autre", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant le Nucléaire
installations_nuc = dataframe_filiere(dataframe=installations_elec, filiere="Nucléaire", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant le sockage non hydraulique
installations_snh = dataframe_filiere(dataframe=installations_elec, filiere="Stockage non hydraulique", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant la Géothermie
installations_geo = dataframe_filiere(dataframe=installations_elec, filiere="Géothermie", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dataframe concernant les énergies maritimes
installations_enm = dataframe_filiere(dataframe=installations_elec, filiere="Energies Marines", 
                                      cols_drop=["debitmaximal", "capacitereservoir", "productible", "hauteurchute"])

# Création du dictionnaire des dataframes + dictionnaire des techonologies
dataframe_dict = {
    "HYD" : installations_hyd,
    "SOL" : installations_sol,
    "ENM" : installations_enm,
    "GEO" : installations_geo,
    "SNH" : installations_snh,
    "NUC" : installations_nuc,
    "AUT" : installations_aut,
    "TNR" : installations_tnr,
    "BIO" : installations_bio,
    "EOL" : installations_eol
}


# Regardons les valeurs manquantes concernant les codeeicresourceobject
installations_elec_na = installations_elec[installations_elec["codeeicresourceobject"].isnull()]

# Montrer un extrait du dataframe
print("\nExtrait des installations électriques concernant ceux qui ont un identifiant nul : ")
print(installations_elec_na.head(n=10))
print(installations_elec_na.tail(n=10))
print("\nLa dimension du dataframe d'aggrégations électriques concernant ceux qui ont un identifiant nul : ")
print(installations_elec_na.size, installations_elec_na.shape)

#########################################################################-

# ---- Création des différentes fichiers CSV préparés pour la création des classes ----

# Prise en compte de la structure
print(installations_elec[installations_elec["puismaxrac"].isnull()][["nominstallation", "filiere", "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge"]])

print(installations_elec[(installations_elec["puismaxrac"].isnull()) & (installations_elec["puismaxinstallee"].isnull())][["nominstallation", "filiere", "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge"]])

def dataframe_condition_nan(dataframe, col_not_null=None, col_null=None):
    new_dataframe = dataframe

    if col_null != None and col_not_null != None:
        new_dataframe = dataframe[(dataframe[col_null].isnull()) & ~(dataframe[col_not_null].isnull())]
    elif col_null != None :
        new_dataframe = dataframe[(dataframe[col_null].isnull())]
    else:
        new_dataframe = dataframe[~(dataframe[col_not_null].isnull())]
    
    return new_dataframe

#print(dataframe_sans_nan(dataframe=dataframe_sans_nan(dataframe=installations_elec, col_null="puismaxrac"), col_not_null="puismaxinstallee"))

def dataframe_multiple_col_nan(dataframe, cols=[], type="null"):
    new_dataframe = dataframe
    if cols == []:
        return new_dataframe
    elif type == "null" :
        for col in cols:
            new_dataframe = dataframe_condition_nan(dataframe=new_dataframe, col_null=col)
    elif type == "not null":
        for col in cols:
            new_dataframe = dataframe_condition_nan(dataframe=new_dataframe, col_not_null=col)
    else:
        raise ValueError("Le type peut avoir comme valeur soit 'null' ou 'not null'")
    
    return new_dataframe

def dataframe_selection_filliere(dataframe, filiere=None, cols_show=[], cols_null=[], cols_not_null=[]):

    if filiere != None :
        new_dataframe = dataframe[(dataframe["filiere"] == filiere)]
    else:
        new_dataframe = dataframe

    if cols_null != [] and cols_not_null != [] :
        new_dataframe = dataframe_multiple_col_nan(dataframe=new_dataframe, cols=cols_null)
        new_dataframe = dataframe_multiple_col_nan(dataframe=new_dataframe, cols=cols_not_null, type="not null")
    
    elif cols_null == [] and cols_not_null != [] :
        new_dataframe = dataframe_multiple_col_nan(dataframe=new_dataframe, cols=cols_not_null, type='not null')

    else :
        new_dataframe = dataframe_multiple_col_nan(dataframe=new_dataframe, cols=cols_null)
    
    print("Le nouveau dataframe avec les colonnes demandées : ")
    print(new_dataframe[cols_show])
    print("---------------------------------------------")

    return new_dataframe

# ------ INSTALLATIONS HYDRAULIQUES ---------
# Observation de 5 installations hydraulique ne contenant aucune information sur la 'puismaxinstallee'
dataframe_selection_filliere(dataframe=installations_hyd, cols_show=["nominstallation", "filiere", 
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxinstallee"])

# Observation de 14 installations hydrauliques réversibles
dataframe_selection_filliere(dataframe=installations_hyd, cols_show=["filiere", 
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxrac"],
                                                                    cols_not_null=["puismaxcharge"])

# Donc installations hydrauliques peuvent être réversible
####################################################################################################-

# ----- INSTALLATIONS BIOÉNERGIES -----
dataframe_selection_filliere(dataframe=installations_bio, filiere="Bioénergies", cols_show=["nominstallation", "filiere", 
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxinstallee"])

dataframe_selection_filliere(dataframe=installations_bio, filiere="Bioénergies", cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxrac"])

dataframe_selection_filliere(dataframe=installations_bio, filiere="Bioénergies", cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxinstalleedischarge"])

# Donc installation de type bioénergies qui ne représente que des installations de productions seulement
#################################################################################################################-

# ----- INSTALLATIONS SOLAIRES -----
dataframe_selection_filliere(dataframe=installations_sol, cols_show=["nominstallation", "filiere", 
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxinstallee"])

dataframe_selection_filliere(dataframe=installations_sol, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxrac"])

dataframe_selection_filliere(dataframe=installations_sol, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxinstalleedischarge"])

# Les installations solaires représente la production et la réversible
#################################################################################################################-

# ----- INSTALLATIONS EOLIENS -----
dataframe_selection_filliere(dataframe=installations_eol, cols_show=["nominstallation", "filiere", 
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxinstallee"])

dataframe_selection_filliere(dataframe=installations_eol, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxrac"])

dataframe_selection_filliere(dataframe=installations_eol, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxcharge"])

# Les installations de type éoliens représente seulement la production
#################################################################################################################-

# ----- INSTALLATIONS THERMIQUES NON RENOUVELABLES -----
dataframe_selection_filliere(dataframe=installations_tnr, cols_show=["nominstallation", "filiere", 
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxinstallee"])

dataframe_selection_filliere(dataframe=installations_tnr, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_null=["puismaxrac"])

dataframe_selection_filliere(dataframe=installations_tnr, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxinstalleedischarge"])

# Les installations de type thermiques non renouvelables représente la production, stockage et réversible
#################################################################################################################-

# ----- INSTALLATIONS NUCLÉAIRES -----
dataframe_selection_filliere(dataframe=installations_nuc, cols_show=["nominstallation",
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"])

dataframe_selection_filliere(dataframe=installations_nuc, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxraccharge"])

# Les installations de type nucléaire représente la production seulement
#################################################################################################################-

# ----- INSTALLATIONS STOCKAGE NON HYDRAULIQUE -----
dataframe_selection_filliere(dataframe=installations_snh, cols_show=["nominstallation",
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"])

dataframe_selection_filliere(dataframe=installations_snh, cols_show=["nominstallation",
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxraccharge"])

# Les installations de type non hydraulique représente la production, stockage et réversible
#################################################################################################################-

# ----- INSTALLATIONS GÉOTHERMIQUE -----
dataframe_selection_filliere(dataframe=installations_geo, cols_show=["nominstallation",
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"])

# Les installations de type géothermique représente la production seulement
#################################################################################################################-

# ----- INSTALLATIONS ENERGIES MARITIMES -----
dataframe_selection_filliere(dataframe=installations_enm, cols_show=["nominstallation",
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"])

dataframe_selection_filliere(dataframe=installations_enm, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxraccharge"])

# Les installations de type d'énergies maritime représente la production, réversible
#################################################################################################################-

# ----- INSTALLATIONS AUTRES -----
dataframe_selection_filliere(dataframe=installations_aut, cols_show=["nominstallation",
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"])

dataframe_selection_filliere(dataframe=installations_aut, cols_show=[
                                                                     "puismaxraccharge", "puismaxcharge", 
                                                                     "puismaxinstallee", "puismaxinstalleedischarge",
                                                                     "energiestockable", "puismaxrac"],
                                                                    cols_not_null=["puismaxraccharge"])

# Les installations de type autre représente la production seulement
#################################################################################################################-

# ---- Dernières préparations + exportation des données sur plusieurs fichiers CSV ----
# Ayant fait une observation des données, on a pu repérer pour certaines filières, qu'il n'y a que des installations de productions ou de stockage ou les deux.
# Avec cette information en-tête, nous allons supprimer les colonnes ne contenant que des valeurs nulles car ils ne représentent aucun intérêts à les garder
# On va d'abord avant cela supprimer certaines lignes de données aberrantes comme on peut l'observer au niveau des fillières, technologies et combustibles

# Dictionnaire de vérification
dict_fil_tech_comb = {
        "AUT" : ["AUTRE", [], []],

        "ENM" : ["ENERGIES MARINES", ["MAREMOTRICE",
                                      "HYDROLIENNE EN MER",
                                      "AUTRE"], []],

        "EOL" : ["EOLIEN", ["TERRESTRE",
                            "EN MER FLOTTANT",
                            "EN MER POSE"], []],

        "GEO" : ["GEOTHERMIE", ["GEOTHERMIE"], []],

        "HYD" : ["HYDRAULIQUE", ["FIL DE L'EAU",
                                 "ECLUSE",
                                 "LAC",
                                 "POMPAGE TURBINAGE",
                                 "HYDROLIEN FLUVIAL"], []],

        "NUC" : ["NUCLEAIRE", [
            "FISSION",
            "FUSION"
        ], ["URANIUM"]],

        "SNH" : ["STOCKAGE NON HYDRAULIQUE", ["BATTERIE",
                                              "HYDROGENE",
                                              "VOLANT D'INERTIE"], []]
        ,

        "SOL" : ["SOLAIRE", [
            "PHOTOVOLTAIQUE",
            "THERMODYNAMIQUE"
        ], []],

        "TNR" : ["THERMIQUE NON RENOUVELABLE", [
            "TURBINE A COMBUSTION",
            "TURBINE A VAPEUR",
            "CYCLE COMBINE",
            "MOTEUR PISTON",
            "COGENERATION A VAPEUR",
            "COGENERATION A COMBUSTION",
            "AUTRE"],
            
            ["FIOUL",
             "CHARBON",
             "GAZ"]],

        "BIO" : ["BIOENERGIES", [
            "TURBINE A COMBUSTION",
            "TURBINE A VAPEUR",
            "CYCLE COMBINE",
            "MOTEUR PISTON",
            "COGENERATION A VAPEUR",
            "COGENERATION A COMBUSTION",
            "AUTRE"],
            ["BOIS ENERGIE",
             "DECHETS DE PAPETERIE",
             "BAGASSE",
             "AUTRES BIOCOMBUSTIBLES SOLIDES OU LIQUIDES",
             "BIOGAZ DE STATIONS D'EPURATION",
             "BIOGAZ DE METHANISATION",
             "BIOGAZ D'INSTALLATIONS DE STOCKAGE DE DECHETS NON DANGEREUX",
             "DECHETS MENAGERS ET URBAINS",
             "DECHETS INDUSTRIELS"]]
    }

# Pour chaque filière, on va vérifier les labels de technologies et de combustibles et les valider ou les supprimer si erreurs
for i in range(len(dataframe_dict)) : 
    fil = list(dataframe_dict.keys())[i]
    liste_tech_comb = dict_fil_tech_comb[fil]

    # Dans le cas d'une liste de technologie et de combustible non nulle
    if liste_tech_comb[1] != [] and liste_tech_comb[2] != [] :
        dataframe_dict[fil] = dataframe_dict[fil][(dataframe_dict[fil]["technologie"].isin(liste_tech_comb[1])) & 
                                                  (dataframe_dict[fil]["combustible"].isin(liste_tech_comb[2]))]
    elif liste_tech_comb[1] != [] :
        dataframe_dict[fil] = dataframe_dict[fil][(dataframe_dict[fil]["technologie"].isin(liste_tech_comb[1])) &
                                                  (dataframe_dict[fil]["combustible"].isnull())]
    else :
        dataframe_dict[fil] = dataframe_dict[fil][(dataframe_dict[fil]["technologie"].isnull()) &
                                                  (dataframe_dict[fil]["combustible"].isnull())]

# Vérification du succès de l'opération
for keys in dataframe_dict:
    if dict_fil_tech_comb[keys][1] == [] and dict_fil_tech_comb[keys][2] == []:
        donnees = dataframe_dict[keys].head(n=5)
    elif dict_fil_tech_comb[keys][1] != [] :
        donnees = dataframe_dict[keys].groupby("technologie").count()
    else:
        donnees = dataframe_dict[keys].groupby(["technologie", "combustible"]).count()

    print("Pour la filière "+keys+" : ")
    print(donnees)
    print("-----------------------------------------")

# Pour l'hydraulique, rien ne changent
installations_hyd.to_csv("Data/HYD_REV_INST.csv")

# Pour la géothermie, les colonnes concernant le stockage sont supprimées
installations_geo.drop(labels=["puismaxraccharge", "puismaxcharge", "puismaxinstalleedischarge", "energiestockable",
                               "filiere"], axis=1).to_csv("Data/GEO_PROD_INST.csv", index=False)

# Pour le solaire, rien ne change
installations_sol.drop(labels=["filiere"], axis=1).to_csv("Data/SOL_REV_INST.csv")

# Pour l'éolien, les colonnes concernant le stockage sont supprimées
installations_eol.drop(labels=["puismaxraccharge", "puismaxcharge", "puismaxinstalleedischarge", "energiestockable", "filiere"], axis=1).to_csv("Data/EOL_PROD_INST.csv", 
                                                                                                                                                index=False)

# Pour le thermique non renouvelable, rien ne change
installations_tnr.drop(labels=["filiere"], axis=1).to_csv("Data/TNR_REV_INST.csv", index=False)

# Pour le nucléaire, les colonnes concernant le stockage sont supprimées
installations_nuc.drop(labels=["puismaxraccharge", "puismaxcharge", "puismaxinstalleedischarge", "energiestockable", "filiere"], axis=1).to_csv("Data/NUC_PROD_INST.csv", index=False)

# Pour le stockage non hydraulique, rien ne change
installations_snh.drop(labels=["filiere"], axis=1).to_csv("Data/SNH_REV_INST.csv", index=False)

# Pour la géothermie, les colonnes concernant le stockage sont supprimées
installations_geo.drop(labels=["puismaxraccharge", "puismaxcharge", "puismaxinstalleedischarge", "energiestockable", "filiere"], axis=1).to_csv("Data/GEO_PROD_INST.csv",
                                                                                                                                                index=False)

# Pour les énergies maritimes, rien ne changent
installations_enm.drop(labels=["filiere"], axis=1).to_csv("Data/ENM_REV_INST.csv", index=False)

# Pour la bioénergie, les colonnes concernant le stockage sont supprimées
installations_bio.drop(labels=["puismaxraccharge", "puismaxcharge", "puismaxinstalleedischarge", "energiestockable", "filiere"], axis=1).to_csv("Data/BIO_PROD_INST.csv", index=False)

# Pour les autres, les colonnes concernant le stockage sont supprimées
installations_aut.drop(labels=["puismaxraccharge", "puismaxcharge", "puismaxinstalleedischarge", "energiestockable", "filiere"], axis=1).to_csv("Data/AUT_PROD_INST.csv", index=False)
######################################################################################-