import pandas as pd
from csv import *
import requests as rqst
import numpy as np
import requests
import zipfile
import io
import warnings
warnings.filterwarnings("ignore")

# import des dataframe grâce au fileopener
file = "donnees.txt"
df_list = dataframe_creator(file)
# ordre des df : hospitalisations, urgences, dépistages, etablissements, espérance de vie, niveaux de vie, pauvreté monétaire, vieillissement, population selon age
df_hosp = df_list[0]
df_urgences = df_list[1]
df_depistage = df_list[2]
df_etab = df_list[3]
df_espvie = df_list[4]
df_nvvie = df_list[5]
df_pauv = df_list[6]
df_vieil = df_list[7]
df_pop = df_list[8]
df_deces = df_list[9]

# Nettoyage de la base des hospitalisations

df_hosp = df_hosp.rename(columns = {'incid_hosp':'nb hospitalisations','incid_rea':'nb reanimations','incid_dc':'nb deces','incid_rad':'nb retour au domicile'})
df_hosp["dep"] = df_hosp["dep"].astype(str)
df_hosp["mois"] = df_hosp["jour"].astype(str).str[5:7]
df_hosp["annee"] = df_hosp["jour"].astype(str).str[:4]

df_temp["id"] = df_hosp["dep"] + "_" + df_hosp["annee"] + "_" + df_hosp["mois"] 
df_hosp_temp = df_hosp.groupby("id").agg({"dep":"first","mois":"first","annee":"first","nb hospitalisations":"sum","nb reanimations":"sum",
 "nb deces":"sum", "nb retour au domicile":"sum"})
df_hosp = df_hosp.groupby("dep").agg({"nb hospitalisations":"sum","nb reanimations":"sum",
 "nb deces":"sum", "nb retour au domicile":"sum"})
df_hosp.index = df_hosp["dep"]
df_hosp.drop(column = "dep", index = "978")

#on retire les territoires d'outre-mer pour garder les départements
tom_list = ['977','978','986','987','988','984','989']
df_hosp = df_hosp.drop(df_hosp[df_hosp["dep"].isin(tom_list)].index)
df_hosp_temp = df_hosp_temp.drop(df_hosp_temp[df_hosp_temp["dep"].isin(tom_list)].index)


#on remet les départements comme index de la df
df_hosp = df_hosp.set_index("dep")

"""
#on crée une dataframe remplie qui contient tous les départements, pour chaque mois et chaque année
# avec les mêmes colonnes que df_hosp, elle est remplie de 0 car on suppose qu'il n'y a pas eu d'incident lié au covid
#quand ce n'est pas renseigné

dep_list = pd.unique(df_hosp["dep"])
column_hosp = df_hosp.columns.to_list()
index_list = []

for dep in dep_list:
    for annee in range(2019,2024):
        for mois in range(1,13):
            id = f'{dep}_{annee}_{mois:02d}'
            index_list.append(id)

df_hosp_fill = pd.DataFrame(0, index=index_list, columns=column_hosp)

#on rassemble les deux dataframes pour avoir 6060 lignes

df_hosp_final = pd.concat([df_hosp, df_hosp_fill], ignore_index=False)
df_hosp_final = df_hosp_final.reset_index().drop_duplicates(subset="index", keep="first").set_index("index").sort_index()
"""



# Nettoyage de la base des urgences

df_urgences = df_urgences[['dep','date_de_passage','sursaud_cl_age_corona','nbre_pass_corona', 'nbre_pass_tot',
 "nbre_hospit_corona","nbre_acte_corona","nbre_acte_tot"]]
#on remplit les valeurs non renseignées par 0
df_urgences.fillna(0)
df_urgences["dep"] = df_urgences['dep'].astype(str)
df_urgences["mois"] = df_urgences["date_de_passage"].astype(str).str[5:7]
df_urgences["annee"] = df_urgences["date_de_passage"].astype(str).str[:4]
df_urgences = df_urgences.groupby(['dep','annee','mois','sursaud_cl_age_corona']).sum()

df_urgences["id"] = df_urgences["dep"] + "_" + df_urgences["annee"] + "_" + df_urgences["mois"] + "_" + df_urgences["sursaud_cl_age_corona"].astype(str)

df_urgences = df_urgences.groupby("id").agg({"dep":"first","mois":"first","annee":"first",
"sursaud_cl_age_corona":"first","nbre_pass_corona":"sum","nbre_pass_tot":"sum",
"nbre_hospit_corona":"sum","nbre_acte_corona":"sum","nbre_acte_tot":"sum"})

"""
#on remet les départements comme index de la df
df_urgences = df_urgences.set_index("dep")
"""


# Nettoyage de la base des dépistages

#on se débarrasse des colonnes inutiles et qu'on doit recalculer
df_depistage = df_depistage.drop(columns=['cl_age90',"Ti","Tp","Td"])
df_depistage = df_depistage.rename(columns = {'pop':'population','P':'nb patients positifs',
'T':'nb patients testes'})

#conversion des valeurs afin de pouvoir faire des calculs
df_depistage["population"] = df_depistage["population"].str.replace(',','.').astype(float)
df_depistage["nb patients positifs"] = df_depistage["nb patients positifs"].str.replace(',','.').astype(float)
df_depistage["nb patients testes"] = df_depistage["nb patients testes"].str.replace(',','.').astype(float)

df_depistage["dep"] = df_depistage['dep'].astype(str)
df_depistage["mois"] = df_depistage["jour"].astype(str).str[5:7]
df_depistage["annee"] = df_depistage["jour"].astype(str).str[:4]

#création d'une id pour pouvoir regrouper par département/mois/année
df_depistage["id"] = df_depistage["dep"] + "_" + df_depistage["annee"] + "_" + df_depistage["mois"]

df_depistage = df_depistage.groupby("id").agg({"dep":"first","mois":"first","annee":"first","population":"mean","nb patients positifs":"sum",
"nb patients testes":"sum"})

#définition de taux en pourcentage
df_depistage['taux de positivite'] = df_depistage['nb patients positifs']*100/df_depistage['nb patients testes']
df_depistage['taux de depistage'] = df_depistage['nb patients testes']*100/df_depistage['population']
df_depistage["taux d'incidence"] = df_depistage['nb patients positifs']*100/df_depistage['population']


"""
#on remet les départements comme index de la df
df_depistage = df_depistage.set_index("dep")
"""

# Nettoyage de la base des établissements

"""on fait en sorte d'avoir des noms pour chaque colonnes pour pouvoir travailler sur le dataFrame"""
names_columns = ["finess", "etalab"]+[str(x) for x in range(30)]

df_etab.columns = names_columns

"""On sélectionne les colonnes intéressantes """
df_etab = df_etab.loc[:,["11","12","17","23",]]

df_etab.rename(columns={"11" : "num_dep", "12" : "nom_dep", "17" : "type_centre", "23" : "statut_centre"}, inplace=True)

"""On souhaite sélectionner les lieux pouvant avoir un lien avec la guérison/dépistage du covid uniquement"""
word_covid = ["hospi", "pharma", "maison de santé", "Laboratoire d'Analyses"]
df_etab["etat_soin_covid"] = df_etab["type_centre"].str.contains(pat="|".join(word_covid), case=False, na=False).astype(int)

df_etab.loc[df_etab["etat_soin_covid"]==1]["type_centre"].unique()


"""Certaines cathégories d'établissement se sont glissée dans notre large sélection, on les retire donc"""
line_to_drop = (["Centre Hospitalier Spécialisé lutte Maladies Mentales", "Maison de Santé pour Maladies Mentales",
"Laboratoire pharmaceutique préparant délivrant allergènes", "Syndicat Inter Hospitalier (S.I.H.)"]
    )
df_etab.loc[df_etab["type_centre"].isin(line_to_drop),"etat_soin_covid"] = 0

df_etab = df_etab.groupby(["nom_dep", "num_dep"])["etat_soin_covid"].sum().reset_index()
df_etab.sort_values(by = "etat_soin_covid",ascending=False)

# Nettoyage de la base de l'espérance de vie

df_espvie = df_espvie.rename(
    columns= {"Unnamed: 0": "num_dep", "Unnamed: 1" : "nom_dep", "Hommes" : "esp_de_vie_homme_naissance",
    "Femmes" : "esp_de_vie_femme_naissance",
    "Hommes.1" : "esp_de_vie_homme_a_60",
    "Femmes.1": "esp_de_vie_femme_a_60",
    "Hommes.2" : "esp_de_vie_homme_a_65",
    "Femmes.2" : "esp_de_vie_femme_a_65"}
    )
for col in df_espvie.select_dtypes(["int64", "float64"]).columns :
    df_espvie[col].fillna(df_espvie[col].median(), inplace=True)
#On enlève les dernières lignes qui sont inutiles
row_to_drop = df_espvie.loc[df_espvie["num_dep"]=="FE"].index[0]
df_espvie.drop(df_espvie.index[row_to_drop ::], inplace=True)
row_to_drop = df_espvie.loc[(df_espvie["num_dep"]=="P")|(df_espvie["num_dep"]=="M")].index
df_espvie.drop(row_to_drop, inplace=True)


# Nettoyage de la base des niveaux de vie

df_nvvie = df_nvvie.rename(columns= {"Départements": "num_dep", "Unnamed: 1" : "nom_dep"})
df_nvvie.dtypes
#On remplace les colonnes de type int ou float manquantes par la médiane
for col in df_nvvie.select_dtypes(["int64", "float64"]).columns :
    df_nvvie[col].fillna(df_nvvie[col].median(), inplace=True)
#Et on supprime les données pour toute la France métropolitaine et toute la France métropolitaine hors IdF
row_to_drop = df_nvvie.loc[df_nvvie["num_dep"]==974].index[0]
df_nvvie.drop(df_nvvie.index[row_to_drop+1 ::], inplace=True)
row_to_drop = df_nvvie.loc[(df_nvvie["num_dep"]=="P")|(df_nvvie["num_dep"]=="M")].index
df_nvvie.drop(row_to_drop, inplace=True)


# Nettoyage de la base de pauvreté monétaire

df_pauv = df_pauv.rename(columns= {"Départements": "num_dep", "Unnamed: 1" : "nom_dep"})
#On remplace les valeurs manquantes par la médiane
for col in df_pauv.select_dtypes(["int64", "float64"]).columns :
    df_pauv[col].fillna(df_pauv[col].median(), inplace=True)
#Et on supprime les données pour toute la France métropolitaine et toute la France métropolitaine hors IdF
row_to_drop = df_pauv.loc[df_pauv["num_dep"]==974].index[0]
df_pauv.drop(df_pauv.index[row_to_drop+1 ::], inplace=True)
row_to_drop = df_pauv.loc[(df_pauv["num_dep"]=="P")|(df_pauv["num_dep"]=="M")].index
df_pauv.drop(row_to_drop, inplace=True)


#Nettoyage de la base de vieillissement

df_vieil = df_vieil.rename(columns={"Unnamed: 0" : "num_dep", "Unnamed: 1" : "nom_dep"})
df_vieil["En 1999"] = pd.to_numeric(df_vieil["En 1999"], errors="coerce")
#On remplace les valeurs manquantes par la médiane
for col in df_vieil.select_dtypes(["int64", "float64"]).columns :
    df_vieil[col].fillna(df_vieil[col].median(), inplace=True)
#Et on supprime les données pour toute la France métropolitaine et toute la France métropolitaine hors IdF
row_to_drop = df_vieil.loc[df_vieil["nom_dep"]=="France métropolitaine et DROM (hors Mayotte)"].index[0]
df_vieil.drop(df_vieil.index[row_to_drop ::], inplace=True)
row_to_drop = df_vieil.loc[(df_vieil["num_dep"]=="P")|(df_vieil["num_dep"]=="M")|(df_vieil["num_dep"]=="69D")|(df_vieil["num_dep"]=="69M")].index
df_vieil.drop(row_to_drop, inplace=True)
df_vieil.drop(["nom_dep", "En 1999"], axis = 1, inplace = True)

#Nettoyage de la base de la population selon l'age


df_pop = df_pop.rename(columns = {"Unnamed: 0" : "num_dep", "Unnamed: 1" : "nom_dep", "Unnamed: 9" : "pop_totale"})
#On remplace les valeurs manquantes par la médiane
for col in df_pop.select_dtypes(["int64", "float64"]).columns :
    df_pop[col].fillna(df_pop[col].median(), inplace=True)
#On observe qu'à partir de la ligne 106, ça n'a plus d'întérêt donc on supprime
df_pop.drop(df_pop.index[105::], inplace=True)
#Et on supprime les données pour toute la France métropolitaine et toute la France métropolitaine hors IdF
row_to_drop = df_pop.loc[(df_pop["num_dep"]=="P")|(df_pop["num_dep"]=="M")].index
df_pop.drop(row_to_drop, inplace=True)
df_pop.drop(columns="Unnamed: 17", inplace=True)

"""
Df_deces, mais inutile vu que données déjà dans df_hosp:

#Nettoyage de la base des décès


df_deces.drop(["JDEC", "COMDEC", "ANAIS", "MNAIS", "JNAIS", "COMDOM", "LIEUDEC2"], axis = 1)
df_deces.sort_values(by=["DEPDEC", "ADEC", "MDEC"], inplace = True)

# Convertir la colonne 'SEXE' pour rendre les valeurs plus explicites
# 1 pour homme, 2 pour femme (basé sur la convention INSEE en général)
df_deces['SEXE'] = df_deces['SEXE'].map({"M": 'homme', "F": 'femme'})
result = (
    df_deces.groupby(['DEPDEC', 'ADEC', 'MDEC', 'SEXE'])
    .size()  # Compter le nombre d'occurrences
    .unstack(fill_value=0)  # Créer des colonnes pour 'homme' et 'femme'
    .reset_index()  # Remettre les index à plat
    .rename(columns={'homme': 'mort_homme', 'femme': 'mort_femme'})  # Renommer les colonnes
)

result.index = result["DEPDEC"]
df_deces = result.drop("DEPDEC", axis = 1)
"""



"""
CODE DE LIANTSOA :
#ouverture du fichier et création df avec les colonnes qui nous intéressent
url_donnees_hosp = 'https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c'
#df_hosp = pd.read_csv(url_donnees_hosp, usecols=['dep','date_de_passage','sursaud_cl_age_corona','nbre_pass_corona','nbre_hospit_corona','nbre_acte_corona','nbre_pass_tot','nbre_acte_tot'])
df_hosp = pd.read_csv(url_donnees_hosp, sep=";")
#création de la colonne mois 
df_hosp.rename(columns = {'incid_hosp':'nb hospitalisations','incid_rea':'nb reanimations','incid_dc':'nb deces','incid_rad':'nb retour au domicile'})
df_hosp["dep"] = df_hosp["dep"].astype(str)
df_hosp["mois"] = df_hosp["jour"].astype(str).str[5:7]
df_hosp["annee"] = df_hosp["jour"].astype(str).str[:4]

#on regroupe par département par mois de l'année
df_hosp_modifie = df_hosp.groupby(['dep','annee','mois']).sum()


url_donnees_urgences_hosp = "https://www.data.gouv.fr/fr/datasets/r/eceb9fb4-3ebc-4da3-828d-f5939712600a"
df_urgences_hosp_full = pd.read_csv(url_donnees_urgences_hosp, sep=";")
df_urgences_hosp = df_urgences_hosp_full[['dep',
'date_de_passage','sursaud_cl_age_corona','nbre_pass_corona', 'nbre_pass_tot', 'nbre_pass_corona', 'nbre_pass_tot',
'nbre_pass_corona', 'nbre_pass_tot']]

#on remplit les valeurs non renseignées par 0 
df_urgences_hosp.fillna(0)

df_urgences_hosp["dep"] = df_urgences_hosp['dep'].astype(str)
df_urgences_hosp["mois"] = df_urgences_hosp["date_de_passage"].astype(str).str[5:7]
df_urgences_hosp["annee"] = df_urgences_hosp["date_de_passage"].astype(str).str[:4]

df_urgences_hosp_modifie = df_urgences_hosp.groupby(['dep','annee','mois','sursaud_cl_age_corona']).sum()


#ne fonctionne pas bien encore
url_donnees_depistage = "https://www.data.gouv.fr/fr/datasets/r/426bab53-e3f5-4c6a-9d54-dba4442b3dbc"
df_depistage = pd.read_csv(url_donnees_depistage, sep=";")
df_depistage = df_depistage.drop(columns=['cl_age90'])
df_depistage = df_depistage.rename(columns = {'pop':'population','P':'patients positifs',
'T':'nb patients testes','Ti':"Taux d'incidence",'Tp':'taux de positivite','Td':'Taux de depistage'})

df_depistage["dep"] = df_depistage['dep'].astype(str)
df_depistage["mois"] = df_depistage["jour"].astype(str).str[5:7]
df_depistage["annee"] = df_depistage["jour"].astype(str).str[:4]

df_depistage = df_depistage.groupby(['dep','annee','mois']).agg({'population':'mean',
'patients positifs':'sum','nb patients testes':'sum'})
print(df_depistage.head(10))
"""