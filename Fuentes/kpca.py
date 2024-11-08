# Kernel-PCA by use Gaussian function

import numpy as np
import pandas as pd



def kernel_gauss(X, sigma):
    """Calcula el Kernel Gaussiano para la matriz de datos X."""
    n = X.shape[0]
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            diff = X[i] - X[j]
            K[i, j] = np.exp(-np.dot(diff, diff) / (2 * sigma**2))
    return K


# Gaussian Kernel
def kpca_gauss(X, sigma, top_k):
    """Aplica Kernel PCA y devuelve las primeras top_k componentes principales."""
    K = kernel_gauss(X, sigma)

    # Centrar el kernel
    N = K.shape[0]
    one_n = np.ones((N, N)) / N
    K_centered = K - one_n @ K - K @ one_n + one_n @ K @ one_n

    # Descomposición en valores y vectores propios
    eigenvalues, eigenvectors = np.linalg.eigh(K_centered)

    # Ordenar y seleccionar Top-K componentes principales
    idx = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, idx]
    eigenvalues = eigenvalues[idx]
    top_eigenvectors = eigenvectors[:, :top_k]

    # Transformación de datos
    X_kpca = K @ top_eigenvectors
    return X_kpca


# 
def load_data():
    data = pd.read_csv('DataIG.csv')
    X = data.iloc[:3000, :-1].values  # Selecciona las primeras 3000 muestras
    return X


# Beginning ...
def main():			
    X = load_data()
    sigma = 6.5  # Define según config.csv
    top_k = 10   # Define según config.csv
    X_kpca = kpca_gauss(X, sigma, top_k)
    np.savetxt('DataKpca.csv', X_kpca, delimiter=",")

		

if __name__ == '__main__':   
	 main()

