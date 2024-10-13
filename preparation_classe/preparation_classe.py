###############################################-
# Auteur : Julien RENOULT
# Sujet 1 : Création de classes sur les installations électriques
# Sujet 2 : Exportation simplifiée d'un fichier CSV sur la mise en service de ces installations
# Sujet 3 : Analyse exploratoire (Solaire, Thermique, Générale)
###############################################-

# Création de la classe mère : 
class Installation_Electrique :

    dict_fil_tech_comb = {
        "AUT" : ["AUTRE", [], []],

        "ENM" : ["ENERGIES MARINES", ["MAREMOTRICE",
                                      "HYDROLIENNE EN MER",
                                      "AUTRES"], []],

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
            "AUTRES"],
            
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
            "AUTRES"],
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

    def __init__(self, id_objet, nom_installation, cod_iris, commune, departement, 
                 region, filiere, epci, dateraccordement, datemiseenservice, datedebutversion, 
                 combustible, combustiblessecondaires, technologie, nbgroupes, regime, gestionnaire,
                 moderaccordement, tensionraccordement, postesource, type_prod_stock) :
        
        self.id = id_objet
        self.nom = nom_installation
        self.code_iris = cod_iris

        self.localisation = {
            "commune" : commune,
            "departement" : departement,
            "region" :region
        }

        self.technologie = {
            "filiere" : filiere,
            "technologie" : technologie,
            "combustible(s)" : (combustible, combustiblessecondaires)
        }

        self.poste_source = postesource
        self.epci = epci

        self.raccordement = {
            "mode" : moderaccordement,
            "date" : dateraccordement,
            "tension" : tensionraccordement
        }

        self.date_mis_serv = datemiseenservice
        self.date_deb_ver = datedebutversion

        self.appartenance = {
            "regime" : regime,
            "gestionnaire" : gestionnaire,
            "nb_groupes" : nbgroupes
        }

        self.prod_stock = type_prod_stock

    def localisation_centrale(self):
        '''
        Récupère la localisation de la centrale en instance.
        Argument :
        - self : l'instance en question
        '''
        return self.localisation
    
    def dates_centrales(self):
        '''
        Récupère la localisation de la centrale en instance.
        Argument :
        - self : l'instance en question
        '''
        return (self.date_deb_ver, self.date_mis_serv)
    
    # Utilisation de print sur un objet
    def __str__(self):
        return f"""L'installation {self.nom} : \n 
                   - localisation : {self.localisation["region"]} \n
                   - filière : {self.technologie["filiere"]} \n 
                   - date de mise en service : {self.date_mis_serv} \n
                   - type : {self.prod_stock}"""
    
# Création de la classe fille concernant les installations de productions d'électricité
class Production(Installation_Electrique) :

    def __init__(self, id_objet, nom_installation, cod_iris, commune, departement, region, 
                 filiere, epci, dateraccordement, datemiseenservice, datedebutversion, combustible, combustiblessecondaires, 
                 technologie, nbgroupes, regime, gestionnaire, moderaccordement, tensionraccordement, postesource,
                 puismaxrac, puismaxinstallee):
        
        super().__init__(id_objet, nom_installation, cod_iris, commune, departement, region, 
                         filiere, epci, dateraccordement, datemiseenservice, datedebutversion, 
                         combustible, combustiblessecondaires, technologie, nbgroupes, regime, 
                         gestionnaire, moderaccordement, tensionraccordement, postesource, "P")
        
        self.information_puissance = {
                "puis_max_rac" : puismaxrac,
                "puis_max_inst" : puismaxinstallee
            }

# Création de la classe fille concernant les installations de stockage électriques
class Stockage(Installation_Electrique) :

    def __init__(self, id_objet, nom_installation, cod_iris, commune, departement, region, 
                 filiere, epci, dateraccordement, datemiseenservice, datedebutversion, combustible, combustiblessecondaires, 
                 technologie, nbgroupes, regime, gestionnaire, moderaccordement, tensionraccordement, postesource,
                 puismaxraccharge, puismaxcharge, puismaxinstalleedischarge, energiestockable):
        
        super().__init__(id_objet, nom_installation, cod_iris, commune, departement, region, filiere, 
                         epci, dateraccordement, datemiseenservice, datedebutversion, combustible, combustiblessecondaires, 
                         technologie, nbgroupes, regime, gestionnaire, moderaccordement, tensionraccordement, postesource,
                         "S")
        
        self.information_puissance = {
            "puis_max_rac_charge" : puismaxraccharge,
            "puis_max_inst_dis" : puismaxinstalleedischarge,
            "puis_max_charge" : puismaxcharge,
            "energie_stockable" : energiestockable
        }

# Création de la classe fille concernant les installations de productions/stockages électriques
class Reversible(Installation_Electrique):

    def __init__(self, id_objet, nom_installation, cod_iris, commune, departement, region, 
                 filiere, epci, dateraccordement, datemiseenservice, datedebutversion, combustible, combustiblessecondaires, 
                 technologie, nbgroupes, regime, gestionnaire, moderaccordement, tensionraccordement, postesource,
                 puismaxraccharge, puismaxinstalleedischarge, puismaxcharge, energiestockable,
                 puismaxrac, puismaxinstallee):
        
        super().__init__(id_objet, nom_installation, cod_iris, commune, departement, region, filiere, 
                         epci, dateraccordement, datemiseenservice, datedebutversion, combustible, combustiblessecondaires, 
                         technologie, nbgroupes, regime, gestionnaire, moderaccordement, tensionraccordement, postesource, "R")
        
        self.information_puissance = {
            "Stockage" : {
            "puis_max_rac_charge" : puismaxraccharge,
            "puis_max_inst_dis" : puismaxinstalleedischarge,
            "puis_max_charge" : puismaxcharge,
            "energie_stockable" : energiestockable
            },
            "Production" : {
                "puis_max_rac" : puismaxrac,
                "puis_max_inst" : puismaxinstallee
            }
        }

# Création de la classe fille sur les installations électriques de type hydraulique en ajoutant des informations supplémentaires concernant les centrales hydrauliques
class Hydraulique(Production, Stockage, Reversible) :

    def __init__(self, id_objet, nom_installation, cod_iris, commune, departement, region, epci, dateraccordement, datemiseenservice, datedebutversion, 
                 combustible, combustiblessecondaires, technologie, nbgroupes, regime, gestionnaire, 
                 moderaccordement, tensionraccordement, postesource, puismaxrac, puismaxinstallee,
                 debitmaximal, capacitereservoir, productible, hauteurchute):
        
        super().__init__(id_objet, nom_installation, cod_iris, commune, departement, region, 
                         "Hydraulique", epci, dateraccordement, datemiseenservice, datedebutversion, 
                         combustible, combustiblessecondaires, technologie, nbgroupes, regime, gestionnaire, 
                         moderaccordement, tensionraccordement, postesource, puismaxrac, puismaxinstallee)

        self.information_hydraulique =  {
            "debitmaximal" : debitmaximal, 
            "capacitereservoir" : capacitereservoir, 
            "productible" : productible, 
            "hauteurchute" : hauteurchute
        }     

