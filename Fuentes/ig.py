import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Normalización con función sigmoidal
def norm_data_sigmoidal(data):
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data.iloc[:, :-1])  # Normaliza todas las columnas excepto la última (la clase)
    return pd.DataFrame(normalized_data, columns=data.columns[:-1]), data.iloc[:, -1]  # La última columna es la clase


# Cálculo de la ganancia de información (ejemplo con valores aleatorios)
def inform_gain(X, y):    
    gains = np.random.rand(X.shape[1])  # Genera valores aleatorios para ilustración
    return gains


# Cargar el archivo de datos
def load_data():   
    #column_names = ['feature_' + str(i) for i in range(1, 41)] + ['class']  # Nombres de columnas de características y clase
    data = pd.read_csv('DATA/DataClass.csv', header=None)
    return data


# Selección de las Top-K variables basadas en la ganancia de información
def select_top_k_variables(X, gains, top_k):
    idx = np.argsort(gains)[-top_k:]  # Índices de las Top-K variables
    return X.iloc[:, idx]


def main():    
    data = load_data()
    X, y = norm_data_sigmoidal(data)
    gains = inform_gain(X, y)  # Llamada corregida a 'inform_gain'
    
    top_k = 25  # Número de variables a seleccionar, puede ajustarse según el archivo config.csv
    X_top_k = select_top_k_variables(X, gains, top_k)
    
    # Añadir la clase de vuelta de forma segura
    X_top_k = X_top_k.copy()  # Hace una copia para evitar el SettingWithCopyWarning
    X_top_k.loc[:, 'class'] = y.values  # Usar loc para añadir la columna de clase
    X_top_k.to_csv('DataIG.csv', index=False)
    pd.DataFrame(gains, columns=['information_gain']).to_csv('Idx_variable.csv', index=False)  # Guarda índices ordenados



if __name__ == '__main__':   
    main()
