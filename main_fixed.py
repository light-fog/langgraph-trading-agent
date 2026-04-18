import time
from bybit_client import BybitClient
from ai_analyzer_fixed import AIAnalyzer
from db_saver import save_signal
save_signal("TEST", 100, "HOLD", 50)
print("🚀 Агент запущен. Анализ BTC/USDT...")

client = BybitClient()
ai = AIAnalyzer()

for i in range(3):
    print(f"\n📊 Цикл {i+1}/3")
    ticker = client.get_ticker("BTCUSDT")
    if ticker:
        price = ticker['last']
        print(f"💰 Цена BTC: ${price:,.2f}")
        signal = ai.analyze_simple("BTC", price, 50, 100)
        print(f"🤖 Сигнал ИИ: {signal}")
    else:
        print("❌ Нет данных от Bybit")
    time.sleep(10)

print("✅ Готово")