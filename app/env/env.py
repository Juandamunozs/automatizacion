import os

dir_proyect = os.path.dirname(os.path.abspath(__file__))

# Ruta de la carpeta 'res'
dir_res = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'res')

# Ruta de la carpeta 'logs'
dir_log = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')

# Verificar si la carpeta 'res' existe; si no, crearla
if not os.path.exists(dir_res):
    os.makedirs(dir_res)

# Verificar si la carpeta 'logs' existe; si no, crearla
if not os.path.exists(dir_log):
    os.makedirs(dir_log)