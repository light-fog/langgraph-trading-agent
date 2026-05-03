
# 🤖 Multi‑Market AI Trading Agent

**AI agent for market analysis and generating trading signals (BUY/SELL/HOLD).**  
Built with **LangGraph**, runs local LLMs via **Ollama**, stores data in **PostgreSQL**, memory in **Qdrant**, notifications in **Telegram**.

## 🏗️ Architecture

```mermaid
graph TD
    A[fetch_price_node] --> B[analyze_node]
    B --> C[save_node]
    C --> D{should_notify}
    D -->|BUY/SELL| E[notify_node]
    D -->|HOLD| F[END]
    E --> F