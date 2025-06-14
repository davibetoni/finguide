import os
import string
import secrets
import pyAesCrypt
from openpyxl import Workbook
from utils import get_data_file
from email_utils import send_email_report

def initialize_system():
    """Inicializa o sistema garantindo que o arquivo Excel e .env existam"""
    create_protected_excel()

def logout_system(password):
    """Desloga o usuário e cripgrafa novamente o arquivo Excel"""
    file_path = get_data_file()
    if os.path.exists(file_path):
        encrypt_excel_file(file_path, password)
    else:
        print("Arquivo Excel não encontrado para criptografia.")

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(characters) for _ in range(length))

def check_password(input_password):
    """Compara a senha informada com o hash salvo"""
    return decrypt_excel_file(get_data_file(), input_password) is not None

def create_protected_excel():
    """Cria o arquivo Excel protegido, gera senha e salva hash"""
    file_path = get_data_file()

    if not os.path.exists(file_path):
        # Criação do arquivo com aba temporária
        wb = Workbook()
        ws = wb.active
        ws.title = "template"
        ws.append(["date", "description", "amount", "category", "source"])
        wb.save(file_path)

        # Geração de senha aleatória e salvamento do hash
        password = generate_random_password()
        
        send_email_report(
            subject="Senha do arquivo Excel",
            body=f"Senha para acessar o arquivo Excel: {password}",
        )

        encrypt_excel_file(file_path, password)

        print(f"🔐 Arquivo criado com senha: {password}")

def encrypt_excel_file(path, password):
    encrypted_path = path + ".aes"
    pyAesCrypt.encryptFile(path, encrypted_path, password, bufferSize=64*1024)
    os.remove(path)
    os.rename(encrypted_path, path)
    
def decrypt_excel_file(path, password):
    try: 
        decrypted_path = path + ".decrypted"
        pyAesCrypt.decryptFile(path, decrypted_path, password, bufferSize=64*1024)
        os.remove(path)
        os.rename(decrypted_path, path)
        
        return path
    except ValueError:
        print("🔒 Senha incorreta ou arquivo corrompido.")
        return None