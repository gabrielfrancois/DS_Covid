from datapreprocessing import df_final

#les départements avec les plus grands ratios patients positifs/population
df_final.nlargest(5, "taux d'incidence", keep = "all")

#les départements avec les plus petits ratios patients positifs/population
df_final.nsmallest(5, "taux d'incidence", keep = "all")