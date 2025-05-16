# 🧠 Context Core

**Context Core** is the engine behind structured, persistent context management for AI workflows.  

It powers a command-line utility, a future web interface, and a custom GPT assistant—so you can keep AI grounded in what matters across conversations.

> Think of it as long-term memory for your AI tools—clear, modular, and under your control.

Designed for anyone who needs to manage project context over time in AI-driven workflows.

---

## 🎯 Why It Exists

Modern AI models are powerful—but fragile. They forget fast, require repetition, and lose track of goals.  
**Context Core** helps you keep your place in long-running projects by giving you tools to:

- Structure reusable context (facts, goals, decisions, etc.)
- Summarize and evolve project knowledge over time
- Load the right context when you need it—in a GPT chat, CLI, or agent

Whether you're debugging code, planning product strategy, or writing a book—this framework makes context portable, inspectable, and adaptable.

---
## ✨ How It Works

The system is project-based and supports both technical and non-technical workflows.  
At its heart is a simple folder structure with structured files (Markdown or JSON), organized by context type:

```bash
/context/
├── facts/
├── goals/
├── decisions/
├── instructions/
├── actions/
├── summaries/
├── archives/
├── personas/
├── timeline/
└── meta.json
```

These files are loaded and interpreted by:

✅ A custom GPT assistant (primary interface)

💻 A CLI utility (for power users and automation)

🌐 A web UI (coming later)

---
## 🛠 Core Capabilities (MVP)

### 🧩 Context Lifecycle Management
- Create structured context by type (facts, goals, decisions, etc.)

- Summarize sessions into portable context chunks

- Archive outdated or inactive files, and restore them as needed

- Keep active context lean with token-aware workflows

### 🧠 Summarization Framework
- Generate summaries from conversations (AI-assisted or manual)

- Focus on insights, decisions, and future-relevant info

- Maintain cumulative understanding over time

### 💾 Storage
- Flat-file system, local-first by default

- Version-safe organization

- Clear folder structure per project

- Optional tagging and config per project
---

## 🤖 Interfaces
### ✨ GPT Assistant (Primary)
- A custom GPT (e.g., "Context Assistant") loads and works with your active context:

- Use natural language to query, update, summarize, and evolve your project memory

- Works with ChatGPT or Claude via API

- Uses CLI tool as backend to fetch, store, and modify context files

### 🖥️ Command-Line Tool (MVP Engine)
```bash
context init project-name
context create facts system-design
context summarize chat.md
context update project-name summary.md
context load --project project-name --facts --goals
```
The CLI powers GPT tool actions and supports manual control.

### 🌐 Web UI (Planned)
Visual interface for reviewing context, managing projects, and editing content.

---
## 📌 Design Principles

- **GPT-first**: Designed to plug directly into GPTs for natural interaction

- **Simple first**: No databases, just folders and files

- **Token-aware**: Keep AI responses tight and useful

- **User-controlled**: You decide what stays and what gets archived

- **Model-agnostic**: Works with any LLM—ChatGPT, Claude, or your own agent

---
## ⏳ Roadmap
 - CLI MVP (Context creation, summarization, loading, archive)

 - GPT Assistant Integration

 - Web UI (project and context explorer)

 - Summary compression & tagging

 - Context relevance scoring

 - Multi-project context and search

---

## ⚠️ Work in Progress

This project is currently under active development. Much of the functionality is not yet implemented.

![Tests](https://github.com/alatruwe/context-core/actions/workflows/test.yml/badge.svg)

### Next Up:
- [ ] **Context Lifecycle Management** (Creation, Enrichment, Pruning)
- [ ] **Summarization Framework** (Session, Cumulative, Decision Summaries)
- [ ] **Local-first Storage** (File System-based with Versioning)
- [ ] **Model-Agnostic Design** (Interface abstraction for multiple AI models)
- [ ] **Conversation Archiving** (Separate storage for full conversations)
- [ ] **Session list / history page**
- [ ] **Authentication (optional)**
