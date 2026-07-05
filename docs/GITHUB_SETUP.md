# GitHub Setup Checklist

Use these steps when you are ready to publish CodeSentinel AI.

## 1. Create Repository

Recommended repository name:

```text
codesentinel-ai
```

Recommended GitHub description:

```text
Agentic code-review and evaluation workbench with deterministic evals, grounded findings, CI, and Docker.
```

Topics:

```text
ai-agents, llm-evals, code-review, devtools, python, ci-cd, agentic-ai
```

## 2. Push Project

From inside the `codesentinel-ai` folder:

```bash
git init
git add .
git commit -m "Initial CodeSentinel AI portfolio project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/codesentinel-ai.git
git push -u origin main
```

## 3. Pin On GitHub Profile

Pin this repo and use this description:

```text
Production-style AI code-review workbench with repository scanning, grounded findings, deterministic evals, CI, and Docker.
```

## 4. Add To Resume

Recommended project entry:

```text
CodeSentinel AI - Agentic Code Review and Evaluation Workbench
- Built a production-style AI code-review system that scans repositories, detects security/reliability risks, and generates grounded review reports with file and line evidence.
- Added deterministic evaluation cases with precision/recall reporting, CI automation, Docker packaging, and a release-gate mode for critical findings.
```

## 5. Demo Commands

```bash
python -m unittest discover -s tests
python -m codesentinel.cli review examples/sample_repo --format markdown
python -m codesentinel.cli eval evals/cases.jsonl
```

## 6. Best Next Enhancements

Do these after the first GitHub push:

1. Deploy the Streamlit demo using `docs/DEPLOY_STREAMLIT.md`.
2. Add SARIF output so findings appear in GitHub code scanning.
3. Add pull-request diff parsing.
4. Add OpenAI provider adapter for natural-language review synthesis.
5. Add a benchmark report comparing deterministic checks vs. LLM-assisted review.
