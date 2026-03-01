# Agente de Compras – Bot Telegram

Este é um **bot de Telegram** que funciona como assistente de compras. Ele permite:

- Adicionar produtos à lista de compras  
- Remover produtos da lista  
- Ver a lista atual  
- Limpar toda a lista  

O bot usa **Long Polling** para receber mensagens do Telegram e **Firestore** como banco de dados.

---

## 📦 Estrutura do Projeto


Estudos_Agente_IA/
├── Dockerfile
├── main.py
├── requirements.txt
├── seu-arquivo-firestore.json
└── README.md


---

## ⚙️ Tecnologias

- Python 3.11  
- pyTelegramBotAPI  
- Google Cloud Firestore  
- Docker  
- Render (Hospedagem gratuita de Web Service)

---

## 📝 Requisitos

1. Ter uma conta no [Telegram](https://telegram.org/) e criar um bot via BotFather  
2. Ter uma conta no [Google Cloud](https://cloud.google.com/) e criar um **Firestore**  
3. Ter o arquivo JSON de credenciais do Firestore  

---

## 🔧 Configuração

### 1. Variáveis de ambiente

No Render (ou localmente) defina:

| Nome                             | Valor                                      |
|---------------------------------|-------------------------------------------|
| TELEGRAM_TOKEN                   | Token do Bot do Telegram                  |
| OPENAI_KEY                       | Chave da OpenAI GPT                        |
| GOOGLE_APPLICATION_CREDENTIALS   | Nome do arquivo JSON do Firestore          |

---

### 2. Instalação local (opcional)

```git clone https://github.com/SeuUsuario/Agente_ia_compras.git

cd Agente_ia_compras
pip install -r requirements.txt
python main.py 
```

Certifique-se de colocar o JSON do Firestore na mesma pasta e definir as variáveis de ambiente.

3. Docker (opcional)
docker build -t agente-compras .
docker run -e TELEGRAM_TOKEN="seu_token" -e OPENAI_KEY="sua_chave" -e GOOGLE_APPLICATION_CREDENTIALS="arquivo.json" agente-compras
🚀 Deploy no Render

Crie um Web Service no Render

Conecte ao repositório GitHub

Configure:

Runtime: Docker

Branch: main

Dockerfile Path: ./Dockerfile

Defina as variáveis de ambiente

Clique em Manual Deploy → Deploy Latest Commit

Acompanhe os logs → bot deve iniciar via Long Polling

💬 Uso no Telegram

compra açúcar → adiciona açúcar à lista

tira óleo → remove óleo da lista

/lista → mostra todos os itens da lista

/limpar → limpa toda a lista

⚠️ Observações

O bot funciona via Long Polling, então não precisa de webhook.

Free tier do Render pode hibernar se ficar sem uso por muito tempo.

Firestore deve estar configurado com permissões corretas para leitura e escrita.

Feito com ❤️ por Deivin
