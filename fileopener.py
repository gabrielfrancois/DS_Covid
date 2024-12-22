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
	df = pd.read_csv(url, encoding="latin1")
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
	reader1 = reader(file, delimiter = ",")
	dataframe_list = []
	for ligne in reader1:
		print(ligne)
		if ligne[0] == "csv":
			print("csv")
			dataframe_list.append(import_data_csv_to_pandas(ligne[1]))
		elif ligne[0] == "xlsx":
			dataframe_list.append(import_data_excel_to_pandas(ligne[1]))
	return dataframe_list



