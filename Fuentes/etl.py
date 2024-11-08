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

def get_attack_class(attack_type):
    dos_attacks = {'neptune', 'teardrop', 'smurf', 'pod', 'back', 'land', 'apache2', 'processtable', 'mailbomb', 'udpstorm'}
    probe_attacks = {'ipsweep', 'portsweep', 'nmap', 'satan', 'saint', 'mscan'}
    
    if attack_type == 'normal':
        return 1
    elif attack_type in dos_attacks:
        return 2
    elif attack_type in probe_attacks:
        return 3
    else:
        return 0

# Paso 1: Procesar datos originales y transformar a formato numérico
def process_data():
    data = pd.read_csv('DATA/KDDTrain.txt', header=None)
    
    # Asignar valores numéricos a las columnas categóricas
    data[1] = data[1].astype('category').cat.codes
    data[2] = data[2].astype('category').cat.codes
    data[3] = data[3].astype('category').cat.codes
    
    # Convertir tipos de ataque a valores numéricos
    data[41] = data[41].astype(str).apply(get_attack_class)
    
    # Guardar datos transformados en Data.csv (25192, 41) incluyendo la columna de clase numérica
    data.iloc[:, :-1].to_csv('DATA/Data.csv', index=False, header=False)

# Paso 2: Clasificar tráfico en normal, DOS, y Probe
def classify_traffic():
    data = pd.read_csv('DATA/KDDTrain.txt', header=None)
    data[1] = data[1].astype('category').cat.codes
    data[2] = data[2].astype('category').cat.codes
    data[3] = data[3].astype('category').cat.codes
    data[41] = data[41].astype(str).apply(get_attack_class)

    # Excluir la columna de clase al crear archivos de cada clase (41 columnas)
    normal_traffic = data[data[41] == 1].iloc[:, :-1]  # (13449, 41)
    dos_traffic = data[data[41] == 2].iloc[:, :-1]     # (9234, 41)
    probe_traffic = data[data[41] == 3].iloc[:, :-1]   # (2289, 41)

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
        class1_selected = class1.iloc[idx_class1].copy() if len(idx_class1) >= 3 else class1.sample(3, replace=True).copy()
        class1_selected['class'] = 1  # Agregar columna de clase
        
        class2_selected = class2.iloc[idx_class2].copy() if len(idx_class2) >= 3 else class2.sample(3, replace=True).copy()
        class2_selected['class'] = 2  # Agregar columna de clase
        
        class3_selected = class3.iloc[idx_class3].copy() if len(idx_class3) >= 3 else class3.sample(3, replace=True).copy()
        class3_selected['class'] = 3  # Agregar columna de clase

        # Combinar todos los datos y guardar (3M, 42)
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
