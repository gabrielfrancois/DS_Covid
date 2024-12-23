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


def dataframe_etablissement(url):
    """
    Input :
    url : lien url de la base de données

    Output :
    df_etablissement (dataframe pandas) : tableau pandas de la base des établissements de santé
    """
    df_etablissement = pd.read_csv(url, delimiter = ";", encoding = "utf-8", skiprows = 1, header = None, low_memory = False)
    return(df_etablissement)

def dataframe_xlsx_format0(url):
    """
    Input :
    url : lien url de la base de données

    Output :
    df (dataframe pandas) : tableau pandas de la base de données données en entrée
    """
    df = pd.read_excel(url, skiprows=4, header=[1])
    return(df)

def dataframe_xlsx_format1(url):
    """
    Input :
    url : lien url de la base de données

    Output :
    df_pauv (dataframe pandas) : tableau pandas de la base de données données en entrée
    """
    df = pd.read_excel(url, skiprows=5, header=[0])
    return(df)
    

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
    print(len(reader1))
	for ligne in reader1:
		if ligne[1] == "https://www.data.gouv.fr/fr/datasets/r/2ce43ade-8d2c-4d1d-81da-ca06c82abc68":
			pass
		elif ligne[0] == "csv":
			dataframe_list.append(import_data_csv_to_pandas(ligne[1]))
		elif ligne[0] == "xlsx0":
            dataframe_list.append(dataframe_xlsx_format0(ligne[1]))
		elif ligne[0] == "xlsx1":
            dataframe_list.append(dataframe_xlsx_format1(ligne[1]))
	return dataframe_list




