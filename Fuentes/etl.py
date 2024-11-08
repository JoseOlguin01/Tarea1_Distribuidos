import numpy as np
import pandas as pd

def config():
    config = pd.read_csv('config.csv', header=None)
    parameters = config.values
    m = parameters[0][0]             # Dimensión embebida (m)
    tau = parameters[1][0]           # Factor de retardo embebido (tau)
    c = parameters[2][0]             # Número de símbolos (c)
    vRK = parameters[3][0]           # Top-K variables relevantes
    sigma = parameters[4][0]         # Sigma (ancho del Kernel)
    vMRK = parameters[5][0]          # Top-K variables menos redundantes
    M = int(parameters[6][0])        # Número de muestras (M) para cada clase
    return m, tau, c, vRK, sigma, vMRK, M

# Paso 1: Procesar datos originales y transformar a formato numérico
def process_data():
    data = pd.read_csv('DATA/KDDTrain.txt', header=None)
    
    # Asignar valores numéricos a las columnas categóricas
    data[1] = data[1].astype('category').cat.codes
    data[2] = data[2].astype('category').cat.codes
    data[3] = data[3].astype('category').cat.codes
    data[41] = data[41].astype(str)  # Convertir a string para coincidencia de ataques

    # Guardar datos transformados (sin columna de clase) en Data.csv
    data.iloc[:, :-1].to_csv('DATA/Data.csv', index=False, header=False)

# Paso 2: Clasificar tráfico en normal, DOS, y Probe
def classify_traffic():
    data = pd.read_csv('DATA/KDDTrain.txt', header=None)
    data[1] = data[1].astype('category').cat.codes
    data[2] = data[2].astype('category').cat.codes
    data[3] = data[3].astype('category').cat.codes
    data[41] = data[41].astype(str)

    dos_attacks = {'neptune', 'teardrop', 'smurf', 'pod', 'back', 'land', 'apache2', 'processtable', 'mailbomb', 'udpstorm'}
    probe_attacks = {'ipsweep', 'portsweep', 'nmap', 'satan', 'saint', 'mscan'}

    # Excluir la columna de clase al crear archivos de cada clase
    normal_traffic = data[data[41] == 'normal'].iloc[:, :-1]
    dos_traffic = data[data[41].isin(dos_attacks)].iloc[:, :-1]
    probe_traffic = data[data[41].isin(probe_attacks)].iloc[:, :-1]

    # Guardar archivos de cada clase con 41 columnas
    normal_traffic.to_csv('DATA/class1.csv', index=False, header=False)
    dos_traffic.to_csv('DATA/class2.csv', index=False, header=False)
    probe_traffic.to_csv('DATA/class3.csv', index=False, header=False)

# Paso 3 y 4: Seleccionar muestras aleatorias y combinar en DataClass.csv
def select_samples():
    _, _, _, _, _, _, M = config()
    
    try:
        # Cargar índices y datos
        idx_class1 = pd.read_csv('DATA/idx_class1.csv', header=None).squeeze()
        idx_class2 = pd.read_csv('DATA/idx_class2.csv', header=None).squeeze()
        idx_class3 = pd.read_csv('DATA/idx_class3.csv', header=None).squeeze()
        class1 = pd.read_csv('DATA/class1.csv', header=None)
        class2 = pd.read_csv('DATA/class2.csv', header=None)
        class3 = pd.read_csv('DATA/class3.csv', header=None)

        # Validar y ajustar índices
        idx_class1 = idx_class1[idx_class1 < len(class1)]
        idx_class2 = idx_class2[idx_class2 < len(class2)]
        idx_class3 = idx_class3[idx_class3 < len(class3)]

        # Seleccionar M muestras (rellenar si es necesario)
        class1_selected = class1.iloc[idx_class1].copy() if len(idx_class1) >= M else class1.sample(M, replace=True).copy()
        class1_selected.loc[:, 'class'] = 1
        class2_selected = class2.iloc[idx_class2].copy() if len(idx_class2) >= M else class2.sample(M, replace=True).copy()
        class2_selected.loc[:, 'class'] = 2
        class3_selected = class3.iloc[idx_class3].copy() if len(idx_class3) >= M else class3.sample(M, replace=True).copy()
        class3_selected.loc[:, 'class'] = 3

        # Combinar todos los datos y guardar con tamaño 3M x 42
        data_class = pd.concat([class1_selected, class2_selected, class3_selected], axis=0).reset_index(drop=True)
        data_class.to_csv('DATA/DataClass.csv', index=False, header=False)

    except Exception as e:
        print("Error al seleccionar muestras:", e)

def main():
    process_data()
    classify_traffic()
    select_samples()
    print("ETL completado y DataClass.csv creado en la carpeta DATA.")

if __name__ == '__main__':
    main()
