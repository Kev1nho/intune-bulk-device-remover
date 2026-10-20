# Intune Bulk Device Remover 🛠️

Este projeto consiste em um script automatizado em Python que se integra à **Microsoft Graph API** para realizar a busca e a exclusão em massa de dispositivos gerenciados no **Microsoft Intune**, utilizando como critério o número de série das máquinas.

Solução ideal para equipes de Infraestrutura, SysOps e Helpdesk que precisam realizar processos de *offboarding* ou limpeza de inventário em larga escala de forma ágil e segura.

## 🚀 Funcionalidades

- **Autenticação Segura:** Implementação do fluxo de credenciais de cliente OAuth 2.0 utilizando a biblioteca oficial `msal` (Microsoft Authentication Library).
- **Processamento em Lote:** Varredura automática de uma pasta local estruturada para processar múltiplos ativos sequencialmente.
- **Tratamento de Erros e Logs:** Sistema de logging robusto que registra falhas operacionais e seriais não localizados sem interromper a execução do script.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Microsoft Graph API** (Endpoint: `/deviceManagement/managedDevices`)
- **MSAL (Microsoft Authentication Library)**
- **Requests** (Para requisições HTTP REST)

## 📋 Pré-requisitos & Configuração no Azure

Para que o script funcione, é necessário registrar um aplicativo no **Microsoft Entra ID (Azure AD)** com o seguinte escopo de permissão do tipo **Aplicação**:

- `DeviceManagementManagedDevices.ReadWrite.All`

> ⚠️ **Importante:** Certifique-se de que um Administrador Global concedeu o consentimento de administrador (*Admin Consent*) para esta permissão no portal do Azure.

## 🔧 Como Executar o Projeto

1. Instale as dependências necessárias:
   ```bash
   pip install requests msal
   ```

2. Crie uma pasta chamada `maquinas_seriais` no mesmo diretório do script.

3. Insira arquivos vazios dentro desta pasta, onde o **nome do arquivo** deve ser exatamente o número de série do dispositivo (ex: `ABC123XYZ.txt`).

4. Insira suas credenciais do Azure (`CLIENT_ID`, `CLIENT_SECRET` e `TENANT_ID`) nas variáveis correspondentes dentro do código.

5. Execute o script:
   ```bash
   python remover_dispositivos.py
   ```
