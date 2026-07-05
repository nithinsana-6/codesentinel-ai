# CodeSentinel AI

Agentic code-review and evaluation workbench for AI-assisted software delivery.

CodeSentinel AI is a production-style portfolio project that demonstrates how to build a reliable coding agent around real software-engineering constraints: repository scanning, tool-based reasoning, risk classification, deterministic evaluation, CI checks, and human-readable review output.

It is designed to be useful even without an LLM API key. The default reviewer uses deterministic heuristics so tests and demos are reproducible. Optional provider adapters can be added for OpenAI, Anthropic, or local models.

## Why This Project Matters

Modern AI engineering is not only prompt engineering. Strong AI products need:

- reliable tool boundaries
- testable agent behavior
- measurable evaluation loops
- safe handling of repository content
- explainable findings
- CI/CD integration
- clear failure modes

This project shows those skills in one focused system.

## Features

- Repository scanner with configurable include/exclude rules
- Static risk analyzer for security, reliability, and maintainability issues
- Agent-style review orchestration with tool outputs and evidence
- Deterministic review reports in Markdown and JSON
- Evaluation harness for measuring reviewer quality against labeled cases
- Streamlit demo app for recruiter-friendly review walkthroughs
- CLI-first workflow suitable for GitHub Actions
- FastAPI-ready service layer through clean core abstractions
- Unit tests using only the Python standard library
- Dockerfile and CI workflow

## Demo

### Web Demo

The Streamlit app entry point is:

```text
app/streamlit_app.py
```

Deploy instructions are in `docs/DEPLOY_STREAMLIT.md`.

### CLI Demo

Run a review against the included intentionally flawed sample repository:

```bash
python -m codesentinel.cli review examples/sample_repo --format markdown
```

Use release-gate mode in CI:

```bash
python -m codesentinel.cli review . --fail-on-critical
```

Run the evaluation suite:

```bash
python -m codesentinel.cli eval evals/cases.jsonl
```

Expected output includes:

- detected hardcoded secret patterns
- broad exception handling
- unsafe shell execution
- missing tests
- TODO/FIXME debt
- structured scorecard for labeled evaluation cases

For resume bullets, LinkedIn copy, and interview talking points, see `docs/PORTFOLIO.md`.

For deeper technical proof, see:

- `docs/ARCHITECTURE.md`
- `docs/EVAL_REPORT.md`
- `docs/TECHNICAL_WRITEUP.md`

## Architecture

```text
CLI
 |
 v
ReviewAgent
 |-- RepositoryScanner
 |-- StaticAnalyzer
 |-- ProviderAdapter
 |-- ReportRenderer
 |
 v
Findings + Evaluation Metrics
```

## Repository Structure

```text
codesentinel-ai/
  src/codesentinel/
    agent.py           # review orchestration
    analyzer.py        # static risk checks
    cli.py             # command-line interface
    config.py          # project configuration
    evaluator.py       # labeled-case evaluation harness
    models.py          # typed domain objects
    providers.py       # deterministic and optional LLM adapters
    renderer.py        # markdown/json report rendering
    scanner.py         # repository file discovery
  tests/
  app/streamlit_app.py
  examples/sample_repo/
  evals/cases.jsonl
  .github/workflows/ci.yml
```

## What To Highlight On LinkedIn

Built a production-style AI code-review workbench that combines repository scanning, agentic review orchestration, deterministic evals, and CI automation. The system generates explainable findings for security, reliability, and maintainability risks, then measures reviewer quality against labeled test cases.

## Interview Talking Points

- Why deterministic evals are necessary before adding LLM providers
- How the agent separates scanning tools, analysis tools, and report generation
- How findings are grounded in file paths and line numbers
- How CI can block regressions in agent behavior
- What safety checks matter before allowing an AI coding agent to modify code
- How this could be extended into PR review, patch generation, or IDE feedback

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python -m unittest discover
```

The core project intentionally has no mandatory third-party runtime dependency.

You can also run the tests immediately after cloning because the repository
includes a small `sitecustomize.py` helper for local `src/` imports:

```bash
python -m unittest discover -s tests
```

For convenience, the repo also includes a tiny root-level `codesentinel/`
shim. That lets this command work from the repository root before installation:

```bash
python -m codesentinel.cli review examples/sample_repo --format markdown
```

## Optional API Providers

The default provider is deterministic and offline. To add a hosted LLM provider, implement the `ReviewProvider` protocol in `src/codesentinel/providers.py` and keep all network/API behavior outside the core analyzer.

## License

MIT
