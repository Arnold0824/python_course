import { startServer } from './server/src/index.js';

startServer().catch((error) => {
  console.error('[server] failed to start');
  console.error(error);
  process.exit(1);
});
