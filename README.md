# Traffic Law → VLM Checklist Pipeline

Parses traffic statutes from government websites (Quebec, Ontario) and translates them into atomic, verifiable JSON checklists for Vision-Language Models.

## Quick Start

### Option A: One-command setup

```bash
python setup.py
```

This creates the venv, installs all dependencies, and downloads the Playwright browser.

### Option B: Manual setup

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browser (needed for Ontario's JS-rendered site)

```bash
python -m playwright install chromium
```

### 4. Set your LLM API key

```bash
# OpenAI
set OPENAI_API_KEY=sk-...          # Windows
export OPENAI_API_KEY=sk-...       # macOS / Linux

# Anthropic
set ANTHROPIC_API_KEY=sk-ant-...   # Windows
export ANTHROPIC_API_KEY=sk-ant-...# macOS / Linux

# Or use a local model via Ollama (no key needed)
```

### 5. Add your prompt

Paste your VLM translation prompt into `config/prompt.txt`. This is the system-level instruction that tells the LLM how to convert law text into JSON.

### 6. Run the pipeline

```bash
# Scrape + translate Quebec laws
python run_pipeline.py --site quebec --model gpt-4o

# Scrape + translate Ontario laws
python run_pipeline.py --site ontario --model claude-3-5-sonnet-20240620

# Use a local model
python run_pipeline.py --site quebec --model ollama/llama3

# Scrape only (no LLM)
python run_pipeline.py --site quebec --scrape-only

# Resume an interrupted run
python run_pipeline.py --site quebec --model gpt-4o --resume
```

## Project Structure

```
traffic_law_pipeline/
├── adapters/           # Site-specific scrapers
│   ├── base.py         # Law dataclass + BaseSiteAdapter interface
│   ├── quebec.py       # legisquebec.gouv.qc.ca (server-rendered)
│   └── ontario.py      # ontario.ca/laws (JS SPA, Playwright)
├── pipeline/           # Core pipeline stages
│   ├── scraper.py      # Orchestrates adapters
│   ├── translator.py   # Sends laws to LLM via Open Interpreter
│   └── writer.py       # NDJSON output + checkpointing
├── schemas/
│   └── law_translation.json  # JSON Schema for output validation
├── config/
│   ├── prompt.txt      # Your VLM translation prompt
│   └── sites.yaml      # Site configurations
├── output/             # Generated at runtime
├── run_pipeline.py     # CLI entry point
├── requirements.txt
└── README.md
```

## How It Works

1. **Scrape** — Site-specific adapters fetch and parse law sections into `Law` objects
2. **Translate** — Each law is sent to an LLM (via [Open Interpreter](https://github.com/openinterpreter/open-interpreter) + [LiteLLM](https://docs.litellm.ai/docs/providers/)) with your prompt
3. **Persist** — Results are written as NDJSON with checkpointing for resumability

## Supported Sites

| Site | Adapter | Rendering | Notes |
|------|---------|-----------|-------|
| Quebec Highway Safety Code | `quebec.py` | Server-rendered | `requests` + `BeautifulSoup` |
| Ontario Highway Traffic Act | `ontario.py` | JavaScript SPA | `Playwright` + `BeautifulSoup` |

## Requirements

- Python ≥ 3.9
- An LLM API key (OpenAI, Anthropic, etc.) or a local model via Ollama
