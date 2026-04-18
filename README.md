# langgraph-trading-agent
AI trading agent with LangGraph, Ollama, Bybit API and Telegram notifications 
# 🤖 LangGraph Trading Agent

AI-агент для криптотрейдинга: получает цену BTC через Bybit, анализирует через локальные LLM (Ollama), выдаёт сигналы и отправляет в Telegram.

## 🚀 Стек
- LangGraph — оркестрация агентов
- Ollama (Mistral, LLama, DeepSeek) — локальные LLM
- Bybit API — рыночные данные
- Telegram API — уведомления
- Docker + PostgreSQL — память и логи

## 📦 Установка и запуск
1. Клонируй репозиторий
2. Установи зависимости: `pip install -r requirements.txt`
3. Запусти агента: `python main.py`

## 🔮 Планы
- Multi-agent система (sbornik + dipkvant)
- RAG с Qdrant
- Поддержка ETH, SOL, акций
