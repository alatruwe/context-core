# 🧠 Context Core

Context Core is a library for maintaining persistent, structured context management across multiple AI workflows. 

It enables users to define, manage, and evolve project context over time, allowing AI systems to maintain continuity and relevance throughout multiple interactions.

Designed for anyone who needs to manage project context over time in AI-driven workflows.

---
## 📁 Core Functionality
The library is designed to handle several essential features for managing context over time:

### 🧩 Context Lifecycle Management
Create and store context in a structured format (Markdown or JSON)

Enrich context by adding key points, summaries, and decisions from ongoing conversations

Prune and refine context as projects evolve

Archive context that is no longer in active use for later reference

### 🧠 Summarization Framework
Generate summaries of individual sessions, aggregating knowledge over time

Focus on decisions, insights, and action items relevant for future sessions

Maintain version history for summaries and context changes

### 💾 Storage
Context files stored locally by default (with optional cloud synchronization)

Version tracking for context evolution, with easy rollback capabilities

User-controlled storage location, with clear guidelines for file organization

---

## ⚠️ Work in Progress

This project is currently under active development. Much of the functionality is not yet implemented.

### Next Up:
- [ ] **Context Lifecycle Management** (Creation, Enrichment, Pruning)
- [ ] **Summarization Framework** (Session, Cumulative, Decision Summaries)
- [ ] **Local-first Storage** (File System-based with Versioning)
- [ ] **Model-Agnostic Design** (Interface abstraction for multiple AI models)
- [ ] **Conversation Archiving** (Separate storage for full conversations)
- [ ] **Session list / history page**
- [ ] **Authentication (optional)**

---
## 🧩 Related Projects
[AI Context](https://github.com/alatruwe/ai-context): A web-based chat tool for maintaining project context in AI conversations.
