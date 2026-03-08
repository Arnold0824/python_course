module.exports = {
  apps: [
    {
      name: 'python-course-server',
      cwd: __dirname,
      script: 'src/index.js',
      interpreter: 'node',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_restarts: 10,
      restart_delay: 3000,
      env: {
        NODE_ENV: 'production',
        SERVER_HOST: '127.0.0.1',
        SERVER_PORT: '9001',
      },
    },
  ],
};
