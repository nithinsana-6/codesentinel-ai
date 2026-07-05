# Building CodeSentinel AI

AI coding agents are most useful when they can reason over repository context, use tools safely, and produce review output that developers can trust. CodeSentinel AI was built to demonstrate those ideas in a small, inspectable system.

## Problem

Many AI code-review demos are thin wrappers around an LLM API. They can look impressive, but they are hard to test, hard to reproduce, and hard to trust in CI.

CodeSentinel AI takes a different path:

1. Build deterministic tools first.
2. Ground every finding in file and line evidence.
3. Add evaluation cases before adding LLM synthesis.
4. Keep the CLI, Streamlit UI, and core review engine separated.

## Approach

The system starts with a repository scanner that selects reviewable files. The static analyzer checks for high-signal risks such as hardcoded secrets, unsafe shell execution, debug mode, broad exception handling, unresolved engineering notes, and missing tests.

The review agent coordinates the tools and produces a structured report. The renderer turns that report into Markdown or JSON. The Streamlit app uses the same core engine, so the demo and CLI stay aligned.

## Why Deterministic First

LLMs are powerful, but their output can vary. A deterministic baseline gives the project a reliable floor:

- tests are stable
- CI can enforce behavior
- evals can be repeated
- future LLM providers can be compared against a baseline

That is why the default provider does not require an API key. An OpenAI provider can be added later for review synthesis while keeping the core analysis and evaluation loop intact.

## What This Demonstrates

- Agent-style orchestration over tools
- Grounded findings with evidence
- Security and reliability review logic
- Evaluation-driven AI engineering
- CLI and web demo delivery
- CI/CD and Docker packaging

## Future Work

The next strongest additions are SARIF output, pull-request diff parsing, and an optional OpenAI provider that summarizes deterministic findings into a natural-language review while preserving file and line evidence.
