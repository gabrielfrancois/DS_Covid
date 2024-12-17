from csv import *
import requests as rqst
import matplotlib.pyplot as graph
import pandas as pd

def import_file_from_web(url, filename):
	"""
	Inputs :
	url (string) : url exact de la base de données
	filename (string) : nom du fichier contenant les données.
	
	Output :
	Void
	"""
	req = rqst.get(url)
	url_content = req.content #On importe les données du lien de téléchargement du fichier csv
	csv_file = open(filename, 'wb') #On ouvre un nouveau fichier csv où on recopie toutes les données
	csv_file.write(url_content)
	csv_file.close()


def import_data_on_python(filename):
	"""
	Inputs :
	filename (string) : nom du fichier contenant les données.
	
	Output :
	data frame pandas
	"""
	return pd.read_csv(filename)




# import_file_from_web()
# casCovid = import_data_on_python()

#totalhp = 0
#totalrea = 0
#totalrad = 0
#totaldc = 0
#ltotalhp = []
#with open('CovidNational.csv', 'w', newline='') as csvfile2: #On crée un autre csv nommé CovidNational, qui contiendra les totaux à l'échelle nationale pour chaque jour
#    writer2 = writer(csvfile2)
#    writer2.writerow(['date;t;totalhp;totalrea;totalrad;totaldc']) #Entête du tableau
#    ref = casCovid[0][2] #Etant donné que la date va changer à un moment, on garde une date de référence dès le premier département, qu'on changera ensuite quand on passera à la date suivante
#    for i in range(1, len(casCovid)):
#        if casCovid[i][2] == "27/06/2020": #Les trois if enlèvent une erreur qui se produit avec ces trois dates, qui apparaissent en format JJ/MM/AAAA plutôt que AAAA-MM-JJ
#            casCovid[i][2] = "2020-06-27"
#        elif casCovid[i][2] == "28/06/2020":
#            casCovid[i][2] = "2020-06-28"
#        elif casCovid[i][2] == "29/06/2020":
#            casCovid[i][2] = "2020-06-29"
#        if casCovid[i][2] != ref: #On vérifie si l'on est passé à la date suivante
#            j = int((i / 94) - 1)
#            writer2.writerow([ref + ";" + str(j)  + ";" + str(totalhp) + ";" + str(totalrea) + ";" + str(totalrad) + ";" + str(totaldc)]) #Dans ce cas, on écrit dans le csv la ligne avec les totaux pour la date là
#            ref = casCovid[i][2] #Et on change la date
#            ltotalhp.append(totalhp)
#            totalhp = 0 #En remettant tous les compteurs à zéro
#            totalrea = 0
#            totalrad = 0
#            totaldc = 0
#        else:
#            totalhp += int(casCovid[i][3])
#            totalrea += int(casCovid[i][4])
#            totalrad += int(casCovid[i][5])
#            totaldc += int(casCovid[i][6])
#
#def CalculHP(t):
#    n = int(t)
#    return ltotalhp[n] + (t-n)*(ltotalhp[n+1]-ltotalhp[n])
#
#print(CalculHP(13.8))





