import telebot
import os
import random
from openai import OpenAI

# Tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# Pocket Option PAIRS
PAIRS = {
    "EURUSD": "EUR/USD OTC",
    "GBPUSD": "GBP/USD OTC",
    "USDJPY": "USD/JPY OTC",
    "AUDUSD": "AUD/USD OTC",
    "EURJPY": "EUR/JPY OTC",
    "GBPJPY": "GBP/JPY OTC",
    "BTCUSD": "BTC/USD OTC",
    "ETHUSD": "ETH/USD OTC"
}

SIGNALS = ["BUY", "SELL", "WAIT"]
TIMEFRAMES = ["M1", "M5", "M15"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🤖 Pocket Option AI Bot\n\n"
        "Ulanyş:\n"
        "/signal\n"
        "/signal M5\n"
        "/signal EURUSD\n"
        "/signal EURUSD M5"
    )

@bot.message_handler(commands=['signal'])
def signal(message):
    parts = message.text.upper().split()

    pair_key = None
    tf = "M1"

    for p in parts[1:]:
        if p in PAIRS:
            pair_key = p
        if p in TIMEFRAMES:
            tf = p

    if pair_key:
        pair = PAIRS[pair_key]
    else:
        pair = random.choice(list(PAIRS.values()))

    sig = random.choice(SIGNALS)

    prompt = f"""
You are a trading assistant.
Give a short analysis for Pocket Option OTC market.

PAIR: {pair}
TIMEFRAME: {tf}
SIGNAL: {sig}

Write 2-3 short sentences.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    analysis = response.choices[0].message.content

    text = f"""
📊 PAIR: {pair}
⏱ TF: {tf}
📌 SIGNAL: {sig}

🧠 AI ANALIZ:
{analysis}

⚠️ Demo / Education maksatly
"""
    bot.send_message(message.chat.id, text)

print("✅ Bot işläp başlady")
bot.polling(none_stop=True)
