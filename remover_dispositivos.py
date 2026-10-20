import os
import requests
import msal
import logging
 
# --- CONFIGURAÇÕES ---
CLIENT_ID = 'seu-client-id'
CLIENT_SECRET = 'seu-client-secret'
TENANT_ID = 'seu-tenant-id'
CAMINHO_PASTA = './maquinas_seriais'
LOG_FILE = 'erro_intune.log'
 
# Configuração básica de log
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
 
# --- AUTENTICAÇÃO (MSAL) ---
authority = f"https://login.microsoftonline.com/{TENANT_ID}"
app = msal.ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
 
if "access_token" not in token_response:
    print("Erro na autenticação!")
    exit()
 
headers = {
    'Authorization': f"Bearer {token_response['access_token']}",
    'Content-Type': 'application/json'
}
 
# --- PROCESSAMENTO ---
def processar_remocao():
    if not os.path.exists(CAMINHO_PASTA):
        print("Pasta não encontrada.")
        return
 
    for arquivo in os.listdir(CAMINHO_PASTA):
        # Pega o nome do arquivo sem a extensão (o Serial)
        serial = os.path.splitext(arquivo)[0]
        print(f"Buscando Serial: {serial}...")
 
        # 1. Buscar o ID do dispositivo pelo Serial
        url_busca = f"https://graph.microsoft.com/v1.0/deviceManagement/managedDevices?$filter=serialNumber eq '{serial}'"
        
        try:
            response = requests.get(url_busca, headers=headers)
            response.raise_for_status()
            data = response.json()
 
            if data['value']:
                device_id = data['value'][0]['id']
                
                # 2. Deletar o dispositivo encontrado
                url_delete = f"https://graph.microsoft.com/v1.0/deviceManagement/managedDevices/{device_id}"
                del_res = requests.delete(url_delete, headers=headers)
                
                if del_res.status_code == 204:
                    print(f"Sucesso: {serial} removido.")
                else:
                    logging.error(f"Erro ao deletar {serial}: Status {del_res.status_code}")
            else:
                # Se a lista 'value' estiver vazia, o serial não existe no Intune
                msg = f"Serial {serial} não localizado no Intune."
                print(f"Aviso: {msg}")
                logging.error(msg)
 
        except Exception as e:
            logging.error(f"Falha crítica no processamento do serial {serial}: {str(e)}")
 
if __name__ == "__main__":
    processar_remocao()
