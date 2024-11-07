# -------------------------------------------------------
# Load Data from File: KDDTrain.txt
# --------------------------------------------------------

import numpy as np
import pandas as pd
# import utility_etl  as ut

# Cargar parametros de config.csv


def config():
    config = pd.read_csv(
        r'D:\Codigos\Universidad\Sistema Distribuido\github\Tarea1_Distribuidos\config.csv', header=None)
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
    data = pd.read_csv(
        r'D:\Codigos\Universidad\Sistema Distribuido\github\Tarea1_Distribuidos\DATA\KDDTrain.txt', header=None)
    # Listados de las clases
    Clase1 = ['normal']
    Clase2 = ['neptune', 'teardrop', 'smurf', 'pod', 'back', 'land', 'apache2',
              'processtable', 'mailbomb', 'udpstorm']
    Clase3 = ['ipsweep', 'portsweep', 'nmap', 'satan', 'saint', 'mscan']
    # Listado de  protocolos
    protocolos = ['tcp', 'udp', 'icmp']
    # Listado de servicios
    servicios = ['ftp_data', 'other', 'private', 'http', 'remote_job', 'name', 'netbios_ns'
                 'eco_i', 'mtp', 'telnet', 'finger', 'domain_u', 'supdup', 'uucp_path', 'Z39_50'
                 'smtp', 'csnet_ns', 'uucp', 'netbios_dgm', 'urp_i', 'auth', 'domain', 'ftp'
                 'bgp', 'ldap', 'ecr_i', 'gopher', 'vmnet', 'systat', 'http_443', 'efs', 'whois'
                 'imap4', 'iso_tsap', 'echo', 'klogin', 'link', 'sunrpc', 'login', 'kshell'
                 'sql_net', 'time', 'hostnames', 'exec', 'ntp_u', 'discard', 'nntp', 'courier'
                 'ctf', 'ssh', 'daytime', 'shell', 'netstat', 'pop_3', 'nnsp', 'IRC', 'pop_2'
                 'printer', 'tim_i', 'pm_dump', 'red_i', 'netbios_ssn', 'rje', 'X11', 'urh_i'
                 'http_8001']

    # Listado de flags
    flags = ['SF', 'S0', 'REJ', 'RSTR', 'SH', 'RSTO', 'S1', 'RSTOS0', 'S3', 'S2', 'OTH']


    # Paso 1
    # Paso 1.1: Transformar los datos originales en formato numérico.
    data = data.replace(Clase1, 1)
    data = data.replace(Clase2, 2)
    data = data.replace(Clase3, 3)
    for i in range(len(protocolos)):
        data = data.replace(protocolos[i], i+1)
    for i in range(len(servicios)):
        data = data.replace(servicios[i], i+1)
    for i in range(len(flags)):
        data = data.replace(flags[i], i+1)
    

    # print primera fila 
    print(data.head(1))




if __name__ == '__main__':
    main()
