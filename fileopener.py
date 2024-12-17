from csv import *
import requests as rqst
import matplotlib.pyplot as graph
import pandas as pd

def import_data_csv_to_pandas(filename):
	"""
	Inputs :
	url (string) : url exact de la base de données
	
	Output :
	data frame pandas
	"""
	return pd.read_csv(url, encoding="latin1")


def import_data_excel_to_pandas(url):
	return pd.read_excel(url)

def dataframes(file):
	reader1 = reader(file, delimiter = ",")
	dataframe_list = []
	for ligne in reader1:
		if ligne[0] == "csv":
			dataframe_list.append(import_data_csv_to_pandas(ligne1))

# import_file_from_web()
# casCovid = import_data_on_python()
