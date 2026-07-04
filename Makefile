.PHONY: test review eval

test:
	python -m unittest discover -s tests

review:
	python -m codesentinel.cli review examples/sample_repo --format markdown

eval:
	python -m codesentinel.cli eval evals/cases.jsonl
