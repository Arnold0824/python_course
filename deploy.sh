#!/usr/bin/env bash
set -euo pipefail

# Repo absolute path on server. Defaults to this file's directory.
REPO_DIR="${REPO_DIR:-$(cd "$(dirname "$0")" && pwd)}"
BRANCH="${BRANCH:-main}"
RUN_BUILD="${RUN_BUILD:-1}"

echo "[deploy] start $(date -Iseconds)"
echo "[deploy] repo=${REPO_DIR}"
echo "[deploy] branch=${BRANCH}"

cd "${REPO_DIR}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[deploy] ${REPO_DIR} is not a git repository" >&2
  exit 1
fi

git fetch --prune origin "${BRANCH}"
git checkout "${BRANCH}"
git pull --ff-only origin "${BRANCH}"

if [[ "${RUN_BUILD}" == "1" ]]; then
  if command -v npm >/dev/null 2>&1; then
    npm ci
    npm run build
  else
    echo "[deploy] npm not found, skip build"
  fi
fi

if [[ -n "${POST_DEPLOY_CMD:-}" ]]; then
  echo "[deploy] running POST_DEPLOY_CMD"
  bash -lc "${POST_DEPLOY_CMD}"
fi

echo "[deploy] done $(date -Iseconds)"
