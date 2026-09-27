# Customer Support AI Agent - Architecture

## 1. Project Goal

The Customer Support AI Agent is an AI-powered customer support system
that remembers customer-specific information across conversations.

The system retrieves relevant customer memories before generating a response.
This allows the AI agent to provide more personalized and context-aware
customer support.

---

## 2. High-Level Architecture

```text
Customer
   |
   v
Frontend Chat UI
   |
   | POST /api/chat
   v
Backend / API
   |
   +--------------------+
   |                    |
   v                    v
Memory Service      AI Agent
   |                    |
   v                    v
Hindsight Cloud       Groq / LLM
   |                    |
   +---------+----------+
             |
             v
       Final Response
             |
             v
          Frontend
