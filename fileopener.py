from csv import *
import requests as rqst
import matplotlib.pyplot as graph
import pandas as pd

def import_data_csv_to_pandas(url):
	"""
	Input :
	url (string) : url exact de la base de données
	
	Output :
	df (dataframe pandas) :  tableau pandas contenant la base de données
	"""
	df = pd.read_csv(url, delimiter = ";", encoding="utf-8")
	return df


def import_data_excel_to_pandas(url):
	"""
	Input :
	url (string) : url exact de la base de données
	
	Output :
	df (dataframe pandas) :  tableau pandas contenant la base de données
	"""
	df = pd.read_excel(url)
	return df

def dataframe_creator(filename):
	"""
	Input : 
	filename (string) : nom du fichier contenant la liste des liens de téléchargement des bases de données requises pour le projet
					Les lignes sont de la forme "format,lien".
	
	Output :
	dataframe_list (dataframe pandas list) : liste de tableau pandas correspondant à chaque base de données
	"""
	file = open(filename, "r")
	dataframe_list = []
	reader1 = reader(file, delimiter = ",")
	for ligne in reader1:
		if ligne[1] == "https://www.data.gouv.fr/fr/datasets/r/2ce43ade-8d2c-4d1d-81da-ca06c82abc68":
			pass
		elif ligne[0] == "csv":
			dataframe_list.append(import_data_csv_to_pandas(ligne[1]))
		elif ligne[0] == "xlsx":
			dataframe_list.append(import_data_excel_to_pandas(ligne[1]))
	return dataframe_list

def dataframe_etablissement():
    """
    Input :
    void

    Output :
    df_etablissement (dataframe pandas) : tableau pandas de la base des établissements de santé
    """
    df_etablissement = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/2ce43ade-8d2c-4d1d-81da-ca06c82abc68", delimiter = ";", encoding = "utf-8", skiprows = 1, header = None, low_memory = False)
    return(df_etablissement)



