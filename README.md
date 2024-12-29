Ce projet Github est réalisé dans le cadre du projet de Python pour la Data Science de deuxième année à l'ENSAE.
Il vise à étudier des facteurs géographiques et socio-démographiques de la mortalité du Covid sur le territoire métropolitain français, à partir de données ministérielles. 

Le fichier main.ipynb contient le coeur du projet et représente intégralement le projet. Comme précisé au sein de ce fichier, il est important au préalable d'installer les packages pythons requis via un terminal. La liste des packages requis est présente dans le fichier requirements.txt. Une seule commande pip install -r DS_Covid/requirements.txt permet d'installer tous les packages requis.
Le csv finaldata.csv permet malgré tout l'affichage des analyses statistiques et de la modification sans l'import des données depuis le web, en cas de problème de connexion ou problème technique. Il faut alors simplement intégrer dans le main la ligne de code suivante :

df_final = pd.read_csv("finaldata.csv")

Bonne lecture !