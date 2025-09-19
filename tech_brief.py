import os
import sys
import requests
from openai import OpenAI

# variáveis obrigatórias
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TG_BOT_TOKEN   = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID     = os.getenv("TG_CHAT_ID")

# mensagem pode vir por env ou argumento
MESSAGE = os.getenv("MESSAGE")
if not MESSAGE and len(sys.argv) > 1:
    MESSAGE = " ".join(sys.argv[1:])

if not OPENAI_API_KEY:
    raise RuntimeError("Faltando OPENAI_API_KEY")
if not TG_BOT_TOKEN:
    raise RuntimeError("Faltando TG_BOT_TOKEN")
if not TG_CHAT_ID:
    raise RuntimeError("Faltando TG_CHAT_ID")
if not MESSAGE:
    raise RuntimeError("Faltando MESSAGE (env ou argumento)")

def ask_openai(prompt: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.responses.create(
        model="gpt-5",
        tools=[{"type": "web_search"}],
        input=prompt
    )
    return resp.output_text.strip()

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    r = requests.post(
        url,
        json={"chat_id": TG_CHAT_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True},
        timeout=30,
    )
    r.raise_for_status()
    r = requests.post(url, json=payload, timeout=20)
    if r.status_code != 200:
        print("Telegram error:", r.status_code, r.text)  # mostra o motivo
        r.raise_for_status()

def main():
    print(f"▶️ Prompt: {MESSAGE[:80]}...")  # debug
    resposta = ask_openai(MESSAGE)
    send_telegram(resposta)
    print("✅ enviado pro Telegram")

if __name__ == "__main__":
    main()
