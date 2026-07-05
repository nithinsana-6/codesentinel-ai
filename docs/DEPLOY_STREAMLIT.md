# Deploy CodeSentinel AI To Streamlit Community Cloud

Use this guide to create a live demo recruiters can click.

## 1. Open Streamlit Community Cloud

Go to:

```text
https://share.streamlit.io/
```

Sign in with GitHub.

You can also try the direct deploy link:

```text
https://share.streamlit.io/deploy?repository=https://github.com/nithinsana-6/codesentinel-ai&branch=main&mainModule=streamlit_app.py
```

## 2. Create New App

Choose:

- Repository: `nithinsana-6/codesentinel-ai`
- Branch: `main`
- Main file path: `streamlit_app.py`

Advanced settings:

- Python version: `3.12` if available

## 3. Requirements File

Streamlit should automatically detect:

```text
requirements.txt
```

If Streamlit asks for a requirements file path, use:

```text
requirements.txt
```

## 4. What The Demo Shows

The app lets reviewers paste code and run a deterministic CodeSentinel review. It displays:

- review summary
- severity counts
- category coverage
- grounded findings with file and line evidence
- Markdown report output

## 5. Add The Live URL To GitHub

After deployment, edit the GitHub repository details and add the Streamlit app URL as the Website link.

Also add it near the top of `README.md`:

```markdown
Live demo: https://YOUR-APP.streamlit.app
```

## 6. LinkedIn Line

```text
Live demo: CodeSentinel AI, an agentic code-review and evaluation workbench for AI-assisted software delivery.
```
