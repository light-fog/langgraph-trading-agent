from sqlalchemy import create_engine, text

def save_signal(symbol, price, signal, confidence):
    try:
        engine = create_engine('postgresql://postgres:12345@localhost:5432/agent_db')
        with engine.connect() as conn:
            query = text("""
                INSERT INTO signals (symbol, price, signal, confidence)
                VALUES (:symbol, :price, :signal, :confidence)
            """)
            conn.execute(query, {
                "symbol": symbol,
                "price": price,
                "signal": signal,
                "confidence": confidence
            })
            conn.commit()
        print("[db_saver] Сигнал сохранён в БД")
        return True
    except Exception as e:
        print(f"[db_saver] Ошибка: {e}")
        return False