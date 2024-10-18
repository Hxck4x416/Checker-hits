import os

# Obtiene la ruta del directorio actual
directorio_actual = os.getcwd()

# Nombre de la subcarpeta
nombre_subcarpeta = 'cuentas'

# Construye la ruta completa a la subcarpeta
ruta_subcarpeta = os.path.join(directorio_actual, nombre_subcarpeta)

# Imprime la ruta
print("La ruta de la subcarpeta es:", ruta_subcarpeta)

# Ahora puedes usar esta ruta para acceder a los archivos dentro de 'subcarpeta'