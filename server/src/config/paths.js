import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const CONFIG_DIR = __dirname;
export const SERVER_ROOT = path.resolve(CONFIG_DIR, '..', '..');
export const REPO_ROOT = path.resolve(SERVER_ROOT, '..');
export const SERVER_LOG_DIR = path.join(SERVER_ROOT, 'logs');
export const SERVER_DATA_DIR = path.join(SERVER_ROOT, 'data');
