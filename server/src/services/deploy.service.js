import { spawn } from 'node:child_process';

export function createDeployService({ config, logger }) {
  let deploying = false;

  function isDeploying() {
    return deploying;
  }

  function start(reason) {
    deploying = true;
    logger.info('deploy started', {
      cwd: config.deploy.cwd,
      reason,
      scriptPath: config.deploy.scriptPath,
      shell: config.deploy.shell,
    });

    const shellArgs =
      process.platform === 'win32' && config.deploy.shell.toLowerCase().includes('powershell')
        ? ['-File', config.deploy.scriptPath]
        : [config.deploy.scriptPath];

    const child = spawn(config.deploy.shell, shellArgs, {
      cwd: config.deploy.cwd,
      env: process.env,
      stdio: 'inherit',
    });

    child.on('error', (error) => {
      deploying = false;
      logger.error('deploy process failed to start', {
        message: error.message,
        reason,
      });
    });

    child.on('exit', (code, signal) => {
      deploying = false;

      if (code === 0) {
        logger.info('deploy completed', {
          exitCode: code,
          reason,
        });
        return;
      }

      logger.error('deploy failed', {
        code: code ?? null,
        reason,
        signal: signal ?? null,
      });
    });
  }

  return {
    isDeploying,
    start,
  };
}
