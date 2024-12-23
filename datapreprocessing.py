import pandas as pd
from fileopener import dataframe_creator, dataframe_etablissement

# import des dataframe grâce au fileopener
file = "donnees.txt"
df_list = dataframe_creator(file)
print(df_list)
# ordre des df : hospitalisations, urgences, dépistages, etablissements, espérance de vie, taux de mortalité, niveaux de vie, pauvreté monétaire, vieillissement, population selon age
df_hosp = df_list[0]
df_urgences = df_list[1]
df_depistage = df_list[2]
df_etab = df_list[3]
df_espvie = df_list[4]
df_txmort = df_list[5]
df_nvvie = df_list[6]
df_pauv = df_list[7]
df_vieil = df_list[8]
df_pop = df_list[9]

# Nettoyage de la base des hospitalisations

df_hosp.rename(columns = {'incid_hosp':'nb hospitalisations','incid_rea':'nb reanimations','incid_dc':'nb deces','incid_rad':'nb retour au domicile'})
df_hosp["dep"] = df_hosp["dep"].astype(str)
df_hosp["mois"] = df_hosp["jour"].astype(str).str[5:7]
df_hosp["annee"] = df_hosp["jour"].astype(str).str[:4]
#on regroupe par département par mois de l'année
df_hosp = df_hosp.groupby(['dep','annee','mois']).sum()

# Nettoyage de la base des urgences

df_urgences = df_urgences[['dep',
'date_de_passage','sursaud_cl_age_corona','nbre_pass_corona', 'nbre_pass_tot', 'nbre_pass_corona', 'nbre_pass_tot',
'nbre_pass_corona', 'nbre_pass_tot']]
#on remplit les valeurs non renseignées par 0 
df_urgences.fillna(0)
df_urgences["dep"] = df_urgences['dep'].astype(str)
df_urgences["mois"] = df_urgences["date_de_passage"].astype(str).str[5:7]
df_urgences["annee"] = df_urgences["date_de_passage"].astype(str).str[:4]
df_urgences = df_urgences.groupby(['dep','annee','mois','sursaud_cl_age_corona']).sum()

# Nettoyage de la base des dépistages

"""
A FAIRE
"""

# Nettoyage de la base des établissements

"""
A FAIRE
"""

# Nettoyage de la base de l'espérance de vie

df_espvie = pd.read_excel(df_espvie, skiprows=5, header=[0])
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

# Nettoyage de la base des taux de mortalité

"""
A FAIRE
"""

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
row_to_drop = df_vieil.loc[(df_vieil["num_dep"]=="P")|(df_vieil["num_dep"]=="M")].index
df_vieil.drop(row_to_drop, inplace=True)

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