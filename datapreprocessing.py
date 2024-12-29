import pandas as pd
from csv import *
import requests as rqst
import numpy as np
import requests
import zipfile
import io
import warnings
warnings.filterwarnings("ignore")
from fileopener import dataframe_creator

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


# Nettoyage de la base des hospitalisations

df_hosp = df_hosp.rename(columns = {'incid_hosp':'nb hospitalisations','incid_rea':'nb reanimations','incid_dc':'nb deces','incid_rad':'nb retour au domicile'})
df_hosp["dep"] = df_hosp["dep"].astype(str)
df_hosp["mois"] = df_hosp["jour"].astype(str).str[5:7]
df_hosp["annee"] = df_hosp["jour"].astype(str).str[:4]

df_hosp = df_hosp.groupby("dep").agg({"nb hospitalisations":"sum","nb reanimations":"sum",
 "nb deces":"sum", "nb retour au domicile":"sum"})
df_hosp.drop(["971", "972", "973", "974", "976", "978"], inplace=True)


# Nettoyage de la base des urgences

df_urgences = df_urgences[['dep','date_de_passage','sursaud_cl_age_corona','nbre_pass_corona', 'nbre_pass_tot',
 "nbre_hospit_corona","nbre_acte_corona","nbre_acte_tot"]]
#on remplit les valeurs non renseignées par 0
df_urgences.fillna(0)
df_urgences["dep"] = df_urgences['dep'].astype(str)
df_urgences["mois"] = df_urgences["date_de_passage"].astype(str).str[5:7]
df_urgences["annee"] = df_urgences["date_de_passage"].astype(str).str[:4]
df_urgences = df_urgences.groupby(['dep']).sum()

df_urgences = df_urgences.groupby("dep").agg({"nbre_pass_corona":"sum","nbre_pass_tot":"sum",
"nbre_hospit_corona":"sum","nbre_acte_corona":"sum","nbre_acte_tot":"sum"})
df_urgences.drop(["971", "972", "973", "974", "976"], inplace = True)


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

#on somme toutes les valeurs
df_depistage = df_depistage.groupby("dep").agg({"population":"mean","nb patients positifs":"sum",
"nb patients testes":"sum"})

df_depistage['taux de positivite'] = df_depistage['nb patients positifs']*100/df_depistage['nb patients testes']
df_depistage['taux de depistage'] = df_depistage['nb patients testes']*100/df_depistage['population']
df_depistage["taux d'incidence"] = df_depistage['nb patients positifs']*100/df_depistage['population']

df_depistage.drop(["971", "972", "973", "974", "975", "976", "977", "978"], inplace = True)


# Nettoyage de la base des établissements

# On fait en sorte d'avoir des noms pour chaque colonnes pour pouvoir travailler sur le dataFrame
names_columns = ["finess", "etalab"]+[str(x) for x in range(30)]
df_etab.columns = names_columns

#On sélectionne les colonnes intéressantes 
df_etab = df_etab.loc[:,["11","12","17","23",]]
df_etab.rename(columns={"11" : "num_dep", "12" : "nom_dep", "17" : "type_centre", "23" : "statut_centre"}, inplace=True)

#On souhaite sélectionner les lieux pouvant avoir un lien avec la guérison/dépistage du covid uniquement
word_covid = ["hospi", "pharma", "maison de santé", "Laboratoire d'Analyses"]
df_etab["etat_soin_covid"] = df_etab["type_centre"].str.contains(pat="|".join(word_covid), case=False, na=False).astype(int)
df_etab.loc[df_etab["etat_soin_covid"]==1]["type_centre"].unique()


#Certaines cathégories d'établissement avec un lien faible avec le Covid se sont glissée dans notre large sélection, on les retire donc
line_to_drop = (["Centre Hospitalier Spécialisé lutte Maladies Mentales", "Maison de Santé pour Maladies Mentales",
"Laboratoire pharmaceutique préparant délivrant allergènes", "Syndicat Inter Hospitalier (S.I.H.)"]
    )
df_etab.loc[df_etab["type_centre"].isin(line_to_drop),"etat_soin_covid"] = 0

df_etab = df_etab.groupby(["nom_dep", "num_dep"])["etat_soin_covid"].sum().reset_index()
df_etab.sort_values(by = "etat_soin_covid",ascending=False)

df_etab.sort_values(by = "num_dep")
df_etab.index = df_etab["num_dep"]
df_etab.drop(["9A", "9B", "9C", "9D", "9E", "9F", "9J"], inplace = True)


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

#On enlève les lignes correspondants à l'Outre-Mer et au total sur la France métropolitaine
row_to_drop = df_espvie.loc[df_espvie["num_dep"]=="FE"].index[0]
df_espvie.drop(df_espvie.index[row_to_drop ::], inplace=True)
row_to_drop = df_espvie.loc[(df_espvie["num_dep"]=="P")|(df_espvie["num_dep"]=="M")|(df_espvie["num_dep"]==971)|(df_espvie["num_dep"]==972)|(df_espvie["num_dep"]==973)|(df_espvie["num_dep"]==974)|(df_espvie["num_dep"]==976)].index
df_espvie.drop(row_to_drop, inplace=True)
df_espvie.index = df_espvie["num_dep"].astype("str")


# Nettoyage de la base des niveaux de vie

df_nvvie = df_nvvie.rename(columns= {"Départements": "num_dep", "Unnamed: 1" : "nom_dep"})
#On remplace les colonnes de type int ou float manquantes par la médiane
for col in df_nvvie.select_dtypes(["int64", "float64"]).columns :
    df_nvvie[col].fillna(df_nvvie[col].median(), inplace=True)
#Et on supprime les données pour toute la France métropolitaine et toute la France métropolitaine hors IdF
row_to_drop = df_nvvie.loc[df_nvvie["num_dep"]==974].index[0]
df_nvvie.drop(df_nvvie.index[row_to_drop+1 ::], inplace=True)
row_to_drop = df_nvvie.loc[(df_nvvie["num_dep"]=="P")|(df_nvvie["num_dep"]=="M")|(df_nvvie["num_dep"]==972)|(df_nvvie["num_dep"]==974)].index
df_nvvie.drop(row_to_drop, inplace=True)
df_nvvie.index = df_nvvie["num_dep"].astype("str")


# Nettoyage de la base de pauvreté monétaire

df_pauv = df_pauv.rename(columns= {"Départements": "num_dep", "Unnamed: 1" : "nom_dep"})

#On remplace les valeurs manquantes par la médiane
for col in df_pauv.select_dtypes(["int64", "float64"]).columns :
    df_pauv[col].fillna(df_pauv[col].median(), inplace=True)

#Et on supprime les totaux pour toute la France métropolitaine, toute la France métropolitaine hors IdF et l'Outre-Mer
row_to_drop = df_pauv.loc[df_pauv["num_dep"]==974].index[0]
df_pauv.drop(df_pauv.index[row_to_drop+1 ::], inplace=True)
row_to_drop = df_pauv.loc[(df_pauv["num_dep"]=="P")|(df_pauv["num_dep"]=="M")|(df_pauv["num_dep"]==972)|(df_pauv["num_dep"]==974)].index
df_pauv.drop(row_to_drop, inplace=True)
df_pauv.index = df_pauv["num_dep"].astype("str")


#Nettoyage de la base de vieillissement

df_vieil = df_vieil.rename(columns={"Unnamed: 0" : "num_dep", "Unnamed: 1" : "nom_dep"})
df_vieil["En 1999"] = pd.to_numeric(df_vieil["En 1999"], errors="coerce")

#On remplace les valeurs manquantes par la médiane
for col in df_vieil.select_dtypes(["int64", "float64"]).columns :
    df_vieil[col].fillna(df_vieil[col].median(), inplace=True)

#Et on supprime les totaux pour toute la France métropolitaine, toute la France métropolitaine hors IdF et l'Outre-Mer
row_to_drop = df_vieil.loc[df_vieil["nom_dep"]=="France métropolitaine et DROM (hors Mayotte)"].index[0]
df_vieil.drop(df_vieil.index[row_to_drop ::], inplace=True)
row_to_drop = df_vieil.loc[(df_vieil["num_dep"]=="P")|(df_vieil["num_dep"]=="M")|(df_vieil["num_dep"]=="69D")|(df_vieil["num_dep"]=="69M")|(df_vieil["num_dep"]==970)|(df_vieil["num_dep"]==971)|(df_vieil["num_dep"]==972)|(df_vieil["num_dep"]==973)|(df_vieil["num_dep"]==974)|(df_vieil["num_dep"]==976)].index
df_vieil.drop(row_to_drop, inplace=True)
df_vieil.drop(["nom_dep", "En 1999"], axis = 1, inplace = True)
df_vieil.index = df_vieil["num_dep"].astype("str")


#Nettoyage de la base de la population selon l'age

df_pop = df_pop.rename(columns = {"Unnamed: 0" : "num_dep", "Unnamed: 1" : "nom_dep", "Unnamed: 9" : "pop_totale"})

#On remplace les valeurs manquantes par la médiane
for col in df_pop.select_dtypes(["int64", "float64"]).columns :
    df_pop[col].fillna(df_pop[col].median(), inplace=True)

#On observe qu'à partir de la ligne 106, ça n'a plus d'întérêt donc on supprime
df_pop.drop(df_pop.index[105::], inplace=True)
#Et on supprime les données pour toute la France métropolitaine et toute la France métropolitaine hors IdF
row_to_drop = df_pop.loc[(df_pop["num_dep"]=="P")|(df_pop["num_dep"]=="M")|(df_pop["num_dep"]=="69D")|(df_pop["num_dep"]=="69M")|(df_pop["num_dep"]==971)|(df_pop["num_dep"]==972)|(df_pop["num_dep"]==973)|(df_pop["num_dep"]==974)|(df_pop["num_dep"]==976)].index
df_pop.drop(row_to_drop, inplace=True)
df_pop.drop(columns="Unnamed: 17", inplace=True)
df_pop.index = df_pop["num_dep"]
df_pop.drop(columns = "num_dep",inplace=True)


df_final = df_pop
df_final["nb hospitalisations"] = df_hosp["nb hospitalisations"]
df_final["nb deces"] = df_hosp["nb deces"]
df_final["espérance de vie"] = df_vieil["En 2021"]
df_final["passage_urg_corona"] = df_urgences["nbre_pass_corona"]
df_final["nb_etab_sante"] = df_etab["etat_soin_covid"]
df_final["esp_de_vie_H_60"] = df_espvie["esp_de_vie_homme_a_60"]
df_final["esp_de_vie_F_60"] = df_espvie["esp_de_vie_femme_a_60"]
df_final["esp_de_vie_H_65"] = df_espvie["esp_de_vie_homme_a_65"]
df_final["esp_de_vie_F_65"] = df_espvie["esp_de_vie_femme_a_65"]
df_final["rapport nv_vie interdécile D9/D1"] = df_nvvie["Rapport interdécile D9/D1"]
df_final["indicateur pauvreté 1"] = df_pauv["Intensité de la pauvreté (1)"]
df_final["indicateur pauvreté 2"] = df_pauv["Intensité de la pauvreté des bénéficiaires de minima sociaux (1) (2)"]
df_final["patients positifs"] = df_depistage["nb patients positifs"]
df_final["patients testés"] = df_depistage["nb patients testes"]
df_final["ratio patients positifs/population"] = df_final["patients positifs"]*100/df_final["pop_totale"]
df_final["ratio patients positifs/testés"] = df_final["patients positifs"]*100/df_final["patients testés"]
df_final["ratio patients testés/population"] = df_final["patients testés"]*100/df_final["pop_totale"]
df_final["ratio population/etab"] = df_final["pop_totale"]/df_final["nb_etab_sante"]
