
---

# 2. `docs/architecture.md`

```markdown
# Customer Support AI Agent - Architecture

## 1. Project Overview

The Customer Support AI Agent is an AI-powered customer support system
that uses customer-specific memory to provide more contextual and
personalized support responses.

The system combines:

- Web-based chat interface
- Flask backend
- Hindsight memory
- Groq-powered LLM
- Customer-specific data
- Persistent conversation context
- REST API integration

---

# 2. Main Goal

The main goal is to build a customer support agent that can remember
useful customer-specific information and use that information in
future interactions.

Instead of treating every customer message as completely independent,
the system retrieves relevant customer context before generating a
response.

The overall concept is:

```text
Customer Interaction
        ↓
Useful Information
        ↓
Memory
        ↓
Future Interaction
        ↓
Memory Retrieval
        ↓
Context-Aware AI Response
