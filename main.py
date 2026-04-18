import time
from bybit_client import BybitClient
from ai_analyzer import AIAnalyzer

BOT_TOKEN = "8674281527:AAGQYGMc8xgCRDSX3NlHOcwyObS4WgRHwAM"
CHAT_ID = "1404135606"

client = BybitClient()
ai = AIAnalyzer()

print("🚀 Агент запущен. Анализ BTC/USDT...")
print("=" * 50)

for i in range(3):
    print(f"\n📊 Цикл {i+1}/3")
    
    ticker = client.get_ticker("BTCUSDT")
    
    if ticker:
        price = ticker['last']
        print(f"💰 Цена BTC: ${price:,.2f}")
        
        signal = ai.analyze_simple("BTC", price, 50, 100)
        print(f"🤖 Сигнал ИИ: {signal}")
        
        from telegram_bot import TelegramBot
        bot = TelegramBot(BOT_TOKEN, CHAT_ID)
        bot.send(f"🚀 Агент запущен\nBTC: ${price:,.2f}\nСигнал: {signal}")
    else:
        print("❌ Нет данных")
    
    if i < 2:
        time.sleep(10)

print("\n✅ Готово")