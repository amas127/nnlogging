#!/bin/env bash
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
"${PROJECT_DIR}/.venv/bin/pytest" \
    "${PROJECT_DIR}/tests/v0.2.0/" \
    --cov="${PROJECT_DIR}/src" \
    --cov-report="term-missing" \
    --cov-branch \
    --cov-fail-under=75
