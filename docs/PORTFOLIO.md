# Portfolio Guide

Use this page to turn CodeSentinel AI into resume, LinkedIn, and interview material.

## Resume Bullet

Built CodeSentinel AI, a production-style agentic code-review workbench that scans repositories, detects security and reliability risks, generates grounded review reports, and evaluates reviewer quality against labeled test cases with precision/recall metrics.

## Stronger Resume Bullet For OpenAI / Codex Roles

Built an AI-agent evaluation workbench for code-review workflows, combining repository scanning, deterministic tool-based analysis, CI-ready review reports, and labeled eval cases to measure reliability before adding LLM provider integrations.

## LinkedIn Post

I built CodeSentinel AI, a production-style AI engineering project focused on agentic code review and evaluation.

The goal was not to build another thin LLM wrapper. I wanted to show the engineering pieces that make coding agents reliable:

- repository scanning
- grounded findings with file and line evidence
- security and reliability checks
- deterministic offline reviewer behavior
- labeled evaluation cases
- precision and recall reporting
- CI/CD integration
- Docker-ready packaging

The project currently runs without an API key, which makes demos and tests reproducible. The next extension is adding OpenAI/Anthropic provider adapters while keeping the core evaluation harness deterministic.

This project helped me think more deeply about how AI coding agents should be evaluated before they are trusted in production workflows.

## GitHub Profile Pin Description

Agentic code-review and evaluation workbench with repository scanning, grounded findings, deterministic evals, CI, Docker, and production-style Python architecture.

## Streamlit Demo Description

Interactive demo for CodeSentinel AI. Paste code, run a deterministic review, inspect severity/category metrics, and view grounded findings with file and line evidence.

## Interview Story

I built CodeSentinel AI to demonstrate that AI engineering is more than calling an LLM API. The system treats the agent as an orchestrator over tools: a scanner gathers repository context, an analyzer produces grounded findings, a provider summarizes the risk profile, and an evaluator measures behavior against labeled cases.

The default provider is deterministic, which makes the project testable and reliable in CI. That design choice lets me add hosted LLM providers later without making the core system flaky. I also added a release-gate mode so teams can use the same CLI for local review reports or CI enforcement.

## Future Roadmap

- Add OpenAI provider adapter for natural-language review synthesis
- Parse unified diffs for pull-request-only review
- Add SARIF output for GitHub code scanning
- Add patch-generation mode with human approval
- Add benchmark datasets for false-positive reduction
- Add FastAPI service wrapper for a web dashboard
