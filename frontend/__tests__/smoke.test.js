const assert = require('node:assert/strict');

test('frontend API base is configured', () => {
  const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api';
  assert.ok(typeof apiBase === 'string');
  assert.ok(apiBase.length > 0);
});
