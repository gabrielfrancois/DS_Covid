import pandas as pd
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