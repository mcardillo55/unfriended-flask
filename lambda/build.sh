#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
ZIP_FILE="${SCRIPT_DIR}/unfriended-lambda.zip"

echo "==> Cleaning previous build..."
rm -rf "${BUILD_DIR}" "${ZIP_FILE}"
mkdir -p "${BUILD_DIR}"

echo "==> Installing dependencies..."
pip install \
    --target "${BUILD_DIR}" \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: \
    -r "${SCRIPT_DIR}/requirements.txt" \
    --quiet

echo "==> Copying application files..."
cp "${SCRIPT_DIR}/app.py" "${BUILD_DIR}/"
cp "${SCRIPT_DIR}/lambda_handler.py" "${BUILD_DIR}/"
cp "${SCRIPT_DIR}/app.db" "${BUILD_DIR}/"
cp -r "${SCRIPT_DIR}/templates" "${BUILD_DIR}/"
cp -r "${SCRIPT_DIR}/static" "${BUILD_DIR}/"

echo "==> Creating deployment zip..."
cd "${BUILD_DIR}"
zip -r "${ZIP_FILE}" . -x '*.pyc' '__pycache__/*' --quiet

ZIP_SIZE=$(du -h "${ZIP_FILE}" | cut -f1)
echo "==> Done! ${ZIP_FILE} (${ZIP_SIZE})"
