import fs from 'node:fs/promises';
import path from 'node:path';

const LEVELS = {
  debug: 10,
  info: 20,
  warn: 30,
  error: 40,
};

function stringifyMeta(meta) {
  if (!meta || Object.keys(meta).length === 0) {
    return '';
  }

  try {
    return ` ${JSON.stringify(meta)}`;
  } catch {
    return ' {"meta":"[unserializable]"}';
  }
}

export function createLogger({ level = 'info', logFile }) {
  const threshold = LEVELS[level] ?? LEVELS.info;
  let logDirReady;

  function ensureLogDir() {
    if (!logDirReady) {
      logDirReady = fs.mkdir(path.dirname(logFile), { recursive: true });
    }

    return logDirReady;
  }

  function write(entryLevel, message, meta = {}) {
    if ((LEVELS[entryLevel] ?? LEVELS.info) < threshold) {
      return;
    }

    const line =
      `${new Date().toISOString()} [${entryLevel.toUpperCase()}] ${message}` +
      `${stringifyMeta(meta)}\n`;

    if (entryLevel === 'error') {
      process.stderr.write(line);
    } else {
      process.stdout.write(line);
    }

    void ensureLogDir()
      .then(() => fs.appendFile(logFile, line, 'utf8'))
      .catch((error) => {
        process.stderr.write(
          `${new Date().toISOString()} [ERROR] log write failed {"message":"${error.message}"}\n`,
        );
      });
  }

  return {
    debug(message, meta) {
      write('debug', message, meta);
    },
    info(message, meta) {
      write('info', message, meta);
    },
    warn(message, meta) {
      write('warn', message, meta);
    },
    error(message, meta) {
      write('error', message, meta);
    },
  };
}
