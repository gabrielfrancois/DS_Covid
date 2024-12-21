import pandas as pd
#ouverture du fichier et création df avec les colonnes qui nous intéressent
url_donnees_hosp = 'https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c'
#df_hosp = pd.read_csv(url_donnees_hosp, usecols=['dep','date_de_passage','sursaud_cl_age_corona','nbre_pass_corona','nbre_hospit_corona','nbre_acte_corona','nbre_pass_tot','nbre_acte_tot'])
df_hosp = pd.read_csv(url_donnees_hosp, sep=";")
df_hosp["mois"] = df_hosp["jour"].astype(str).str[5:7]
df_hosp["annee"] = df_hosp["jour"].astype(str).str[:4]

df_hosp_modifie = df_hosp.groupby(['dep','annee','mois']).sum()
print(df_hosp_modifie.head())
