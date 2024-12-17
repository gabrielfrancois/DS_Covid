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
	return pd.read_csv(filename, encoding="latin1")


def import_data_excel_to_pandas(url):
	pd.read_excel(url)



import_file_from_web()
casCovid = import_data_on_python()
