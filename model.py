from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LassoCV
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

from datapreprocessing import *

indep_var = ["espérance de vie", "pop_totale", "rapport nv_vie interdécile D9/D1", "indicateur pauvreté 1", "indicateur pauvreté 2", "nb_etab_sante", "ratio population/etab"]
X = df_final[indep_var]
y = df_final["nb deces"]

scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

""" Régression linéaire des Moindres Carrées Ordinaires """
X_reg = sm.add_constant(df_final[indep_var], prepend = False)
mod = sm.OLS(y, X_reg)
res = mod.fit()

#sm.graphics.plot_partregress('nb deces', 'ratio population/etab', ["espérance de vie", "pop_totale", "rapport nv_vie interdécile D9/D1", "indicateur pauvreté 1", "indicateur pauvreté 2", "nb_etab_sante"], data=df_final, obs_labels=False)

# Split des données
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

""" Modèle Random Forest """

# Entraînement du modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Évaluation
rmse = mean_squared_error(y_test, y_pred)
#print(f"RMSE : {rmse}")

importances = model.feature_importances_
features = X.columns

# Importance des variables
#print("RandomForest")
feature_importances = pd.DataFrame({"feature": features, "importance": importances})
#print(feature_importances.sort_values(by="importance", ascending=False))

"""Modèle SVM"""

# Division en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardisation des données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# SVM avec noyau RBF (Radial Basis Function)
svm_model = SVR(kernel="rbf", C=10, gamma= 0.1)  # C = Régularisation, gamma = paramètre RBF
svm_model.fit(X_train, y_train)

# Prédictions
y_pred = svm_model.predict(X_test)

# Évaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
#print(f"Mean Squared Error (MSE): {mse}")
#print(f"R² Score: {r2}")

"""
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # Ligne parfaite
plt.xlabel("Valeurs réelles")
plt.ylabel("Prédictions")
plt.title("Valeurs réelles vs Prédictions")
plt.show()
"""

"""Code Ridge"""

# Pipeline : Polynômes + Ridge
pipeline_ridge = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),  # Relations polynomiales
    ('ridge', RidgeCV(alphas=np.logspace(-4, 4, 100), cv=5))  # Régression Ridge avec validation croisée
])

# Entraînement du modèle
pipeline_ridge.fit(X_train, y_train)

# Extraction des coefficients
coefficients = pipeline_ridge.named_steps['ridge'].coef_

# Noms des variables (incluant les termes polynomiaux)
feature_names = pipeline_ridge.named_steps['poly'].get_feature_names_out(X.columns)

# DataFrame pour analyse
coef_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': coefficients
})


# Prédictions sur les données de test
y_pred = pipeline_ridge.predict(X_test)

# Calcul des métriques
mse = mean_squared_error(y_test, y_pred)  # Mean Squared Error
mae = mean_absolute_error(y_test, y_pred)  # Mean Absolute Error
r2 = r2_score(y_test, y_pred)  # R² score

"""
# Barplot des coefficients les plus importants
top_features = coef_df.sort_values(by="Coefficient", key=abs, ascending=False).head(10)  # Top 10
print(top_features)
plt.figure(figsize=(10, 6))
plt.barh(top_features["Feature"], top_features["Coefficient"], color="skyblue")
plt.xlabel("Coefficient")
plt.ylabel("Variable")
plt.title("Importance des variables dans la régression Ridge (avec polynômes)")
plt.gca().invert_yaxis()
plt.show()
"""