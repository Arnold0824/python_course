import path from 'node:path';
import { REPO_ROOT, SERVER_LOG_DIR } from './paths.js';

function readString(name, fallback = '') {
  const value = process.env[name];
  if (value === undefined || value === null || value === '') {
    return fallback;
  }

  return String(value);
}

function readInt(name, fallback) {
  const value = process.env[name];
  if (value === undefined || value === null || value === '') {
    return fallback;
  }

  const parsed = Number.parseInt(value, 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`${name} must be an integer`);
  }

  return parsed;
}

function readBool(name, fallback = false) {
  const value = process.env[name];
  if (value === undefined || value === null || value === '') {
    return fallback;
  }

  return ['1', 'true', 'yes', 'on'].includes(String(value).toLowerCase());
}

function readIdentifier(name, fallback) {
  const value = readString(name, fallback);
  if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(value)) {
    throw new Error(`${name} must contain only letters, numbers, and underscores`);
  }

  return value;
}

export function loadConfig() {
  return {
    app: {
      host: readString('SERVER_HOST', '0.0.0.0'),
      port: readInt('SERVER_PORT', 9001),
      env: readString('NODE_ENV', 'development'),
      jsonLimit: readString('JSON_BODY_LIMIT', '1mb'),
      logLevel: readString('LOG_LEVEL', 'info'),
      logFile: readString('SERVER_LOG_FILE', path.join(SERVER_LOG_DIR, 'server.log')),
      name: 'python-course-server',
    },
    mysql: {
      host: '127.0.0.1',
      port: 3306,
      user: 'root',
      password: readString('MYSQL_PASSWORD', ''),
      database: 'python_course',
      connectionLimit: 10,
      connectTimeout: 10000,
    },
    webhook: {
      path: readString('WEBHOOK_PATH', '/api/webhooks/github'),
      secret: readString('WEBHOOK_SECRET', ''),
      branchRef: readString('WEBHOOK_BRANCH_REF', 'refs/heads/main'),
      maxBodySize: readString('WEBHOOK_MAX_BODY_SIZE', '1mb'),
      testOnly: readBool('WEBHOOK_TEST_ONLY', false),
    },
    deploy: {
      cwd: readString('DEPLOY_CWD', REPO_ROOT),
      scriptPath: readString('DEPLOY_SCRIPT', path.join(REPO_ROOT, 'deploy.sh')),
      shell: readString(
        'DEPLOY_SHELL',
        process.platform === 'win32' ? 'powershell.exe' : '/bin/bash',
      ),
    },
    analytics: {
      pageViewTable: readIdentifier('ANALYTICS_PAGE_VIEW_TABLE', 'page_views'),
    },
    admin: {
      token: readString('ADMIN_TOKEN', ''),
    },
  };
}
