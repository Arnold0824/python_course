import { startServer } from './index.js';

startServer().catch((error) => {
  console.error('[server] startup failed');
  console.error(error);
  process.exit(1);
});
