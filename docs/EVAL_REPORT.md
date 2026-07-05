# Evaluation Report

CodeSentinel AI includes a lightweight evaluation harness for measuring whether review behavior matches expected findings on labeled cases.

## Current Evaluation Command

```bash
python -m codesentinel.cli eval evals/cases.jsonl
```

## Current Result

```text
Cases: 2
Average precision: 1.00
Average recall: 1.00
```

## Evaluation Cases

| Case | Expected Behavior |
|---|---|
| `secret-and-shell-risk` | Detect hardcoded secret, unsafe shell execution, and missing tests |
| `debug-and-broad-exception` | Detect debug mode, broad exception handling, and missing tests |

## Metrics

Precision measures how many detected findings were expected.

Recall measures how many expected findings were detected.

These metrics matter because AI-assisted code review systems can fail in two different ways:

- False positives: noisy findings that developers ignore.
- False negatives: missed risks that reach production.

## Why The Eval Harness Matters

The project intentionally measures deterministic behavior before adding hosted LLM providers. That makes it possible to compare future LLM-assisted review output against a stable baseline.

## Next Benchmark Additions

- Add benign repositories to measure false positives.
- Add pull-request diff cases.
- Add multi-file data-flow examples.
- Add SARIF comparison output.
- Track result changes across model/provider versions.
