import os
import logging
from env.env import dir_log

# Ruta del archivo de log
log_file = os.path.join(dir_log, "log.txt")

# Configuración de logging
logging.basicConfig(
    filename=log_file,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

# Handler para mostrar los logs en la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Añadir el handler al logger
logging.getLogger().addHandler(console_handler)

# Exportar el logger global
logging_api = logging.getLogger()

