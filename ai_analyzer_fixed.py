import requests

def analyze_with_dipkvant(symbol, price):
    try:
        url = "http://localhost:11434/api/chat"
        prompt = f"{symbol} price is {price} USD. Answer ONLY ONE WORD: BUY, SELL, or HOLD. No other text."
        
        payload = {
            "model": "mistral",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"num_predict": 5, "temperature": 0.1}
        }
        
        print("[ai_analyzer] Жду ответ...")
        response = requests.post(url, json=payload, timeout=60)
        data = response.json()
        answer = data.get("message", {}).get("content", "").strip().upper()
        
        print(f"[ai_analyzer] Ответ модели: {answer}")
        
        # Ищем BUY или SELL в ответе
        if "BUY" in answer:
            return "BUY", 75.0
        elif "SELL" in answer:
            return "SELL", 75.0
        else:
            return "HOLD", 50.0
        
    except Exception as e:
        print(f"[ai_analyzer] Ошибка: {e}")
        return "HOLD", 50.0