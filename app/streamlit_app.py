from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from codesentinel.agent import ReviewAgent
from codesentinel.renderer import render_markdown


SAMPLE_CODE = '''import subprocess

API_KEY = "super-secret-token-123"


def run_backup(path):
    # TODO: validate user input before shelling out
    subprocess.run(f"tar -czf backup.tgz {path}", shell=True)


def handler(event):
    try:
        run_backup(event["path"])
    except Exception:
        return {"ok": False}
    return {"ok": True}


debug = True
'''


def run_review(code: str, filename: str):
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        target = repo / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(code, encoding="utf-8")
        return ReviewAgent().review(repo)


def severity_color(severity: str) -> str:
    return {
        "critical": "#b42318",
        "high": "#c2410c",
        "medium": "#b7791f",
        "low": "#2f855a",
    }.get(severity, "#4a5568")


st.set_page_config(
    page_title="CodeSentinel AI",
    page_icon="CS",
    layout="wide",
)

st.title("CodeSentinel AI")
st.caption("Agentic code-review and evaluation workbench for AI-assisted software delivery.")

with st.sidebar:
    st.header("Demo Controls")
    filename = st.text_input("Filename", value="app.py")
    run_button = st.button("Run Review", type="primary", use_container_width=True)
    st.divider()
    st.markdown(
        "This demo runs deterministic offline analysis. No API key is required, "
        "which keeps the review reproducible for recruiters and CI."
    )

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.subheader("Input Code")
    code = st.text_area(
        "Paste Python, JavaScript, TypeScript, Go, Java, YAML, JSON, TOML, or Markdown.",
        value=SAMPLE_CODE,
        height=520,
        label_visibility="collapsed",
    )

if run_button or "last_report" not in st.session_state:
    st.session_state.last_report = run_review(code, filename)

report = st.session_state.last_report
severity_counts = report.severity_counts()
category_counts = report.category_counts()

with right:
    st.subheader("Review Summary")
    st.write(report.summary)

    metric_cols = st.columns(4)
    for column, severity in zip(metric_cols, ["critical", "high", "medium", "low"]):
        column.metric(severity.title(), severity_counts[severity])

    st.subheader("Category Coverage")
    st.bar_chart(category_counts)

st.subheader("Findings")

if not report.findings:
    st.success("No findings detected.")
else:
    for finding in report.findings:
        location = finding.file_path
        if finding.line_number is not None:
            location = f"{location}:{finding.line_number}"
        with st.expander(f"{finding.severity.value.upper()} - {finding.title} - {location}", expanded=True):
            st.markdown(
                f"<span style='color:{severity_color(finding.severity.value)}; font-weight:700'>"
                f"{finding.category.value.title()} / {finding.severity.value.title()}</span>",
                unsafe_allow_html=True,
            )
            st.write(finding.description)
            st.info(finding.recommendation)
            if finding.evidence:
                st.code(finding.evidence, language="python")

with st.expander("Markdown Report"):
    st.code(render_markdown(report), language="markdown")
