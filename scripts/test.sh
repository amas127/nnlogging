#!/bin/env sh
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "${PROJECT_DIR}/.venv/bin/activate" ]]
then
    source "${PROJECT_DIR}/.venv/bin/activate"
fi
PYTHON_VER=$(python -c "import sys;ver=sys.version_info;print(f'{ver.major}-{ver.minor}')")
mkdir -p "${PROJECT_DIR}/reports"
pytest \
    "${PROJECT_DIR}/tests" \
    --html="${PROJECT_DIR}/reports/test-report-${PYTHON_VER}.html" --self-contained-html \
    --cov="${PROJECT_DIR}/src" \
    --cov-report="html" \
    --cov-report="term-missing" \
    > "${PROJECT_DIR}/reports/test-${PYTHON_VER}.log"
