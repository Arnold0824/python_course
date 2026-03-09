#!/usr/bin/env bash
set -euo pipefail

# Repo absolute path on server. Defaults to this file's directory.
REPO_DIR="${REPO_DIR:-$(cd "$(dirname "$0")" && pwd)}"
BRANCH="${BRANCH:-main}"
RUN_BUILD="${RUN_BUILD:-1}"
SERVER_DIR="${SERVER_DIR:-${REPO_DIR}/server}"
RUN_SERVER_INSTALL="${RUN_SERVER_INSTALL:-1}"
PM2_APP_NAME="${PM2_APP_NAME:-python-course-server}"
PM2_ECOSYSTEM_CONFIG="${PM2_ECOSYSTEM_CONFIG:-${SERVER_DIR}/ecosystem.config.cjs}"
PM2_AUTO_RESTART="${PM2_AUTO_RESTART:-1}"

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

if [[ "${RUN_SERVER_INSTALL}" == "1" ]]; then
  if [[ -f "${SERVER_DIR}/package.json" ]]; then
    if command -v npm >/dev/null 2>&1; then
      echo "[deploy] installing server dependencies"
      if [[ -f "${SERVER_DIR}/package-lock.json" ]]; then
        npm --prefix "${SERVER_DIR}" ci
      else
        npm --prefix "${SERVER_DIR}" install
      fi
    else
      echo "[deploy] npm not found, skip server dependency install"
    fi
  else
    echo "[deploy] server package.json not found, skip server dependency install"
  fi
fi

if [[ "${RUN_BUILD}" == "1" ]]; then
  if command -v npm >/dev/null 2>&1; then
    npm ci
    npm run build
  else
    echo "[deploy] npm not found, skip build"
  fi
fi

if [[ "${PM2_AUTO_RESTART}" == "1" ]]; then
  if command -v pm2 >/dev/null 2>&1; then
    if pm2 describe "${PM2_APP_NAME}" >/dev/null 2>&1; then
      echo "[deploy] restarting pm2 app ${PM2_APP_NAME}"
      pm2 restart "${PM2_APP_NAME}" --update-env
    elif [[ -f "${PM2_ECOSYSTEM_CONFIG}" ]]; then
      echo "[deploy] starting pm2 app ${PM2_APP_NAME} from ${PM2_ECOSYSTEM_CONFIG}"
      pm2 start "${PM2_ECOSYSTEM_CONFIG}" --only "${PM2_APP_NAME}" --update-env
      pm2 save
    else
      echo "[deploy] pm2 ecosystem config not found, skip pm2 start"
    fi
  else
    echo "[deploy] pm2 not found, skip pm2 restart"
  fi
fi

if [[ -n "${POST_DEPLOY_CMD:-}" ]]; then
  echo "[deploy] running POST_DEPLOY_CMD"
  bash -lc "${POST_DEPLOY_CMD}"
fi

echo "[deploy] done $(date -Iseconds)"
