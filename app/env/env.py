import os

dir_proyect = os.path.dirname(os.path.abspath(__file__))

# Ruta de la carpeta 'res'
dir_res = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'res')

# Verificar si la carpeta 'res' existe; si no, crearla
if not os.path.exists(dir_res):
    os.makedirs(dir_res)