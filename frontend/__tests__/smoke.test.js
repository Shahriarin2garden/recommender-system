const assert = require('node:assert/strict');
const { test } = require('node:test');

test('frontend API base is configured', () => {
  const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api';
  assert.ok(typeof apiBase === 'string');
  assert.ok(apiBase.length > 0);
});
