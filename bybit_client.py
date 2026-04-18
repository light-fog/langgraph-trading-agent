import requests

class BybitClient:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def get_ticker(self, symbol="BTCUSDT"):
        try:
            symbol_clean = symbol.replace("+", "").replace("/", "")
            
            # Пробуем категорию spot для всех, т.к. tradfi может не работать
            category = "spot"
                
            url = f"{self.base_url}/v5/market/tickers"
            params = {"category": category, "symbol": symbol_clean}
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("retCode") == 0 and data["result"]["list"]:
                ticker = data["result"]["list"][0]
                return {
                    "symbol": symbol,
                    "last": float(ticker["lastPrice"]),
                    "high": float(ticker.get("highPrice24h", 0)),
                    "low": float(ticker.get("lowPrice24h", 0)),
                    "volume": float(ticker.get("volume24h", 0))
                }
            else:
                print(f"[BybitClient] Ошибка API для {symbol}: {data.get('retMsg', 'Нет данных')}")
                return {"symbol": symbol, "last": 0.0, "high": 0.0, "low": 0.0, "volume": 0.0}
        except Exception as e:
            print(f"[BybitClient] Сетевая ошибка для {symbol}: {e}")
            return {"symbol": symbol, "last": 0.0, "high": 0.0, "low": 0.0, "volume": 0.0}