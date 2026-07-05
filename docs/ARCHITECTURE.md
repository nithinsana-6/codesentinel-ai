# CodeSentinel AI Architecture

CodeSentinel AI is designed as a small, production-style agentic system. The core idea is to keep the agent orchestration separate from the tools it uses, so every step can be tested, measured, and replaced independently.

## System Flow

```text
Repository or pasted code
        |
        v
RepositoryScanner
        |
        v
SourceFile objects
        |
        v
StaticAnalyzer
        |
        v
Finding objects
        |
        v
ReviewAgent + Provider
        |
        v
ReviewReport
        |
        v
Markdown / JSON / Streamlit UI
```

## Components

### RepositoryScanner

`src/codesentinel/scanner.py`

Discovers reviewable files while excluding noise such as `.git`, virtual environments, build output, caches, and oversized files. The scanner converts raw files into structured `SourceFile` objects so downstream tools do not need to know about filesystem traversal.

### StaticAnalyzer

`src/codesentinel/analyzer.py`

Runs deterministic checks for security, reliability, maintainability, and testing risks. Every finding includes category, severity, file path, optional line number, evidence, and remediation guidance.

### ReviewAgent

`src/codesentinel/agent.py`

Coordinates scanner, analyzer, provider, and report construction. The agent acts as the orchestration layer rather than hiding all logic inside one prompt or one function.

### Provider Layer

`src/codesentinel/providers.py`

The default provider is deterministic so demos, tests, and CI are reproducible. Hosted LLM providers can be added later without changing scanner, analyzer, evaluator, or renderer behavior.

### Evaluator

`src/codesentinel/evaluator.py`

Runs labeled JSONL test cases and reports precision/recall. This gives the project an evaluation loop before adding any LLM-based review synthesis.

### Streamlit Demo

`app/streamlit_app.py`

Provides a recruiter-friendly interface where users can paste code, run a deterministic review, inspect severity/category metrics, and read grounded findings.

## Design Decisions

- Deterministic core first, optional LLM provider later.
- Findings are grounded in file and line evidence.
- CLI-first workflow for CI and automation.
- Streamlit demo for easy inspection.
- Evaluation cases live in version control.
- No mandatory external API key for the base project.

## Extension Points

- OpenAI provider for natural-language review synthesis.
- SARIF output for GitHub code scanning.
- Pull-request diff parsing.
- Patch-generation mode with human approval.
- More labeled eval cases for false-positive/false-negative tracking.
