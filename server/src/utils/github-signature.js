import crypto from 'node:crypto';

export function getHeaderValue(value) {
  if (!value) {
    return '';
  }

  return Array.isArray(value) ? value[0] : value;
}

export function verifyGitHubSignature(rawBody, signatureHeader, secret) {
  if (!signatureHeader || !signatureHeader.startsWith('sha256=')) {
    return false;
  }

  const expected = `sha256=${crypto.createHmac('sha256', secret).update(rawBody).digest('hex')}`;
  const receivedBuffer = Buffer.from(signatureHeader);
  const expectedBuffer = Buffer.from(expected);

  if (receivedBuffer.length !== expectedBuffer.length) {
    return false;
  }

  return crypto.timingSafeEqual(receivedBuffer, expectedBuffer);
}
