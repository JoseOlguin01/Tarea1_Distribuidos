#-------------------------------------------------------
# Load Data from File: KDDTrain.txt
#--------------------------------------------------------

import numpy   as np
import pandas  as pd
#import utility_etl  as ut

# Cargar parametros de config.csv
def config():
    config = pd.read_csv('config.csv',header=None)
    parameters = config.values
    # Línea 1: Dimensión embebida (m) de DE.
    m = parameters[0][0]
    # Línea 2: Factor de retardo embebido (tau) de DE.
    tau = parameters[1][0]
    # Línea 3: Número símbolos (c) de DE.
    c = parameters[2][0]
    # Línea 4: Top-K variables relevantes.
    vRK = parameters[3][0]
    # Línea 5: Sigma: ancho del Kernel.
    sigma = parameters[4][0]
    # Línea 6: Top-K variables menos redundantes.
    vMRK = parameters[5][0]
    
# Beginning ...
def main():
    config()
    data=pd.read_csv(r'D:\Codigos\Universidad\Sistema Distribuido\Eva3\Codigo\DATA\KDDTrain.txt',header=None)
    # asignar valores numericos a las variables categoricas
    data[1]=data[1].astype('category').cat.codes
    data[2]=data[2].astype('category').cat.codes
    data[3]=data[3].astype('category').cat.codes
    data[41]=data[41].astype('category').cat.codes
    print(data)
    print(data[1].unique())
    print(data[2].unique())
    print(data[3].unique())
    print(data[41].unique())
    

if __name__ == '__main__':   
	 main()

