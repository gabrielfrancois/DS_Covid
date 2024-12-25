from csv import *
import requests as rqst
import matplotlib.pyplot as graph
import pandas as pd
import numpy as np
import requests
import zipfile
import io


def import_data_csv_to_pandas(url):
	"""
	Input :
	url (str) : url exact de la base de données
	
	Output :
	df (dataframe pandas) :  tableau pandas contenant la base de données
	"""
	df = pd.read_csv(url, delimiter = ";", encoding="utf-8", low_memory=False)
	return df


def dataframe_etablissement(url):
	"""
	Input :
	url (str) : lien url de la base de données

	Output :
	df_etablissement (dataframe pandas) : tableau pandas de la base des établissements de santé
	"""
	df_etablissement = pd.read_csv(url, delimiter = ";", encoding = "utf-8", skiprows = 1, header = None, low_memory = False)
	return(df_etablissement)

def dataframe_xlsx_format0(url):
	"""
	Input :
	url (str) : lien url de la base de données

	Output :
	df (dataframe pandas) : tableau pandas de la base de données données en entrée
	"""
	df = pd.read_excel(url, skiprows=4, header=[1])
	return(df)

def dataframe_xlsx_format1(url):
	"""
	Input :
	url (str) : lien url de la base de données

	Output :
	df_pauv (dataframe pandas) : tableau pandas de la base de données données en entrée
	"""
	df = pd.read_excel(url, skiprows=5, header=[0])
	return(df)

def dataframe_zip(url):
	"""
	Input :
	url (str) : lien url de téléchargement du zip contenant les bases de données des décès en France entre 2018 et 2023 inclus

	Output:
	final_df (dataframe pandas) : tableau pandas final contenant les multiples bases de données concaténées
	"""

	# Télécharger le fichier ZIP
	response = requests.get(url)
	final_df = pd.Dataframe()
	if response.status_code == 200:
		# Charger le contenu du ZIP en mémoire
		zip_file = zipfile.ZipFile(io.BytesIO(response.content))

		# Liste des fichiers CSV dans l'archive
		csv_files = [name for name in zip_file.namelist() if name.endswith('.csv')]

		# Lire chaque fichier CSV directement en DataFrame
		dataframes = []
		for csv_file in csv_files:
			if csv_file != "metadonnees_deces_ficdet.csv" and csv_file != "DC_2018_det.csv":
				with zip_file.open(csv_file) as file:  # Ouvrir le fichier CSV dans le ZIP
					df = pd.read_csv(file, delimiter = ";")  # Lire le CSV dans un DataFrame
					dataframes.append(df)

		# Combiner tous les DataFrames
		final_df = pd.concat(dataframes)
	else:
		raise Exception(f"Échec du téléchargement : Code HTTP {response.status_code}")	
	return final_df
	

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
			dataframe_list.append(pd.read_csv(ligne[1], delimiter = ";", encoding = "utf-8", skiprows = 1, header = None, low_memory = False))
		elif ligne[0] == "csv":
			dataframe_list.append(import_data_csv_to_pandas(ligne[1]))
		elif ligne[0] == "xlsx0":
			dataframe_list.append(dataframe_xlsx_format0(ligne[1]))
		elif ligne[0] == "xlsx1":
			dataframe_list.append(dataframe_xlsx_format1(ligne[1]))
		elif ligne[0] == "zip":
			dataframe_list.append(dataframe_zip(ligne[1]))
	return dataframe_list




