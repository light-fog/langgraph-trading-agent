from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
import asyncio
from bybit_client import BybitClient
from ai_analyzer_fixed import analyze_with_dipkvant
from db_saver import save_signal
from telegram_bot import TelegramBot  # ← исправлено

# Твои данные для Telegram (замени на свои)
TOKEN = "8674257786:AAGQYGMc8xgCRDSX3NlHOcwyObS4WgRHwAM"
CHAT_ID = "5694922177"

class AgentState(TypedDict):
    symbol: str
    price: float
    signal: str
    confidence: float
    messages: List
    step_count: int

def fetch_price_node(state: AgentState) -> AgentState:
    symbol = state.get("symbol", "BTCUSDT")
    client = BybitClient()
    ticker = client.get_ticker(symbol)
    price = ticker["last"]
    print(f"[fetch_price] {symbol} = {price}")
    return {
        **state,
        "price": price,
        "step_count": state.get("step_count", 0) + 1
    }

def analyze_node(state: AgentState) -> AgentState:
    price = state["price"]
    symbol = state.get("symbol", "BTCUSDT")
    signal, confidence = analyze_with_dipkvant(symbol, price)
    print(f"[analyze] Сигнал: {signal}, Уверенность: {confidence}%")
    return {
        **state,
        "signal": signal,
        "confidence": confidence,
        "messages": state.get("messages", []) + [
            AIMessage(content=f"Анализ {symbol}: {signal} ({confidence}%)")
        ]
    }

def save_node(state: AgentState) -> AgentState:
    save_signal(
        symbol=state["symbol"],
        price=state["price"],
        signal=state["signal"],
        confidence=state["confidence"]
    )
    print("[save] Сигнал сохранён в БД")
    return state

def notify_node(state: AgentState) -> AgentState:
    message = f"📊 {state['symbol']}: {state['signal']}\n💰 Цена: {state['price']}\n🎯 Уверенность: {state['confidence']}%"
    bot = TelegramBot(TOKEN, CHAT_ID)  # ← исправлено
    bot.send(message)                   # ← исправлено
    print("[notify] Отправлено в Telegram")
    return state

def should_notify(state: AgentState) -> str:
    signal = state["signal"]
    if state.get("step_count", 0) > 10:
        print("[router] Превышен лимит шагов, завершаем")
        return END
    if signal in ["BUY", "SELL"]:
        return "notify"
    return END

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("fetch_price", fetch_price_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("save", save_node)
    workflow.add_node("notify", notify_node)
    workflow.set_entry_point("fetch_price")
    workflow.add_edge("fetch_price", "analyze")
    workflow.add_edge("analyze", "save")
    workflow.add_conditional_edges("save", should_notify, {"notify": "notify", END: END})
    workflow.add_edge("notify", END)
    return workflow.compile()

async def main():
    graph = build_graph()
    initial_state = {
        "symbol": "BTCUSDT",
        "price": 0.0,
        "signal": "",
        "confidence": 0.0,
        "messages": [],
        "step_count": 0
    }
    result = graph.invoke(initial_state)
    print("\n=== РЕЗУЛЬТАТ ===")
    print(f"Символ: {result['symbol']}")
    print(f"Цена: {result['price']}")
    print(f"Сигнал: {result['signal']}")
    print(f"Уверенность: {result['confidence']}%")

if __name__ == "__main__":
    asyncio.run(main())