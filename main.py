import os
import json
import telebot
from google.cloud import firestore
import openai

# =========================
# CONFIGURAÇÕES
# =========================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
GCP_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

if not TOKEN or not OPENAI_KEY or not GCP_CREDENTIALS:
    raise Exception("Certifique-se de configurar todas as variáveis de ambiente!")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_CREDENTIALS

bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_KEY
db = firestore.Client(database="compras")  # Free tier é suficiente

# =========================
# FUNÇÕES FIRESTORE
# =========================
def pegar_lista(usuario):
    doc_ref = db.collection("listas").document(usuario)
    doc = doc_ref.get()
    return doc.to_dict().get("itens", []) if doc.exists else []

def salvar_lista(usuario, lista):
    db.collection("listas").document(usuario).set({"itens": lista})

def limpar_lista(usuario):
    db.collection("listas").document(usuario).delete()

# =========================
# INTERPRETAÇÃO DE MENSAGENS
# =========================
def interpretar_mensagem(texto):
    prompt = f"""
Você é um assistente de lista de compras. Analise a mensagem do usuário e responda APENAS em JSON:
{{"acao": "adicionar" | "remover" | "ignorar", "item": "nome do produto simplificado"}}
Exemplo:
- "Oi" -> {{"acao": "ignorar", "item": null}}
- "compra arroz" -> {{"acao": "adicionar", "item": "arroz"}}
- "tira feijão" -> {{"acao": "remover", "item": "feijão"}}

Mensagem do usuário: "{texto}"
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception:
        return {"acao": "ignorar", "item": None}

# =========================
# LÓGICA DO BOT
# =========================
@bot.message_handler(func=lambda message: True)
def responder(message):
    usuario = str(message.from_user.id)
    texto_usuario = message.text.strip()

    # Comandos manuais
    if texto_usuario.lower() == "/lista":
        lista = pegar_lista(usuario)
        if not lista:
            bot.reply_to(message, "📋 Sua lista está vazia.")
        else:
            bot.reply_to(message, "📋 Sua lista:\n- " + "\n- ".join(lista))
        return

    if texto_usuario.lower() == "/limpar":
        limpar_lista(usuario)
        bot.reply_to(message, "🗑️ Lista limpa!")
        return

    # Interpretar mensagem via OpenAI
    intencao = interpretar_mensagem(texto_usuario)
    acao = intencao.get("acao")
    item = intencao.get("item")

    if acao == "ignorar" or not item:
        bot.reply_to(message, "👋 Para gerenciar sua lista use: /lista, /limpar ou diga o que quer comprar.")
        return

    lista = pegar_lista(usuario)

    if acao == "adicionar":
        if item.lower() in [i.lower() for i in lista]:
            bot.reply_to(message, f"🔁 '{item}' já está na lista.")
        else:
            lista.append(item)
            salvar_lista(usuario, lista)
            bot.reply_to(message, f"✅ '{item}' adicionado!")

    elif acao == "remover":
        nova_lista = [i for i in lista if i.lower() != item.lower()]
        if len(nova_lista) < len(lista):
            salvar_lista(usuario, nova_lista)
            bot.reply_to(message, f"🗑️ '{item}' removido da lista.")
        else:
            bot.reply_to(message, f"❓ Não achei '{item}' na sua lista.")

# =========================
# INICIAR BOT
# =========================
if __name__ == "__main__":
    bot.infinity_polling()
